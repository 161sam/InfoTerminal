# Graph Views Service

This service exposes graph-related views via FastAPI.

## Development

Create a virtual environment and install the package in editable mode:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .
```

The editable install includes the asynchronous PostgreSQL driver `asyncpg` used by `db.py`.

For running tests install the dev requirements:

```bash
pip install -r requirements-dev.txt
```

Start the service during development with:

```bash
IT_FORCE_READY=1 uvicorn app:app --port 8403 --reload
```
