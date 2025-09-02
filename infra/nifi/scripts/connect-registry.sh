#!/usr/bin/env bash
set -euo pipefail
NIFI=${NIFI:-http://nifi.127.0.0.1.nip.io}
REG=${REG:-http://nifi-registry.127.0.0.1.nip.io}

echo "→ Get Root Group ID"
ROOT=$(curl -s "$NIFI/nifi-api/process-groups/root" | jq -r .id)

echo "→ Add Registry Client"
REG_ID=$(curl -s -X POST "$NIFI/nifi-api/controller/registry-clients" \
  -H 'Content-Type: application/json' \
  -d '{"revision":{"version":0},"component":{"name":"local-reg","uri":"'"$REG"'/nifi-registry"}}' | jq -r '.id')

echo "→ Create Bucket in Registry (if not exists)"
# NiFi Registry has its own API; create a bucket named 'flows' if none exists
curl -s -X POST "$REG/nifi-registry-api/buckets" -H 'Content-Type: application/json' \
  -d '{"name":"flows"}' >/dev/null || true

echo "→ Done. You can now start versioning Process Groups from the NiFi UI."
