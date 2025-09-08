#!/usr/bin/env bash
set -euo pipefail

BASE="${1:-http://localhost:8403}"
echo "Using base: $BASE"

echo "1) Ego (read, envelope)"
curl -s "${BASE}/graphs/view/ego?label=Person&key=id&value=alice&depth=1&limit=10" | jq '{ok, data: ( .data | {nodes:(.nodes|length), relationships:(.relationships|length)} ), counts}'

echo "2) Write ohne Auth (soll 401/403 sein)"
curl -s -i -X POST "${BASE}/graphs/cypher?write=1" -H 'Content-Type: application/json' -d '{"stmt":"RETURN 1","params":{}}' | sed -n '1,10p'

echo "3) Rate-Limit (2/sec) – drei schnelle Writes"
for i in 1 2 3; do
  curl -s -u "${GV_BASIC_USER:-dev}:${GV_BASIC_PASS:-devpass}" -X POST "${BASE}/graphs/cypher?write=1" \
    -H 'Content-Type: application/json' -d '{"stmt":"RETURN 1","params":{}}' -D - | sed -n '1,12p'
done

echo "4) Dossier Export"
curl -s "${BASE}/graphs/export/dossier?label=Person&key=id&value=alice&depth=2" | jq '{ok, n:(.data.nodes|length), m:(.data.edges|length)}'
