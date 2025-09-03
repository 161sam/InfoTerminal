#!/bin/bash
set -euo pipefail
TID=$(curl -s http://localhost:8085/nifi-api/process-groups/root/templates | \
  grep -o '"id":"[^"]*"[^}]*"name":"infoterminal_aleph_ingest"' | \
  head -n1 | sed 's/.*"id":"\([^"]*\)".*/\1/')
[ -z "$TID" ] && { echo "template not found" >&2; exit 1; }
curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"templateId":"'$TID'","originX":0,"originY":0}' \
  http://localhost:8085/nifi-api/process-groups/root/template-instance >/dev/null
