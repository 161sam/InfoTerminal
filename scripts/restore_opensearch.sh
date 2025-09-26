#!/usr/bin/env bash
set -euo pipefail
if [[ ${1:-} =~ ^(--help|-h)$ || $# -eq 0 ]]; then
  cat <<'USAGE'
Usage: restore_opensearch.sh <archive>

Restores an OpenSearch data directory from a tar.gz archive created via
scripts/backup_opensearch.sh. The script stops the running opensearch service,
extracts the archive into the shared data volume using an ephemeral container,
and then restarts the service. Override compose files via IT_COMPOSE_FILES
(comma-separated) and IT_COMPOSE_PROJECT.
USAGE
  exit 0
fi

ARCHIVE=$1
if [[ ! -f "$ARCHIVE" ]]; then
  echo "File not found: $ARCHIVE" >&2
  exit 1
fi

read -r -a compose_files <<<"${IT_COMPOSE_FILES:-docker-compose.yml}"
compose_args=()
if [[ -n "${IT_COMPOSE_PROJECT:-}" ]]; then
  compose_args+=(-p "$IT_COMPOSE_PROJECT")
fi
for f in "${compose_files[@]}"; do
  compose_args+=(-f "$f")
done

abs_dir=$(cd "$(dirname "$ARCHIVE")" && pwd)
file_name=$(basename "$ARCHIVE")

stop_cmd=(docker compose "${compose_args[@]}" stop opensearch)
restore_cmd=(docker compose "${compose_args[@]}" run --rm --volume "$abs_dir:/backups:ro" opensearch bash -c "rm -rf /usr/share/opensearch/data/* && tar -xzf /backups/$file_name -C /usr/share/opensearch")
start_cmd=(docker compose "${compose_args[@]}" start opensearch)

run_cmd() {
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    printf 'DRY_RUN: %s\n' "$*"
  else
    printf '+ %s\n' "$*"
    "$@"
  fi
}

run_cmd "${stop_cmd[@]}"
if [[ "${DRY_RUN:-0}" != "1" ]]; then
  run_cmd "${restore_cmd[@]}"
  run_cmd "${start_cmd[@]}"
  echo "OpenSearch restore completed from $ARCHIVE"
fi
