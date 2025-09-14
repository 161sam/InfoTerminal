#!/usr/bin/env bash
set -euo pipefail
FILE=${1:?sql file}
CMD="docker cp $FILE postgres:/tmp/restore.sql && docker exec postgres psql -U postgres -f /tmp/restore.sql"
if [ "${DRY_RUN:-0}" = "1" ]; then
  echo "DRY_RUN: $CMD"
else
  echo "+ $CMD"
  eval "$CMD"
fi
