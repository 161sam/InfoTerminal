#!/usr/bin/env bash
set -euo pipefail

API="${DOC_ENTITIES_URL:-http://127.0.0.1:8005}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
DOC_DIR="$ROOT_DIR/examples/docs"

echo "[seed-demo] sending example docs to doc-entities"
for f in "$DOC_DIR"/*; do
  title=$(basename "$f")
  payload=$(jq -Rs . <"$f")
  curl -s -X POST "$API/annotate" \
    -H 'Content-Type: application/json' \
    -d "{\"text\":$payload,\"title\":\"$title\"}" >/dev/null
  echo "  uploaded $title"
done

echo "[seed-demo] seeding example graph"
python "$ROOT_DIR/services/graph-api/scripts/seed_graph.py" >/dev/null

echo "[seed-demo] done"
