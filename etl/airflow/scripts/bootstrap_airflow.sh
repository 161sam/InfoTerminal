#!/usr/bin/env bash
set -euo pipefail

# Set Airflow Variables
airflow variables set OPENBB_API_KEY "${OPENBB_API_KEY:-}"
airflow variables set DBT_TARGET "${DBT_TARGET:-dev}"
airflow variables set SUPERSET_URL "${SUPERSET_URL:-http://superset.default.svc:8088}"
airflow variables set SUPERSET_TOKEN "${SUPERSET_TOKEN:-}"

# Example Connection (e.g., Postgres for dbt)
airflow connections add dbt_postgres \
  --conn-type=postgres \
  --conn-host="${DBT_PG_HOST:-postgres}" \
  --conn-login="${DBT_PG_USER:-user}" \
  --conn-password="${DBT_PG_PASSWORD:-password}" \
  --conn-schema="${DBT_PG_DB:-db}"
