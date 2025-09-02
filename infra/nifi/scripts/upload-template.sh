#!/usr/bin/env bash
set -euo pipefail
NIFI_URL=${NIFI_URL:-http://nifi.127.0.0.1.nip.io}
TEMPLATE=infra/nifi/templates/openbb_prices_template.xml

echo "→ Hole Root Process Group ID…"
ROOT_ID=$(curl -s "$NIFI_URL/nifi-api/process-groups/root" | jq -r .id)

echo "→ Lade Template hoch…"
curl -s -X POST "$NIFI_URL/nifi-api/process-groups/$ROOT_ID/templates/upload" \
  -H 'Content-Type: multipart/form-data' \
  -F "template=@$TEMPLATE" >/dev/null

echo "→ Liste Templates…"
TID=$(curl -s "$NIFI_URL/nifi-api/flow/templates" | jq -r '.templates[-1].id')

echo "→ Platziere Template…"
curl -s -X POST "$NIFI_URL/nifi-api/process-groups/$ROOT_ID/template-instance" \
  -H 'Content-Type: application/json' \
  -d "{\"templateId\":\"$TID\",\"originX\":0.0,\"originY\":0.0}" >/dev/null

echo "→ Starte alle Prozessoren…"
PG=$(curl -s "$NIFI_URL/nifi-api/process-groups/$ROOT_ID/process-groups" | jq -r '.processGroups[0].id // empty')
curl -s -X PUT "$NIFI_URL/nifi-api/flow/process-groups/$ROOT_ID" \
  -H 'Content-Type: application/json' \
  -d '{"id":"'"$ROOT_ID"'","state":"RUNNING"}' >/dev/null || true
echo "Fertig."
