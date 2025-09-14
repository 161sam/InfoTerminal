#!/usr/bin/env bash
set -euo pipefail
TS=$(date +%Y%m%d_%H%M%S)
OUT=${1:-backups}
mkdir -p "$OUT"
FILE="$OUT/opensearch_$TS.snapshot"
CMD="docker exec opensearch bash -c 'curl -XPUT localhost:9200/_snapshot/it_backup/$TS?wait_for_completion=true'"
if [ "${DRY_RUN:-0}" = "1" ]; then
  echo "DRY_RUN: $CMD"
else
  echo "+ $CMD"
  eval "$CMD"
fi
