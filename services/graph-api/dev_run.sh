#!/usr/bin/env bash
set -euo pipefail

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8402}"

export NEO4J_URI="${NEO4J_URI:-bolt://127.0.0.1:7687}"
export NEO4J_USER="${NEO4J_USER:-neo4j}"
# Passwort in BEIDEN Variablen bereitstellen (Kompatibilität)
export NEO4J_PASSWORD="${NEO4J_PASSWORD:-${NEO4J_PASS:-test12345}}"
export NEO4J_PASS="${NEO4J_PASS:-$NEO4J_PASSWORD}"

# OpenTelemetry noise in local dev unbedingt aus
export OTEL_SDK_DISABLED=${OTEL_SDK_DISABLED:-1}
unset OTEL_EXPORTER_OTLP_ENDPOINT OTEL_TRACES_EXPORTER OTEL_METRICS_EXPORTER OTEL_LOGS_EXPORTER

# venv sicherstellen + Deps
if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
  . .venv/bin/activate
  python -m pip install -U pip wheel
  if [ -f requirements.txt ]; then
    pip install -r requirements.txt
  else
    pip install fastapi "uvicorn[standard]" neo4j pydantic httpx
  fi
else
  . .venv/bin/activate
fi

echo "[graph-api] Using Neo4j ENV:"
echo "NEO4J_URI=${NEO4J_URI}"
echo "NEO4J_USER=${NEO4J_USER}"
echo "NEO4J_PASSWORD=****"
echo "NEO4J_PASS=****"

# Warten bis Bolt bereit
for i in {1..60}; do (echo >/dev/tcp/127.0.0.1/7687) >/dev/null 2>&1 && break || sleep 1; done

exec python -m uvicorn app:app --host "${HOST}" --port "${PORT}" --reload
