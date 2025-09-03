#!/bin/bash
set -euo pipefail
curl -s -X PUT -H 'Content-Type: application/json' \
  -d '{"id":"root","state":"RUNNING"}' \
  http://localhost:8085/nifi-api/flow/process-groups/root >/dev/null
