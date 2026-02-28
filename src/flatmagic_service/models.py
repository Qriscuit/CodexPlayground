"""Data models and validation helpers for service requests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class PayloadValidationError(ValueError):
    """Raised when client request payload is missing required data."""


@dataclass(frozen=True)
class Bounds:
    left: int
    top: int
    width: int
    height: int

    @property
    def right(self) -> int:
        return self.left + self.width

    @property
    def bottom(self) -> int:
        return self.top + self.height

    @classmethod
    def from_payload(cls, payload: Any) -> "Bounds":
        if not isinstance(payload, dict):
            raise PayloadValidationError("`bounds` must be an object.")
        required = ("left", "top", "width", "height")
        missing = [key for key in required if key not in payload]
        if missing:
            raise PayloadValidationError(f"`bounds` missing keys: {', '.join(missing)}")

        left = _to_int(payload["left"], "bounds.left")
        top = _to_int(payload["top"], "bounds.top")
        width = _to_int(payload["width"], "bounds.width")
        height = _to_int(payload["height"], "bounds.height")
        if width <= 0 or height <= 0:
            raise PayloadValidationError("`bounds.width` and `bounds.height` must be > 0.")
        return cls(left=left, top=top, width=width, height=height)

    def as_dict(self) -> dict[str, int]:
        return {
            "left": self.left,
            "top": self.top,
            "width": self.width,
            "height": self.height,
            "right": self.right,
            "bottom": self.bottom,
        }


def _to_int(value: Any, field: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise PayloadValidationError(f"`{field}` must be an integer.") from exc
