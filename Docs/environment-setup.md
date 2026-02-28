# Environment Setup (v1)

Based on the current context in `Docs/working-memory.md`, we are starting with a **simple, conservative Python CLI prototype environment**.

## 1) Create a local virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2) Configure the first environment

```bash
cp .env.example .env
```

Default values:
- `APP_ENV=development`
- `APP_NAME=layer-aware-cleanup-prototype`

## 3) Run the first hello-world file

```bash
python3 src/hello_world.py
```

Expected output:

```text
Hello, world! layer-aware-cleanup-prototype is running in the development environment.
```
