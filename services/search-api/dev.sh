#!/usr/bin/env bash
set -e
export OS_URL=${OS_URL:-http://localhost:9200}
uvicorn app:app --host 127.0.0.1 --port 8001 --reload
