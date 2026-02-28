"""Audit log helpers for FlatMagic sessions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_audit_log(log_dir: str | Path, session_id: str, payload: dict[str, Any]) -> Path:
    directory = Path(log_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{session_id}.json"
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    return path
