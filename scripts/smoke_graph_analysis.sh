#!/usr/bin/env bash
# Smoke test for graph-api analysis endpoints.
# Usage: GRAPH_ANALYSIS_BASE=http://localhost:8612 scripts/smoke_graph_analysis.sh
set -euo pipefail

BASE="${GRAPH_ANALYSIS_BASE:-${1:-http://localhost:8612}}"
START_NODE="${GRAPH_SMOKE_START:-p1}"
END_NODE="${GRAPH_SMOKE_END:-p2}"
CENTER_NODE="${GRAPH_SMOKE_CENTER:-$START_NODE}"
MAX_LENGTH="${GRAPH_SMOKE_MAXLEN:-6}"
LIMIT="${GRAPH_SMOKE_LIMIT:-5}"

have_jq=1
if ! command -v jq >/dev/null 2>&1; then
  have_jq=0
fi

info() { printf '\n→ %s\n' "$*"; }
fail() { echo "❌ $*" >&2; exit 1; }

check_health() {
  info "Checking graph-api health at ${BASE}/healthz"
  if ! curl -sSf "${BASE}/healthz" >/dev/null 2>&1; then
    fail "graph-api health check failed at ${BASE}/healthz"
  fi
  echo "✅ graph-api reachable"
}

call_api() {
  local description="$1"
  local method="$2"
  local path="$3"
  local payload="${4:-}"
  local url="${BASE}${path}"

  info "${description} (${url})"
  local response
  if [[ -n "$payload" ]]; then
    response=$(curl -sS -w '\n%{http_code}' -H 'Accept: application/json' -H 'Content-Type: application/json' -X "$method" --data "$payload" "$url") || fail "curl failed for ${url}"
  else
    response=$(curl -sS -w '\n%{http_code}' -H 'Accept: application/json' -X "$method" "$url") || fail "curl failed for ${url}"
  fi

  local status="${response##*$'\n'}"
  local body="${response%$'\n'$status}"

  if [[ "$status" != "200" ]]; then
    echo "$body"
    fail "HTTP ${status} for ${url}"
  fi

  if [[ $have_jq -eq 1 ]]; then
    echo "$body" | jq '.'
  else
    echo "$body"
  fi

  RESPONSE_BODY="$body"
}

ensure_field() {
  local expr="$1"
  local message="$2"
  if [[ $have_jq -eq 1 ]]; then
    echo "$RESPONSE_BODY" | jq -e "$expr" >/dev/null 2>&1 || fail "$message"
  else
    [[ "$RESPONSE_BODY" == *"$message"* ]] || fail "$message"
  fi
}

check_health

call_api "Degree centrality" "GET" "/graphs/analysis/degree?limit=${LIMIT}&offset=0"
ensure_field '.algorithm == "degree"' "degree response missing algorithm"
ensure_field '.results | length > 0' "degree response empty"

call_api "Louvain communities" "GET" "/graphs/analysis/communities?min_size=1&limit=${LIMIT}"
ensure_field '.community_count >= 0' "community response missing count"

call_api "Shortest path" "POST" "/graphs/analysis/shortest-path" "{\"start_node_id\":\"${START_NODE}\",\"end_node_id\":\"${END_NODE}\",\"max_length\":${MAX_LENGTH}}"
ensure_field '.path_found == true or .path_found == false' "shortest path response missing path_found"

call_api "Subgraph export (markdown)" "GET" "/graphs/analysis/subgraph-export?center_id=${CENTER_NODE}&format=markdown&radius=2&limit=50"
ensure_field '.markdown' "subgraph export missing markdown"

echo "\n✅ Graph analysis smoke checks completed successfully."
