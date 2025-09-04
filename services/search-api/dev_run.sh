#!/usr/bin/env bash
set -euo pipefail

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8401}"

if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
  . .venv/bin/activate
  python -m pip install -U pip wheel
  if [ -f requirements.txt ]; then
    pip install -r requirements.txt
  else
    pip install fastapi "uvicorn[standard]" opensearch-py httpx pydantic
  fi
else
  . .venv/bin/activate
fi

exec python -m uvicorn app.main:app --host "${HOST}" --port "${PORT}" --reload
