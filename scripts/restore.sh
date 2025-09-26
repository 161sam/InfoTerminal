#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: restore.sh [OPTIONS]

Restores OpenSearch, Neo4j, and Postgres from a backup directory or manifest by
calling the service-specific restore scripts.

Options:
  -p, --path DIR         Directory that holds the backup artefacts
                         (default: latest subdirectory in artifacts/backup).
  -m, --manifest FILE    Explicit path to a backup-manifest.json.
  -s, --services LIST    Comma-separated subset of services (opensearch, neo4j,
                         postgres). Default: all services found in the manifest.
  -h, --help             Show this help text.

Environment:
  DRY_RUN=1              Print commands without executing them.
  IT_COMPOSE_FILES       Comma-separated docker compose files to use.
  IT_COMPOSE_PROJECT     docker compose project name.
USAGE
}

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
DEFAULT_SERVICES=(opensearch neo4j postgres)
BACKUP_ROOT="artifacts/backup"
BACKUP_DIR=""
MANIFEST_FILE=""
REQUESTED_SERVICES=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--path)
      BACKUP_DIR=$2
      shift 2
      ;;
    -m|--manifest)
      MANIFEST_FILE=$2
      shift 2
      ;;
    -s|--services)
      IFS=',' read -r -a REQUESTED_SERVICES <<<"$2"
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

find_latest_backup_dir() {
  local root=$1
  find "$root" -mindepth 1 -maxdepth 1 -type d -printf '%T@ %p\n' \
    | sort -nr | head -n1 | cut -d' ' -f2-
}

if [[ -z "$BACKUP_DIR" ]]; then
  if [[ ! -d "$BACKUP_ROOT" ]]; then
    echo "No backup directory supplied and $BACKUP_ROOT does not exist" >&2
    exit 1
  fi
  BACKUP_DIR=$(find_latest_backup_dir "$BACKUP_ROOT")
  if [[ -z "$BACKUP_DIR" ]]; then
    echo "No backup directories found under $BACKUP_ROOT" >&2
    exit 1
  fi
else
  if [[ ! -d "$BACKUP_DIR" ]]; then
    echo "Backup path is not a directory: $BACKUP_DIR" >&2
    exit 1
  fi
fi

if [[ -z "$MANIFEST_FILE" ]]; then
  MANIFEST_FILE="$BACKUP_DIR/backup-manifest.json"
fi

if [[ -f "$MANIFEST_FILE" ]]; then
  MANIFEST_FILE=$(cd "$(dirname "$MANIFEST_FILE")" && pwd)/$(basename "$MANIFEST_FILE")
  BACKUP_DIR=$(dirname "$MANIFEST_FILE")
else
  BACKUP_DIR=$(cd "$BACKUP_DIR" && pwd)
fi

declare -A service_extensions=(
  [opensearch]="tar.gz"
  [neo4j]="dump"
  [postgres]="sql"
)

resolve_from_manifest() {
  local manifest=$1
  local service=$2
  python <<'PY' "$manifest" "$service"
import json
import os
import sys

manifest_path, service = sys.argv[1:3]
with open(manifest_path, "r", encoding="utf-8") as handle:
    data = json.load(handle)
services = data.get("services", {})
if service not in services:
    raise SystemExit(1)
print(services[service])
PY
}

resolve_backup_file() {
  local service=$1
  local manifest=$2
  local dir=$3
  local rel
  if [[ -f "$manifest" ]]; then
    if rel=$(resolve_from_manifest "$manifest" "$service" 2>/dev/null); then
      printf '%s/%s' "$dir" "$rel"
      return 0
    fi
  fi
  local ext=${service_extensions[$service]}
  local candidate=$(ls -1t "$dir"/${service}_*.${ext} 2>/dev/null | head -n1 || true)
  if [[ -n "$candidate" ]]; then
    printf '%s' "$candidate"
    return 0
  fi
  return 1
}

if [[ ${#REQUESTED_SERVICES[@]} -eq 0 ]]; then
  if [[ -f "$MANIFEST_FILE" ]]; then
    mapfile -t REQUESTED_SERVICES < <(python <<'PY' "$MANIFEST_FILE"
import json
import sys
with open(sys.argv[1], "r", encoding="utf-8") as handle:
    data = json.load(handle)
print("\n".join(sorted(data.get("services", {}).keys())))
PY
)
  else
    REQUESTED_SERVICES=(${DEFAULT_SERVICES[@]})
  fi
fi

if [[ ${#REQUESTED_SERVICES[@]} -eq 0 ]]; then
  echo "No services requested for restore" >&2
  exit 1
fi

for svc in "${REQUESTED_SERVICES[@]}"; do
  if [[ -z ${service_extensions[$svc]:-} ]]; then
    echo "Unsupported service: $svc" >&2
    exit 1
  fi
done

declare -A resolved_files=()
for svc in "${REQUESTED_SERVICES[@]}"; do
  file=$(resolve_backup_file "$svc" "$MANIFEST_FILE" "$BACKUP_DIR") || {
    echo "Unable to locate backup artefact for $svc in $BACKUP_DIR" >&2
    exit 1
  }
  if [[ ! -f "$file" ]]; then
    echo "Backup artefact missing: $file" >&2
    exit 1
  fi
  resolved_files[$svc]=$file
  echo "Using $file for $svc"
done

for svc in "${REQUESTED_SERVICES[@]}"; do
  script="$SCRIPT_DIR/restore_${svc}.sh"
  if [[ ! -x "$script" ]]; then
    echo "Missing helper script: $script" >&2
    exit 1
  fi
  "$script" "${resolved_files[$svc]}"
  echo "✔ ${svc} restore triggered"
done

echo "Restore completed for: ${REQUESTED_SERVICES[*]}"
