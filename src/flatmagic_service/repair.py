"""Conservative region repair operators for FlatMagic prototype."""

from __future__ import annotations

from typing import Any


def apply_repair(
    rgba: bytes | bytearray,
    width: int,
    height: int,
    proposals: list[dict[str, Any]],
    accepted_region_ids: set[str],
    options: dict[str, Any] | None = None,
) -> tuple[bytearray, dict[str, Any]]:
    opts = options or {}
    blend_strength = max(0.0, min(1.0, float(opts.get("blend_strength", 0.7))))

    accepted_pixels = _resolve_accepted_pixels(proposals, accepted_region_ids, width, height)
    if not accepted_pixels:
        return bytearray(rgba), {"changed_pixel_count": 0, "accepted_region_count": 0}

    source = bytearray(rgba)
    output = bytearray(rgba)
    changed = 0

    for idx in sorted(accepted_pixels):
        x = idx % width
        y = idx // width

        neighbors: list[tuple[int, int, int]] = []
        fallback_neighbors: list[tuple[int, int, int]] = []
        for ny in range(max(0, y - 1), min(height - 1, y + 1) + 1):
            for nx in range(max(0, x - 1), min(width - 1, x + 1) + 1):
                if nx == x and ny == y:
                    continue
                nidx = (ny * width) + nx
                base = nidx * 4
                if source[base + 3] == 0:
                    continue
                rgb = (source[base], source[base + 1], source[base + 2])
                fallback_neighbors.append(rgb)
                if nidx not in accepted_pixels:
                    neighbors.append(rgb)

        sample = neighbors if neighbors else fallback_neighbors
        if not sample:
            continue

        avg_r = sum(pixel[0] for pixel in sample) / len(sample)
        avg_g = sum(pixel[1] for pixel in sample) / len(sample)
        avg_b = sum(pixel[2] for pixel in sample) / len(sample)

        base = idx * 4
        old_r = source[base]
        old_g = source[base + 1]
        old_b = source[base + 2]

        new_r = int(round((1.0 - blend_strength) * old_r + blend_strength * avg_r))
        new_g = int(round((1.0 - blend_strength) * old_g + blend_strength * avg_g))
        new_b = int(round((1.0 - blend_strength) * old_b + blend_strength * avg_b))

        if old_r != new_r or old_g != new_g or old_b != new_b:
            changed += 1

        output[base] = new_r
        output[base + 1] = new_g
        output[base + 2] = new_b

    return output, {"changed_pixel_count": changed, "accepted_region_count": len(accepted_region_ids)}


def _resolve_accepted_pixels(
    proposals: list[dict[str, Any]],
    accepted_region_ids: set[str],
    width: int,
    height: int,
) -> set[int]:
    accepted_pixels: set[int] = set()
    for proposal in proposals:
        region_id = str(proposal.get("region_id", ""))
        if region_id not in accepted_region_ids:
            continue
        bbox = proposal.get("bbox", {})
        if not isinstance(bbox, dict):
            continue
        x = int(bbox.get("x", 0))
        y = int(bbox.get("y", 0))
        bw = int(bbox.get("width", 0))
        bh = int(bbox.get("height", 0))
        if bw <= 0 or bh <= 0:
            continue

        mask_rle = proposal.get("mask_rle", {})
        local_indices = _decode_mask_rle(mask_rle, bw, bh)
        for local in local_indices:
            lx = local % bw
            ly = local // bw
            gx = x + lx
            gy = y + ly
            if gx < 0 or gx >= width or gy < 0 or gy >= height:
                continue
            accepted_pixels.add((gy * width) + gx)
    return accepted_pixels


def _decode_mask_rle(mask_rle: Any, bbox_width: int, bbox_height: int) -> set[int]:
    if not isinstance(mask_rle, dict):
        return set()
    runs = mask_rle.get("runs", [])
    if not isinstance(runs, list):
        return set()

    max_index = bbox_width * bbox_height
    out: set[int] = set()
    for run in runs:
        if not isinstance(run, (list, tuple)) or len(run) != 2:
            continue
        start = int(run[0])
        length = int(run[1])
        if length <= 0:
            continue
        for value in range(start, start + length):
            if 0 <= value < max_index:
                out.add(value)
    return out
