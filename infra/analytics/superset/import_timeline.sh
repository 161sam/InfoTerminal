#!/usr/bin/env bash
set -euo pipefail

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
TOK=$(login | jq -r '.access_token // empty')
if [ -z "$TOK" ]; then echo "❌ Login failed"; exit 1; fi
AUTH="Authorization: Bearer $TOK"

echo "→ Searching dataset 'timeline_events'"
DS_JSON=$(curl -sS -H "$AUTH" "$URL/api/v1/dataset/?q=(filters:!((col:table_name,opr:eq,value:timeline_events)))")
DS_ID=$(echo "$DS_JSON" | jq -r '.result[]?.id' | head -n1)
if [ -z "$DS_ID" ] || [ "$DS_ID" = "null" ]; then
  echo "❌ Dataset 'timeline_events' not found. Please upload CSV first (infra/analytics/timeline_events.csv)."; exit 1;
fi

echo "→ Creating chart 'Timeline Table'"
CHART_PAY='{ "slice_name": "Timeline Table", "viz_type": "table", "datasource_id": '"$DS_ID"', "datasource_type": "table", "params": "{\"all_columns\":[\"timestamp\",\"entity\",\"type\",\"details\"]}" }'
CHART=$(curl -sS -H "$AUTH" -H 'Content-Type: application/json' -d "$CHART_PAY" "$URL/api/v1/chart/" )
CH_ID=$(echo "$CHART" | jq -r '.id // .result.id // empty')
if [ -z "$CH_ID" ]; then echo "❌ Chart create failed: $CHART"; exit 1; fi

echo "→ Creating dashboard 'Investigation Timeline'"
DASH_PAY='{ "dashboard_title": "Investigation Timeline", "published": true }'
DASH=$(curl -sS -H "$AUTH" -H 'Content-Type: application/json' -d "$DASH_PAY" "$URL/api/v1/dashboard/" )
DASH_ID=$(echo "$DASH" | jq -r '.id // .result.id // empty')
if [ -z "$DASH_ID" ]; then echo "❌ Dashboard create failed: $DASH"; exit 1; fi

echo "→ (Manual) Add chart $CH_ID to dashboard $DASH_ID via UI (API layout building omitted)"
echo "✅ Done. Open $URL/superset/dashboard/$DASH_ID/"

