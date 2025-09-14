#!/usr/bin/env bash
set -euo pipefail
FILE=${1:?dump file}
CMD="docker exec neo4j neo4j-admin database load neo4j --from=$FILE --force"
if [ "${DRY_RUN:-0}" = "1" ]; then
  echo "DRY_RUN: $CMD"
else
  echo "+ $CMD"
  eval "$CMD"
fi
