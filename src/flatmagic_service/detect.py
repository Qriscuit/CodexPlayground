"""Conservative defect proposal generator for FlatMagic prototype."""

from __future__ import annotations

from collections import deque
from typing import Any


def detect_regions(
    rgba: bytearray | bytes,
    width: int,
    height: int,
    options: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    opts = options or {}
    threshold = float(opts.get("contrast_threshold", 32))
    min_region_area = max(1, int(opts.get("min_region_area", 2)))
    max_region_fraction = max(0.0001, min(1.0, float(opts.get("max_region_fraction", 0.02))))
    max_region_area = max(1, int(width * height * max_region_fraction))
    max_regions = max(1, int(opts.get("max_regions", 50)))

    luminance = [0.0] * (width * height)
    alpha = [0] * (width * height)
    for idx in range(width * height):
        base = idx * 4
        r = rgba[base]
        g = rgba[base + 1]
        b = rgba[base + 2]
        a = rgba[base + 3]
        alpha[idx] = a
        luminance[idx] = (0.2126 * r) + (0.7152 * g) + (0.0722 * b)

    candidate = [False] * (width * height)
    delta_map = [0.0] * (width * height)

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            idx = y * width + x
            if alpha[idx] == 0:
                continue
            nbr = [
                luminance[idx - 1],
                luminance[idx + 1],
                luminance[idx - width],
                luminance[idx + width],
            ]
            avg = sum(nbr) / 4.0
            delta = abs(luminance[idx] - avg)
            delta_map[idx] = delta
            if delta >= threshold:
                candidate[idx] = True

    visited = [False] * (width * height)
    raw_regions: list[dict[str, Any]] = []

    for idx, flag in enumerate(candidate):
        if not flag or visited[idx]:
            continue

        queue: deque[int] = deque([idx])
        visited[idx] = True
        component: list[int] = []
        delta_sum = 0.0
        min_x = width
        max_x = 0
        min_y = height
        max_y = 0

        while queue:
            current = queue.popleft()
            component.append(current)
            delta_sum += delta_map[current]

            cx = current % width
            cy = current // width
            min_x = min(min_x, cx)
            max_x = max(max_x, cx)
            min_y = min(min_y, cy)
            max_y = max(max_y, cy)

            neighbors = (
                current - 1 if cx > 0 else None,
                current + 1 if cx < width - 1 else None,
                current - width if cy > 0 else None,
                current + width if cy < height - 1 else None,
            )
            for nxt in neighbors:
                if nxt is None or visited[nxt] or not candidate[nxt]:
                    continue
                visited[nxt] = True
                queue.append(nxt)

        area = len(component)
        if area < min_region_area or area > max_region_area:
            continue

        bbox_width = max_x - min_x + 1
        bbox_height = max_y - min_y + 1
        mean_delta = delta_sum / area if area else 0.0
        region_confidence = _compute_confidence(
            mean_delta=mean_delta,
            area=area,
            image_area=width * height,
            max_region_fraction=max_region_fraction,
        )
        risk_tags = _risk_tags(region_confidence, area, width * height)

        raw_regions.append(
            {
                "bbox": {"x": min_x, "y": min_y, "width": bbox_width, "height": bbox_height},
                "confidence": round(region_confidence, 3),
                "mask_rle": _encode_mask_rle(component, width, min_x, min_y, bbox_width, bbox_height),
                "reason": "high_local_contrast_outlier",
                "risk_tags": risk_tags,
                "pixel_count": area,
                "mean_delta": round(mean_delta, 3),
            }
        )

    raw_regions.sort(key=lambda item: (item["confidence"], -item["pixel_count"]), reverse=True)

    proposals = []
    for order, region in enumerate(raw_regions[:max_regions], start=1):
        proposal = dict(region)
        proposal["region_id"] = f"r{order:03d}"
        proposals.append(proposal)

    stats = {
        "candidate_pixel_count": int(sum(1 for v in candidate if v)),
        "proposal_count": len(proposals),
        "threshold": threshold,
        "min_region_area": min_region_area,
        "max_region_area": max_region_area,
    }
    return proposals, stats


def _compute_confidence(mean_delta: float, area: int, image_area: int, max_region_fraction: float) -> float:
    delta_score = min(1.0, max(0.0, mean_delta / 96.0))
    area_ratio = area / max(1, image_area)
    max_ratio = max_region_fraction
    size_penalty = min(1.0, area_ratio / max_ratio)
    confidence = 0.42 + (0.50 * delta_score) - (0.18 * size_penalty)
    return max(0.05, min(0.98, confidence))


def _risk_tags(confidence: float, area: int, image_area: int) -> list[str]:
    tags = []
    if confidence < 0.55:
        tags.append("low_confidence")
    if area > image_area * 0.01:
        tags.append("large_region")
    if not tags:
        tags.append("conservative_ok")
    return tags


def _encode_mask_rle(
    component: list[int],
    width: int,
    min_x: int,
    min_y: int,
    bbox_width: int,
    bbox_height: int,
) -> dict[str, Any]:
    local_indices = []
    for idx in component:
        x = idx % width
        y = idx // width
        lx = x - min_x
        ly = y - min_y
        local_indices.append((ly * bbox_width) + lx)
    local_indices.sort()

    runs: list[list[int]] = []
    if local_indices:
        run_start = local_indices[0]
        run_length = 1
        for value in local_indices[1:]:
            if value == run_start + run_length:
                run_length += 1
                continue
            runs.append([run_start, run_length])
            run_start = value
            run_length = 1
        runs.append([run_start, run_length])

    return {"width": bbox_width, "height": bbox_height, "runs": runs}
