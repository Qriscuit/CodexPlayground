"""Unit tests for FlatMagic local service endpoints."""

from __future__ import annotations

import json
import socket
import sys
import threading
import time
import unittest
from http.client import HTTPConnection
from pathlib import Path
from tempfile import TemporaryDirectory

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from flatmagic_service.server import create_server  # noqa: E402


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _sample_rgba(width: int, height: int) -> list[int]:
    values = []
    for y in range(height):
        for x in range(width):
            base = 120
            if x == width // 2 and y == height // 2:
                base = 255
            values.extend([base, base, base, 255])
    return values


class FlatMagicServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = TemporaryDirectory()
        port = _find_free_port()
        cls.server = create_server("127.0.0.1", port, log_dir=cls.temp_dir.name, output_encoding="list")
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)
        cls.temp_dir.cleanup()

    def _request(self, method: str, path: str, payload: dict | None = None) -> tuple[int, dict]:
        conn = HTTPConnection("127.0.0.1", self.port, timeout=5)
        body = "" if payload is None else json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        conn.request(method, path, body=body, headers=headers)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        conn.close()
        return response.status, json.loads(data)

    def test_health(self) -> None:
        status, payload = self._request("GET", "/health")
        self.assertEqual(status, 200)
        self.assertEqual(payload["status"], "ok")
        self.assertIn("version", payload)

    def test_detect_returns_proposals(self) -> None:
        width = 8
        height = 8
        status, payload = self._request(
            "POST",
            "/v1/detect",
            {
                "session_id": "detect-session",
                "document_id": "doc-1",
                "layer_id": "layer-1",
                "bounds": {"left": 0, "top": 0, "width": width, "height": height},
                "rgba8": _sample_rgba(width, height),
                "options": {
                    "contrast_threshold": 10,
                    "min_region_area": 1,
                    "max_region_fraction": 0.5,
                    "max_regions": 10,
                },
            },
        )
        self.assertEqual(status, 200)
        self.assertIn("proposals", payload)
        self.assertGreaterEqual(len(payload["proposals"]), 1)
        proposal = payload["proposals"][0]
        self.assertIn("region_id", proposal)
        self.assertIn("bbox", proposal)
        self.assertIn("mask_rle", proposal)

    def test_repair_identity_when_no_selection(self) -> None:
        width = 8
        height = 8
        rgba = _sample_rgba(width, height)
        status, payload = self._request(
            "POST",
            "/v1/repair",
            {
                "session_id": "repair-identity",
                "document_id": "doc-1",
                "layer_id": "layer-1",
                "bounds": {"left": 0, "top": 0, "width": width, "height": height},
                "rgba8": rgba,
                "proposals": [],
                "accepted_region_ids": [],
            },
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["rgba8"], rgba)
        self.assertEqual(payload["repair_stats"]["changed_pixel_count"], 0)

    def test_repair_changes_when_region_selected(self) -> None:
        width = 8
        height = 8
        rgba = _sample_rgba(width, height)
        detect_status, detect_payload = self._request(
            "POST",
            "/v1/detect",
            {
                "session_id": "repair-detect",
                "document_id": "doc-1",
                "layer_id": "layer-1",
                "bounds": {"left": 0, "top": 0, "width": width, "height": height},
                "rgba8": rgba,
                "options": {
                    "contrast_threshold": 10,
                    "min_region_area": 1,
                    "max_region_fraction": 0.5,
                },
            },
        )
        self.assertEqual(detect_status, 200)
        self.assertGreater(len(detect_payload["proposals"]), 0)
        selected_id = detect_payload["proposals"][0]["region_id"]

        repair_status, repair_payload = self._request(
            "POST",
            "/v1/repair",
            {
                "session_id": "repair-apply",
                "document_id": "doc-1",
                "layer_id": "layer-1",
                "bounds": {"left": 0, "top": 0, "width": width, "height": height},
                "rgba8": rgba,
                "proposals": detect_payload["proposals"],
                "accepted_region_ids": [selected_id],
                "write_log": True,
            },
        )
        self.assertEqual(repair_status, 200)
        self.assertGreater(repair_payload["repair_stats"]["changed_pixel_count"], 0)
        self.assertNotEqual(repair_payload["rgba8"], rgba)
        self.assertTrue(repair_payload["audit_log"])


if __name__ == "__main__":
    unittest.main()
