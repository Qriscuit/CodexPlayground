# CodexPlayground

FlatMagic Photoshop prototype workspace.

## Components

- `photoshop-plugin/` - Photoshop UXP panel plugin (detect -> preview -> apply).
- `src/flatmagic_service/` - local Python HTTP service with:
  - `GET /health`
  - `POST /v1/echo`
  - `POST /v1/detect`
  - `POST /v1/repair`
- `tests/` - unit tests for the local service.

## Run the Python service

```powershell
python src/run_flatmagic_service.py --host 127.0.0.1 --port 8765
```

Or as a module:

```powershell
$env:PYTHONPATH="src"
python -m flatmagic_service --host 127.0.0.1 --port 8765
```

## Service request shape

### `POST /v1/detect`

- Required: `document_id`, `layer_id`, `bounds`, `rgba8`
- Optional: `session_id`, `options`

### `POST /v1/repair`

- Required: `document_id`, `layer_id`, `bounds`, `rgba8`, `proposals`, `accepted_region_ids`
- Optional: `session_id`, `options`, `output_encoding`, `write_log`

## Run tests

```powershell
python -m unittest tests/test_flatmagic_service.py -v
```

## Load plugin in Photoshop

1. Open UXP Developer Tool.
2. Add plugin from: `photoshop-plugin/`
3. Start panel: `FlatMagic`
4. Ensure local service is running, then click `Ping` in the panel.

## Existing docs

- `Docs/project-brief.md`
- `Docs/working-memory.md`
- `Docs/paper-summary.md`
