#!/usr/bin/env bash
set -euo pipefail

checks=(
  "search-api:8401:/healthz"
  "graph-api:8402:/healthz"
  "graph-views:8403:/healthz"
  "entity-resolution:8404:/healthz"
  "doc-entities:8406:/healthz"
)
ok=0; fail=0

for item in "${checks[@]}"; do
  svc="${item%%:*}"
  rest="${item#*:}"
  port="${rest%%:*}"
  path="${rest#*:}"
  url="http://127.0.0.1:${port}${path}"
  if curl -sf "$url" >/dev/null; then
    printf "✓ %-17s %s\n" "$svc" "OK"
    ok=$((ok+1))
  else
    printf "✗ %-17s %s\n" "$svc" "FAIL"
    fail=$((fail+1))
  fi
done

# Frontend separater Health
if curl -sf "http://127.0.0.1:3411/api/health" >/dev/null; then
  printf "✓ %-17s %s\n" "frontend" "OK"
else
  printf "✗ %-17s %s\n" "frontend" "FAIL"
fi

echo "Summary: ${ok} OK, ${fail} FAIL"
