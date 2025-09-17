#!/usr/bin/env bash
set -euo pipefail

retry() {
  local n=0 max=${2:-8} delay=${3:-2}
  until [ $n -ge $max ]; do
    eval "$1" && return 0 || true
    n=$((n+1)); sleep $delay
  done
  eval "$1"  # final attempt (let it fail)
}

# Minimal Superset importer: creates a dashboard and a basic chart referencing an existing dataset
# Prereq: Create dataset from CSV (timeline_events.csv) via UI or API.
# Env: SUPERSET_URL (default http://localhost:8644), SUP_USER, SUP_PASS

URL=${SUPERSET_URL:-http://localhost:8644}
USER=${SUP_USER:-admin}
PASS=${SUP_PASS:-adminadmin}

login() {
  curl -sS -X POST "$URL/api/v1/security/login" \
    -H 'Content-Type: application/json' \
    -d '{"username":"'"$USER"'","password":"'"$PASS"'","provider":"db","refresh":true}'
}

echo "→ Logging in to $URL as $USER"
TOK=$(retry "login" 5 2 | jq -r '.access_token // empty')
if [ -z "$TOK" ]; then echo "❌ Login failed"; exit 1; fi
AUTH="Authorization: Bearer $TOK"

CSV_PATH=${CSV_PATH:-infra/analytics/timeline_events.csv}
if [ ! -f "$CSV_PATH" ]; then echo "❌ CSV not found at $CSV_PATH"; exit 1; fi

echo "→ Ensuring Postgres has table 'timeline_events' (docker compose required)"
if docker compose ps postgres >/dev/null 2>&1; then
  docker compose cp "$CSV_PATH" postgres:/tmp/timeline_events.csv
  docker compose exec -T postgres bash -lc "psql -U \
    ${POSTGRES_USER:-it_user} -d ${POSTGRES_DB:-it_graph} -v ON_ERROR_STOP=1 -c \"CREATE TABLE IF NOT EXISTS timeline_events (timestamp timestamptz, entity text, type text, details text); TRUNCATE timeline_events; COPY timeline_events (timestamp, entity, type, details) FROM '/tmp/timeline_events.csv' WITH (FORMAT csv, HEADER true);\""
else
  echo "⚠️ docker compose postgres not found; skipping DB import. Ensure the table exists."
fi

echo "→ Ensure Superset Database connection to Postgres"
DBS=$(retry "curl -sS -H \"$AUTH\" \"$URL/api/v1/database/\"" 5 2)
DB_ID=$(echo "$DBS" | jq -r '.result[] | select(.database_name=="it_postgres") | .id' | head -n1)
if [ -z "$DB_ID" ] || [ "$DB_ID" = "null" ]; then
  NEWDB='{ "database_name":"it_postgres", "sqlalchemy_uri":"postgresql+psycopg2://'"${POSTGRES_USER:-it_user}"':'"${POSTGRES_PASSWORD:-it_pass}"'@postgres:5432/'"${POSTGRES_DB:-it_graph}"'", "expose_in_sqllab":true, "allow_csv_upload":true }'
  RESP=$(retry "curl -sS -H \"$AUTH\" -H 'Content-Type: application/json' -d \"$NEWDB\" \"$URL/api/v1/database/\"" 5 2)
  DB_ID=$(echo "$RESP" | jq -r '.id // .result.id // empty')
fi
if [ -z "$DB_ID" ] || [ "$DB_ID" = "null" ]; then echo "❌ Could not create/find Superset DB"; exit 1; fi

echo "→ Creating/Fetching dataset 'timeline_events'"
DS_JSON=$(retry "curl -sS -H \"$AUTH\" \"$URL/api/v1/dataset/?q=(filters:!((col:table_name,opr:eq,value:timeline_events)))\"" 5 2)
DS_ID=$(echo "$DS_JSON" | jq -r '.result[]?.id' | head -n1)
if [ -z "$DS_ID" ] || [ "$DS_ID" = "null" ]; then
  PAY='{ "database": '"$DB_ID"', "schema": "public", "table_name": "timeline_events" }'
  RESP=$(retry "curl -sS -H \"$AUTH\" -H 'Content-Type: application/json' -d \"$PAY\" \"$URL/api/v1/dataset/\"" 5 2)
  DS_ID=$(echo "$RESP" | jq -r '.id // .result.id // empty')
fi
if [ -z "$DS_ID" ] || [ "$DS_ID" = "null" ]; then echo "❌ Could not create dataset"; exit 1; fi

# Create charts
echo "→ Creating chart 'Timeline Table'"
CHART_PAY='{ "slice_name": "Timeline Table", "viz_type": "table", "datasource_id": '"$DS_ID"', "datasource_type": "table", "params": "{\"all_columns\":[\"timestamp\",\"entity\",\"type\",\"details\"]}" }'
CHART=$(retry "curl -sS -H \"$AUTH\" -H 'Content-Type: application/json' -d \"$CHART_PAY\" \"$URL/api/v1/chart/\"" 5 2)
CH_ID=$(echo "$CHART" | jq -r '.id // .result.id // empty')
if [ -z "$CH_ID" ]; then echo "❌ Chart create failed: $CHART"; exit 1; fi

echo "→ Creating chart 'Timeline Series'"
SERIES_PAY='{ "slice_name": "Timeline Series", "viz_type": "echarts_timeseries_line", "datasource_id": '"$DS_ID"', "datasource_type": "table", "params": "{\"time_grain_sqla\":null,\"time_range\":\"No filter\",\"x_axis\":\"timestamp\",\"metrics\":[{\"label\":\"count\"}],\"query_mode\":\"aggregate\",\"groupby\":[\"type\"]}" }'
SERIES=$(retry "curl -sS -H \"$AUTH\" -H 'Content-Type: application/json' -d \"$SERIES_PAY\" \"$URL/api/v1/chart/\"" 5 2)
SERIES_ID=$(echo "$SERIES" | jq -r '.id // .result.id // empty')
if [ -z "$SERIES_ID" ]; then echo "❌ Series chart create failed: $SERIES"; exit 1; fi

echo "→ Creating dashboard 'Investigation Timeline'"
DASH_PAY='{ "dashboard_title": "Investigation Timeline", "published": true }'
DASH=$(curl -sS -H "$AUTH" -H 'Content-Type: application/json' -d "$DASH_PAY" "$URL/api/v1/dashboard/" )
DASH_ID=$(echo "$DASH" | jq -r '.id // .result.id // empty')
if [ -z "$DASH_ID" ]; then echo "❌ Dashboard create failed: $DASH"; exit 1; fi

# Build a simple layout with both charts
ROOT=ROOT_ID
GRID=GRID_ID
ROW1=ROW_ID_1
ROW2=ROW_ID_2
CH1=CHART_$CH_ID
CH2=CHART_$SERIES_ID
POS=$(cat <<JSON
{
  "DASHBOARD_VERSION_KEY": "v2",
  "$ROOT": {"id":"$ROOT","type":"ROOT","children":["$GRID"]},
  "$GRID": {"id":"$GRID","type":"GRID","children":["$ROW1","$ROW2"]},
  "$ROW1": {"id":"$ROW1","type":"ROW","children":["$CH1"],"meta":{"background":"BACKGROUND_TRANSPARENT"}},
  "$ROW2": {"id":"$ROW2","type":"ROW","children":["$CH2"],"meta":{"background":"BACKGROUND_TRANSPARENT"}},
  "$CH1": {"id":"$CH1","type":"CHART","children":[],"meta":{"width":12,"height":24,"chartId":$CH_ID}},
  "$CH2": {"id":"$CH2","type":"CHART","children":[],"meta":{"width":12,"height":24,"chartId":$SERIES_ID}}
}
JSON
)

echo "→ Updating dashboard layout"
retry "curl -sS -H \"$AUTH\" -H 'Content-Type: application/json' -X PUT -d '{\\\"position_json\\\": '\"$POS\"'}' \"$URL/api/v1/dashboard/$DASH_ID\" >/dev/null" 5 2

echo "✅ Done. Open $URL/superset/dashboard/$DASH_ID/"
