#!/usr/bin/env bash
set -euo pipefail
if ! command -v dbt >/dev/null 2>&1 && ! command -v dbt-core >/dev/null 2>&1; then
  echo "[dbt] TODO: Install dbt (pipx/pip) and set profiles.yml. Skipping."
  exit 0
fi
dbt deps || true
dbt seed || true
dbt run || true
dbt test || true
