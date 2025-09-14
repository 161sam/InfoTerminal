#!/usr/bin/env bash
set -euo pipefail
SNAP=${1:?snapshot id}
CMD="docker exec opensearch bash -c 'curl -XPOST localhost:9200/_snapshot/it_backup/$SNAP/_restore?wait_for_completion=true'"
if [ "${DRY_RUN:-0}" = "1" ]; then
  echo "DRY_RUN: $CMD"
else
  echo "+ $CMD"
  eval "$CMD"
fi
