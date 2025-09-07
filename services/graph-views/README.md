# Graph Views Service

This service exposes graph-related views via FastAPI.

## Development

Create a virtual environment and install the package in editable mode:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .
```

Graph-Views initialisiert Postgres asynchron via `asyncpg`; die Abhängigkeit ist Bestandteil des Pakets.

For running tests install the dev requirements:

```bash
pip install -r requirements-dev.txt
```

Start the service during development with:

```bash
IT_FORCE_READY=1 uvicorn app:app --port 8403 --reload
```
