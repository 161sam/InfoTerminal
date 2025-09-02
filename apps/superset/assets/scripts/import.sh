#!/usr/bin/env bash
set -euo pipefail

SUPERTSET_URL="${SUPERTSET_URL:-http://localhost:8088}"
SUPERTSET_TOKEN="${SUPERTSET_TOKEN:-}" 
ASSETS_DIR="$(dirname "$0")/.."

if [[ -z "$SUPERTSET_TOKEN" ]]; then
  echo "SUPERTSET_TOKEN env var required" >&2
  exit 1
fi

for kind in datasets charts dashboard; do
  dir="$ASSETS_DIR/$kind"
  if [[ -d "$dir" ]]; then
    for file in "$dir"/*; do
      echo "Importing $file"
      curl -sf -X POST "$SUPERTSET_URL/api/v1/assets/import" \
        -H "Authorization: Bearer $SUPERTSET_TOKEN" \
        -F "formData=@$file" \
        || echo "Failed to import $file"
    done
  fi
  done
