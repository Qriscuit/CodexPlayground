# FlatMagic Photoshop UXP Plugin (Prototype)

This folder contains a Photoshop UXP panel plugin that connects to a local FlatMagic Python service.

## What it does in v1

- Lists likely pixel layers from the active document.
- Sends layer pixels to `POST /v1/detect`.
- Shows proposed cleanup regions with confidence.
- Sends selected regions to `POST /v1/repair`.
- Applies repaired pixels to a duplicated non-destructive result layer.
- Supports session rollback and local audit export.

## Load in Photoshop (Developer mode)

1. Open Photoshop.
2. Open UXP Developer Tool.
3. Add plugin from this folder: `photoshop-plugin/`.
4. Start the plugin panel named `FlatMagic`.

## Service dependency

The plugin expects the local service at `http://127.0.0.1:8765` by default.

If your service runs on another port, set it in the panel `Service URL` field.
