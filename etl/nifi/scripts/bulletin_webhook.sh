#!/usr/bin/env bash
set -euo pipefail
NIFI_URL="${NIFI_URL:-http://localhost:8080/nifi-api}"
WEBHOOK_URL="${WEBHOOK_URL:-}" # e.g., Slack or Teams webhook
LAST_TS="$(date +%s)000"

while true; do
  DATA=$(curl -fsS "${NIFI_URL}/flow/bulletin-board?after=${LAST_TS}") || { sleep 30; continue; }
  TS=$(echo "$DATA" | jq -r '.bulletinBoard.bulletins[-1].bulletin.timestamp' 2>/dev/null || echo "$LAST_TS")
  LAST_TS="$TS"
  MSG=$(echo "$DATA" | jq -r '.bulletinBoard.bulletins[] | select(.bulletin.level != "INFO") | .bulletin.message' 2>/dev/null)
  if [[ -n "$MSG" && -n "$WEBHOOK_URL" ]]; then
    curl -fsS -X POST -H 'Content-Type: application/json' -d "{\"text\":\"NiFi: $MSG\"}" "$WEBHOOK_URL" || true
  fi
  sleep 60
done
