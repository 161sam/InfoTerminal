#!/usr/bin/env bash
set -euo pipefail
TS=$(date +%Y%m%d_%H%M%S)
OUT=${1:-backups}
mkdir -p "$OUT"
FILE="$OUT/neo4j_$TS.dump"
CMD="docker exec neo4j neo4j-admin database dump neo4j --to=$FILE"
if [ "${DRY_RUN:-0}" = "1" ]; then
  echo "DRY_RUN: $CMD"
else
  echo "+ $CMD"
  eval "$CMD"
fi
