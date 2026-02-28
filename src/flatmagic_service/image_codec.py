"""RGBA payload encode/decode helpers."""

from __future__ import annotations

import base64
from typing import Any

from .models import PayloadValidationError


def decode_rgba8(payload: Any, expected_length: int) -> bytearray:
    """Decode rgba8 payload from list[int], bytes, or base64 object/string."""
    if isinstance(payload, list):
        try:
            raw = bytearray(int(v) & 0xFF for v in payload)
        except (TypeError, ValueError) as exc:
            raise PayloadValidationError("`rgba8` list must contain integers in [0,255].") from exc
    elif isinstance(payload, (bytes, bytearray)):
        raw = bytearray(payload)
    elif isinstance(payload, str):
        raw = _decode_base64_string(payload)
    elif isinstance(payload, dict):
        encoding = str(payload.get("encoding", "")).lower()
        if encoding != "base64":
            raise PayloadValidationError("`rgba8.encoding` must be `base64` when object payload is used.")
        data = payload.get("data")
        if not isinstance(data, str):
            raise PayloadValidationError("`rgba8.data` must be a base64 string.")
        raw = _decode_base64_string(data)
    else:
        raise PayloadValidationError("`rgba8` must be a list, bytes, base64 string, or {encoding,data}.")

    if len(raw) != expected_length:
        raise PayloadValidationError(
            f"`rgba8` has {len(raw)} bytes but expected {expected_length} from bounds."
        )
    return raw


def encode_rgba8(payload: bytes | bytearray, encoding: str = "list") -> list[int] | dict[str, str]:
    normalized = encoding.lower().strip()
    if normalized in ("list", "", "json"):
        return list(payload)
    if normalized == "base64":
        encoded = base64.b64encode(bytes(payload)).decode("ascii")
        return {"encoding": "base64", "data": encoded}
    raise PayloadValidationError(f"Unsupported output encoding: {encoding}")


def _decode_base64_string(raw: str) -> bytearray:
    value = raw.strip()
    if value.startswith("base64:"):
        value = value[len("base64:") :]
    try:
        return bytearray(base64.b64decode(value, validate=True))
    except Exception as exc:  # noqa: BLE001
        raise PayloadValidationError("Failed to decode base64 `rgba8` payload.") from exc
