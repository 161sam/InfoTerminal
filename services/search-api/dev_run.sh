#!/usr/bin/env bash
cd "$(dirname "$0")"
. .venv/bin/activate
exec uvicorn app:app --host 127.0.0.1 --port 8401 --reload
