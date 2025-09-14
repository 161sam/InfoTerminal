#!/usr/bin/env bash
set -euo pipefail
TS=$(date +%Y%m%d_%H%M%S)
OUT=${1:-backups}
mkdir -p "$OUT"
FILE="$OUT/postgres_$TS.sql"
CMD="docker exec postgres pg_dump -U postgres --format=plain --file=/tmp/dump.sql && docker cp postgres:/tmp/dump.sql $FILE"
if [ "${DRY_RUN:-0}" = "1" ]; then
  echo "DRY_RUN: $CMD"
else
  echo "+ $CMD"
  eval "$CMD"
fi
