#!/usr/bin/env bash
set -euo pipefail

URL=${SUPERSET_URL:-http://localhost:8644}
USER=${SUP_USER:-admin}
PASS=${SUP_PASS:-adminadmin}

if ! curl -fsS "$URL/health" >/dev/null 2>&1; then
  echo "SKIP: Superset not reachable at $URL"; exit 0;
fi

echo "E2E: Superset importer"
SUPERSET_URL=$URL SUP_USER=$USER SUP_PASS=$PASS bash infra/analytics/superset/import_timeline.sh || {
  echo "FAIL: importer script"; exit 1;
}
echo "OK"

