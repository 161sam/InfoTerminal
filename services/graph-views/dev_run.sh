#!/usr/bin/env bash
set -euo pipefail
export OTEL_SDK_DISABLED=1
export OTEL_TRACES_EXPORTER=none
export OTEL_METRICS_EXPORTER=none
export OTEL_LOGS_EXPORTER=none
unset OTEL_EXPORTER_OTLP_ENDPOINT OTEL_EXPORTER_OTLP_TRACES_ENDPOINT
cd "$(dirname "$0")"
set -a; [ -f ./.env.local ] && . ./.env.local; set +a
. .venv/bin/activate 2>/dev/null || true

PORT="${PORT:-8403}"
HOST="${HOST:-127.0.0.1}"
PG_HOST="${PG_HOST:-127.0.0.1}"
PG_PORT="${PG_PORT:-55432}"
PG_DB="${PG_DB:-it_graph}"
PG_USER="${PG_USER:-it_user}"
PG_PASSWORD="${PG_PASSWORD:-it_pass}"

echo "[graph-views] waiting for postgres ${PG_HOST}:${PG_PORT} ..."
for i in {1..60}; do
  (echo >/dev/tcp/${PG_HOST}/${PG_PORT}) >/dev/null 2>&1 && ok=1 || ok=0
  [ "$ok" = 1 ] && break
  sleep 1
done
if [ "${ok:-0}" != "1" ]; then
  echo "[graph-views] postgres not reachable, skipping start."
  exit 0
fi

export PG_HOST PG_PORT PG_DB PG_USER PG_PASSWORD
echo "[graph-views] starting on http://${HOST}:${PORT}"
exec uvicorn app:app --host "$HOST" --port "$PORT" --reload

