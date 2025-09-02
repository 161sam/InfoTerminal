#!/usr/bin/env bash
set -euo pipefail
NIFI_URL="${NIFI_URL:-http://localhost:8080/nifi-api}"
TEMPLATE="etl/nifi/templates/aleph_ingest_watchfolder.xml"
PG_ROOT_ID="${PG_ROOT_ID:-root}"
PARAM_CTX_NAME="${PARAM_CTX_NAME:-aleph-ingest}"

# 1) Template hochladen
TID=$(curl -fsS -X POST -H "Content-Type: application/xml" \
  --data-binary @"${TEMPLATE}" "${NIFI_URL}/process-groups/${PG_ROOT_ID}/templates/upload" \
  | jq -r '.template.id')

# 2) Parameter Context erstellen/aktualisieren (vereinfacht; in echt via ParamContext API)
# -> optional: hier nur Hinweis ausgeben
echo "Template uploaded: ${TID}"

# 3) Template auf Canvas instantiieren
curl -fsS -X POST -H "Content-Type: application/json" \
  -d "{\"templateId\":\"${TID}\",\"originX\":0,\"originY\":0}" \
  "${NIFI_URL}/process-groups/${PG_ROOT_ID}/template-instance"

echo "NiFi template instantiated. Open NiFi UI to bind Parameter Context and start processors."
