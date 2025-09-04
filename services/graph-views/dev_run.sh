#!/usr/bin/env bash
set -euo pipefail
HOST="${HOST:-127.0.0.1}"; PORT="${PORT:-8403}"
PG_HOST="${PG_HOST:-127.0.0.1}"; PG_PORT="${PG_PORT:-5432}"
PG_DB="${PG_DB:-it_graph}"; PG_USER="${PG_USER:-it_user}"; PG_PASSWORD="${PG_PASSWORD:-it_pass}"

# venv + Deps
if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
  . .venv/bin/activate
  python -m pip install -U pip wheel
  if [ -f requirements.txt ]; then
    pip install -r requirements.txt
  else
    pip install fastapi "uvicorn[standard]" psycopg2-binary sqlalchemy pydantic
  fi
else
  . .venv/bin/activate
fi

echo "[graph-views] waiting for postgres ${PG_HOST}:${PG_PORT} ..."
for i in {1..60}; do (echo >/dev/tcp/${PG_HOST}/${PG_PORT}) >/dev/null 2>&1 && break || sleep 1; done

export PG_HOST PG_PORT PG_DB PG_USER PG_PASSWORD

# Target automatisch wählen
TARGET="app.main:app"
[ -f app.py ] && TARGET="app:app"

exec python -m uvicorn "$TARGET" --host "$HOST" --port "$PORT" --reload
