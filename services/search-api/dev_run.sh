#!/usr/bin/env bash
set -a
[ -f ./.env.local ] && . ./.env.local
set +a
export OTEL_SDK_DISABLED=true
export OTEL_TRACES_EXPORTER=none
export OTEL_METRICS_EXPORTER=none
export OTEL_LOGS_EXPORTER=none
export OTEL_PYTHON_DISABLED_INSTRUMENTATIONS="*"
unset OTEL_EXPORTER_OTLP_ENDPOINT OTEL_EXPORTER_OTLP_TRACES_ENDPOINT
cd "$(dirname "$0")"
set -a
[ -f ./.env.local ] && . ./.env.local
set +a
. .venv/bin/activate
exec uvicorn app:app --host 127.0.0.1 --port 8401 --reload
