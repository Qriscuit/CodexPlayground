# FlatMagic Prototype API Contracts

## Service API

### `GET /health`

Response:

```json
{
  "status": "ok",
  "service": "flatmagic-local",
  "version": "0.1.0",
  "time_utc": "2026-02-28T00:00:00+00:00"
}
```

### `POST /v1/detect`

Request:

```json
{
  "session_id": "sess-...",
  "document_id": "12",
  "layer_id": "34",
  "bounds": { "left": 0, "top": 0, "width": 512, "height": 512 },
  "rgba8": [0, 0, 0, 255],
  "options": {
    "contrast_threshold": 32,
    "min_region_area": 2,
    "max_region_fraction": 0.02,
    "max_regions": 50
  }
}
```

Response:

```json
{
  "session_id": "sess-...",
  "document_id": "12",
  "layer_id": "34",
  "bounds": {
    "left": 0,
    "top": 0,
    "width": 512,
    "height": 512,
    "right": 512,
    "bottom": 512
  },
  "proposals": [
    {
      "region_id": "r001",
      "bbox": { "x": 25, "y": 40, "width": 4, "height": 3 },
      "confidence": 0.87,
      "mask_rle": { "width": 4, "height": 3, "runs": [[0, 2], [5, 1]] },
      "reason": "high_local_contrast_outlier",
      "risk_tags": ["conservative_ok"],
      "pixel_count": 3,
      "mean_delta": 48.2
    }
  ],
  "stats": {
    "candidate_pixel_count": 9,
    "proposal_count": 1,
    "threshold": 32.0,
    "min_region_area": 2,
    "max_region_area": 5242
  },
  "time_utc": "2026-02-28T00:00:00+00:00"
}
```

### `POST /v1/repair`

Request:

```json
{
  "session_id": "sess-...",
  "document_id": "12",
  "layer_id": "34",
  "bounds": { "left": 0, "top": 0, "width": 512, "height": 512 },
  "rgba8": [0, 0, 0, 255],
  "proposals": [],
  "accepted_region_ids": ["r001"],
  "options": { "blend_strength": 0.7 },
  "write_log": true
}
```

Response fields include:

- `repair_stats.changed_pixel_count`
- `repair_stats.accepted_region_count`
- `rgba8` (list by default, base64 optional)
- `source_hash`
- `result_hash`
- `audit_log` path

## Plugin-side Data Contracts

- `LayerSnapshot`
  - `document_id`, `layer_id`, `bounds`, `color_mode`, `rgba8`, `source_hash`
- `RepairProposal`
  - `region_id`, `bbox`, `confidence`, `mask_rle`, `reason`, `risk_tags`
- `RepairSession`
  - `session_id`, `snapshot`, `proposals`, `selected_region_ids`, `started_at`, `result_layer_ids`
- `AuditEntry`
  - `session_id`, `document_id`, `source_layer_id`, `accepted_region_ids`, `proposals`, `result_layer_ids`, `created_at`
