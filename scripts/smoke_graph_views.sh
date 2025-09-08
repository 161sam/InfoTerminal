#!/usr/bin/env bash
set -euo pipefail

BASE="${BASE:-${1:-http://localhost:8403}}"
BOOT="${BOOT:-0}"

have_jq=1
command -v jq >/dev/null 2>&1 || have_jq=0

echo "Using base: $BASE (BOOT=$BOOT) jq=$have_jq"

kill_server() {
  if [[ -n "${SERVER_PID:-}" ]]; then
    echo "Stopping uvicorn (pid=$SERVER_PID)"
    kill "$SERVER_PID" || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
}
trap kill_server EXIT

req() {
  local url="$1"
  local method="${2:-GET}"
  local body="${3:-}"
  local auth="${4:-}"
  local tmp_h; tmp_h="$(mktemp)"
  local curl_args=(-sS -D "$tmp_h" -H 'Accept: application/json' -X "$method" "$url")
  [[ -n "$body" ]] && curl_args+=(-H 'Content-Type: application/json' --data "$body")
  [[ -n "$auth" ]] && curl_args+=(-u "$auth")
  local out; out="$(curl "${curl_args[@]}" || true)"
  local code; code="$(awk 'BEGIN{c=0} /^HTTP/{c=$2} END{print c}' "$tmp_h")"
  local ct; ct="$(awk 'BEGIN{IGNORECASE=1} /^Content-Type:/{sub(/\r$/,"" ); print $2}' "$tmp_h")"
  rm -f "$tmp_h"
  echo "---"
  echo "GET $url  => $code  (ct=${ct:-n/a})"
  if [[ "${ct:-}" == application/json* ]]; then
    if [[ "$have_jq" -eq 1 ]]; then
      echo "$out" | jq . || { echo "(non-fatal) jq failed to parse JSON body:"; echo "$out" | head -c 400; echo; }
    else
      echo "$out" | head -c 400; echo
    fi
  else
    echo "(non-JSON body, first 400 chars):"
    echo "$out" | head -c 400; echo
  fi
  return 0
}

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
req "${BASE}/graphs/view/ego?label=Person&key=id&value=alice&depth=1&limit=10"

echo "2) Write ohne Auth (erwartet 401/403)"
curl -sS -i -X POST "${BASE}/graphs/cypher?write=1" -H 'Content-Type: application/json' -d '{"stmt":"RETURN 1","params":{}}' | sed -n '1,12p'

echo "3) Rate-Limit (2/sec) – drei schnelle Writes"
for i in 1 2 3; do
  curl -sS -u "${GV_BASIC_USER:-dev}:${GV_BASIC_PASS:-devpass}" -X POST "${BASE}/graphs/cypher?write=1" \
    -H 'Content-Type: application/json' -d '{"stmt":"RETURN 1","params":{}}' -D - | sed -n '1,20p'
done

echo "4) Dossier Export"
req "${BASE}/graphs/export/dossier?label=Person&key=id&value=alice&depth=2"

