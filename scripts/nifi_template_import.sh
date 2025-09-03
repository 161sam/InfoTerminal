#!/bin/bash
set -euo pipefail
curl -s -F template=@etl/nifi/templates/infoterminal_aleph_ingest.xml \
  http://localhost:8085/nifi-api/process-groups/root/templates/upload >/dev/null
