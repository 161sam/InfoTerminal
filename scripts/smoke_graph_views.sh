#!/usr/bin/env bash
set -euo pipefail

BASE="${BASE:-${1:-http://localhost:8403}}"
BOOT="${BOOT:-0}"

echo "Using base: $BASE (BOOT=$BOOT)"

kill_server() {
  if [[ -n "${SERVER_PID:-}" ]]; then
    echo "Stopping uvicorn (pid=$SERVER_PID)"
    kill "$SERVER_PID" || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
}
trap kill_server EXIT

if [[ "$BOOT" == "1" ]]; then
  echo "Booting local graph-views via uvicorn..."
  pushd services/graph-views >/dev/null
  : "${GV_ALLOW_WRITES:=1}"
  : "${GV_BASIC_USER:=dev}"
  : "${GV_BASIC_PASS:=devpass}"
  : "${GV_RATE_LIMIT_WRITE:=2/second}"
  : "${GV_AUDIT_LOG:=1}"
  .venv/bin/uvicorn app:app --host 0.0.0.0 --port 8403 --reload >/tmp/gv.dev.log 2>&1 &
  SERVER_PID=$!
  popd >/dev/null

  echo "Waiting for /healthz ..."
  for i in {1..50}; do
    if curl -sf "${BASE}/healthz" >/dev/null; then
      echo "Service healthy."
      break
    fi
    sleep 0.2
  done
fi

echo "1) Ego (read, envelope)"
curl -s "${BASE}/graphs/view/ego?label=Person&key=id&value=alice&depth=1&limit=10" | jq '{ok, data: ( .data | {nodes:(.nodes|length), relationships:(.relationships|length)} ), counts}'

echo "2) Write ohne Auth (soll 401/403 sein)"
curl -s -i -X POST "${BASE}/graphs/cypher?write=1" -H 'Content-Type: application/json' -d '{"stmt":"RETURN 1","params":{}}' | sed -n '1,10p'

echo "3) Rate-Limit (2/sec) – drei schnelle Writes"
for i in 1 2 3; do
  curl -s -u "${GV_BASIC_USER:-dev}:${GV_BASIC_PASS:-devpass}" -X POST "${BASE}/graphs/cypher?write=1" \
    -H 'Content-Type: application/json' -d '{"stmt":"RETURN 1","params":{}}' -D - | sed -n '1,15p'
done

echo "4) Dossier Export"
curl -s "${BASE}/graphs/export/dossier?label=Person&key=id&value=alice&depth=2" | jq '{ok, n:(.data.nodes|length), m:(.data.edges|length)}'

