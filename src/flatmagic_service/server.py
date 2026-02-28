"""HTTP server for FlatMagic local prototype service."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from . import __version__
from .audit import write_audit_log
from .detect import detect_regions
from .image_codec import decode_rgba8, encode_rgba8
from .models import Bounds, PayloadValidationError
from .repair import apply_repair


class FlatMagicHTTPServer(ThreadingHTTPServer):
    """Custom HTTP server state for request handlers."""

    def __init__(self, host_port: tuple[str, int], log_dir: str | Path, output_encoding: str):
        super().__init__(host_port, FlatMagicRequestHandler)
        self.log_dir = Path(log_dir)
        self.output_encoding = output_encoding


class FlatMagicRequestHandler(BaseHTTPRequestHandler):
    """Simple JSON API for detect/repair workflows."""

    server_version = "FlatMagicPrototypeHTTP/0.1"
    protocol_version = "HTTP/1.1"

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send_json(
                HTTPStatus.OK,
                {
                    "status": "ok",
                    "service": "flatmagic-local",
                    "version": __version__,
                    "time_utc": _utc_now(),
                },
            )
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/v1/echo":
            payload = self._read_json_body()
            self._send_json(HTTPStatus.OK, {"echo": payload, "time_utc": _utc_now()})
            return

        if self.path == "/v1/detect":
            payload = self._read_json_body()
            try:
                response = self._handle_detect(payload)
                self._send_json(HTTPStatus.OK, response)
            except PayloadValidationError as exc:
                self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return

        if self.path == "/v1/repair":
            payload = self._read_json_body()
            try:
                response = self._handle_repair(payload)
                self._send_json(HTTPStatus.OK, response)
            except PayloadValidationError as exc:
                self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def _handle_detect(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise PayloadValidationError("Request body must be a JSON object.")
        bounds = Bounds.from_payload(payload.get("bounds"))
        rgba = decode_rgba8(payload.get("rgba8"), expected_length=bounds.width * bounds.height * 4)

        options = payload.get("options", {})
        if options is None:
            options = {}
        if not isinstance(options, dict):
            raise PayloadValidationError("`options` must be an object.")

        proposals, stats = detect_regions(rgba, bounds.width, bounds.height, options)
        session_id = str(payload.get("session_id") or _default_session_id())

        response = {
            "session_id": session_id,
            "document_id": str(payload.get("document_id", "")),
            "layer_id": str(payload.get("layer_id", "")),
            "bounds": bounds.as_dict(),
            "proposals": proposals,
            "stats": stats,
            "time_utc": _utc_now(),
        }
        return response

    def _handle_repair(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise PayloadValidationError("Request body must be a JSON object.")
        bounds = Bounds.from_payload(payload.get("bounds"))
        source = decode_rgba8(payload.get("rgba8"), expected_length=bounds.width * bounds.height * 4)

        proposals = payload.get("proposals", [])
        if not isinstance(proposals, list):
            raise PayloadValidationError("`proposals` must be an array.")
        accepted = payload.get("accepted_region_ids", [])
        if not isinstance(accepted, list):
            raise PayloadValidationError("`accepted_region_ids` must be an array.")
        accepted_ids = {str(value) for value in accepted}

        options = payload.get("options", {})
        if options is None:
            options = {}
        if not isinstance(options, dict):
            raise PayloadValidationError("`options` must be an object.")

        repaired, repair_stats = apply_repair(
            rgba=source,
            width=bounds.width,
            height=bounds.height,
            proposals=proposals,
            accepted_region_ids=accepted_ids,
            options=options,
        )

        output_encoding = str(payload.get("output_encoding") or self.server.output_encoding)
        encoded = encode_rgba8(repaired, output_encoding)
        session_id = str(payload.get("session_id") or _default_session_id())
        document_id = str(payload.get("document_id", ""))
        layer_id = str(payload.get("layer_id", ""))

        source_hash = _sha256_hex(source)
        result_hash = _sha256_hex(repaired)
        audit_record = {
            "session_id": session_id,
            "document_id": document_id,
            "layer_id": layer_id,
            "accepted_region_ids": sorted(accepted_ids),
            "repair_stats": repair_stats,
            "source_hash": source_hash,
            "result_hash": result_hash,
            "time_utc": _utc_now(),
        }
        should_write_log = bool(payload.get("write_log", True))
        log_path = None
        if should_write_log:
            log_path = write_audit_log(self.server.log_dir, session_id, audit_record)

        response = {
            "session_id": session_id,
            "document_id": document_id,
            "layer_id": layer_id,
            "bounds": bounds.as_dict(),
            "accepted_region_ids": sorted(accepted_ids),
            "repair_stats": repair_stats,
            "rgba8_encoding": output_encoding,
            "rgba8": encoded,
            "source_hash": source_hash,
            "result_hash": result_hash,
            "audit_log": str(log_path) if log_path else None,
            "time_utc": _utc_now(),
        }
        return response

    def _read_json_body(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0:
            return {}
        raw = self.rfile.read(content_length)
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise PayloadValidationError("Body must be valid UTF-8 JSON.") from exc
        if not isinstance(parsed, dict):
            raise PayloadValidationError("Body root must be a JSON object.")
        return parsed

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        content = json.dumps(payload).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        """Override to reduce noisy stdout output during tests."""
        del format, args


def create_server(host: str, port: int, log_dir: str | Path = "logs", output_encoding: str = "list") -> FlatMagicHTTPServer:
    return FlatMagicHTTPServer((host, port), log_dir=log_dir, output_encoding=output_encoding)


def run_server(host: str, port: int, log_dir: str | Path = "logs", output_encoding: str = "list") -> None:
    server = create_server(host=host, port=port, log_dir=log_dir, output_encoding=output_encoding)
    print(f"[flatmagic-service] listening on http://{host}:{server.server_address[1]}")
    print(f"[flatmagic-service] audit logs: {Path(log_dir).resolve()}")
    server.serve_forever()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="FlatMagic local prototype service")
    parser.add_argument("--host", default=os.getenv("FLATMAGIC_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("FLATMAGIC_PORT", "8765")))
    parser.add_argument("--log-dir", default=os.getenv("FLATMAGIC_LOG_DIR", "logs"))
    parser.add_argument(
        "--output-encoding",
        default=os.getenv("FLATMAGIC_OUTPUT_ENCODING", "list"),
        choices=("list", "base64"),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    run_server(args.host, args.port, args.log_dir, args.output_encoding)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _default_session_id() -> str:
    return f"sess-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"


def _sha256_hex(payload: bytes | bytearray) -> str:
    return hashlib.sha256(bytes(payload)).hexdigest()
