#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: backup.sh [OPTIONS]

Co-ordinates backups for OpenSearch, Neo4j, and Postgres by calling the
service-specific scripts. Outputs a manifest describing the generated files.

Options:
  -o, --out DIR          Target directory for the backup run. Defaults to
                         artifacts/backup/<timestamp>.
  -s, --services LIST    Comma-separated subset of services (opensearch, neo4j,
                         postgres). Default: all services.
  -t, --timestamp TS     Reuse a fixed timestamp for all backup artefacts.
  -h, --help             Show this help text.

Environment:
  DRY_RUN=1              Print commands without executing them.
  IT_COMPOSE_FILES       Comma-separated docker compose files to use.
  IT_COMPOSE_PROJECT     docker compose project name.
USAGE
}

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
DEFAULT_SERVICES=(opensearch neo4j postgres)
TARGET_DIR=""
REQUESTED_SERVICES=()
CUSTOM_TIMESTAMP=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--out)
      TARGET_DIR=$2
      shift 2
      ;;
    -s|--services)
      IFS=',' read -r -a REQUESTED_SERVICES <<<"$2"
      shift 2
      ;;
    -t|--timestamp)
      CUSTOM_TIMESTAMP=$2
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ ${#REQUESTED_SERVICES[@]} -eq 0 ]]; then
  REQUESTED_SERVICES=(${DEFAULT_SERVICES[@]})
fi

for svc in "${REQUESTED_SERVICES[@]}"; do
  case "$svc" in
    opensearch|neo4j|postgres) ;;
    *)
      echo "Unsupported service: $svc" >&2
      exit 1
      ;;
  esac
done

TIMESTAMP=${CUSTOM_TIMESTAMP:-${IT_BACKUP_TIMESTAMP:-$(date +%Y%m%d_%H%M%S)}}
export IT_BACKUP_TIMESTAMP="$TIMESTAMP"

if [[ -z "$TARGET_DIR" ]]; then
  TARGET_DIR="artifacts/backup/$TIMESTAMP"
fi
mkdir -p "$TARGET_DIR"

manifest_tmp=$(mktemp)
trap 'rm -f "$manifest_tmp"' EXIT

declare -A service_extensions=(
  [opensearch]="tar.gz"
  [neo4j]="dump"
  [postgres]="sql"
)

for svc in "${REQUESTED_SERVICES[@]}"; do
  script="$SCRIPT_DIR/backup_${svc}.sh"
  if [[ ! -x "$script" ]]; then
    echo "Missing helper script: $script" >&2
    exit 1
  fi
  "$script" "$TARGET_DIR"
  ext=${service_extensions[$svc]}
  file="$TARGET_DIR/${svc}_${TIMESTAMP}.${ext}"
  if [[ "${DRY_RUN:-0}" != "1" && ! -f "$file" ]]; then
    echo "Expected backup artefact not found: $file" >&2
    exit 1
  fi
  printf '%s %s\n' "$svc" "$file" >>"$manifest_tmp"
  echo "✔ ${svc} backup complete" >&2
done

if [[ "${DRY_RUN:-0}" == "1" ]]; then
  echo "DRY_RUN active – manifest not written"
  exit 0
fi

manifest_path="$TARGET_DIR/backup-manifest.json"
python <<'PY' "$TARGET_DIR" "$manifest_tmp" "$manifest_path" "$TIMESTAMP"
import json
import os
import sys

target_dir, manifest_tmp, manifest_path, timestamp = sys.argv[1:5]
services = {}
with open(manifest_tmp, "r", encoding="utf-8") as handle:
    for line in handle:
        svc, path = line.rstrip("\n").split(" ", 1)
        services[svc] = os.path.relpath(path, target_dir)

with open(manifest_path, "w", encoding="utf-8") as handle:
    json.dump({"timestamp": timestamp, "services": services}, handle, indent=2)
    handle.write("\n")
PY

echo "Backup manifest written to $manifest_path"
