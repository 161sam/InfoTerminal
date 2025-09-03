#!/usr/bin/env bash
set -euo pipefail
export OTEL_SDK_DISABLED=1
export OTEL_TRACES_EXPORTER=none
export OTEL_METRICS_EXPORTER=none
export OTEL_LOGS_EXPORTER=none
cd "$(dirname "$0")"
set -a; [ -f ./.env.local ] && . ./.env.local; set +a
. .venv/bin/activate 2>/dev/null || true
exec uvicorn app:app --host 127.0.0.1 --port 8405 --reload
