#!/usr/bin/env bash
set -e
export PG_HOST=${PG_HOST:-localhost}
export PG_PORT=${PG_PORT:-5432}
export PG_DB=${PG_DB:-infoterminal}
export PG_USER=${PG_USER:-app}
export PG_PASS=${PG_PASS:-app}
uvicorn app:app --host 127.0.0.1 --port 8004 --reload
