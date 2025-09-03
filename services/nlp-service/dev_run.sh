#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Load local env if present
env_file=".env.local"
if [ -f "$env_file" ]; then
  set -a
  . "$env_file"
  set +a
fi

export OTEL_SDK_DISABLED=1
export OTEL_TRACES_EXPORTER=none
export OTEL_METRICS_EXPORTER=none
export OTEL_LOGS_EXPORTER=none
unset OTEL_EXPORTER_OTLP_ENDPOINT OTEL_EXPORTER_OTLP_TRACES_ENDPOINT

. .venv/bin/activate 2>/dev/null || true
exec uvicorn app:app --host 127.0.0.1 --port "${PORT:-8405}" --reload
