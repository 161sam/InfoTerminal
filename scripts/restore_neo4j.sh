#!/usr/bin/env bash
set -euo pipefail
if [[ ${1:-} =~ ^(--help|-h)$ || $# -eq 0 ]]; then
  cat <<'USAGE'
Usage: restore_neo4j.sh <dump-file>

Restores a `.dump` archive created with scripts/backup_neo4j.sh. The script
stops the running neo4j service, loads the database using neo4j-admin in an
ephemeral container, and then restarts the service. Override compose files via
IT_COMPOSE_FILES (comma-separated) and IT_COMPOSE_PROJECT.
USAGE
  exit 0
fi

FILE=$1
if [[ ! -f "$FILE" ]]; then
  echo "File not found: $FILE" >&2
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

abs_dir=$(cd "$(dirname "$FILE")" && pwd)

stop_cmd=(docker compose "${compose_args[@]}" stop neo4j)
load_cmd=(docker compose "${compose_args[@]}" run --rm --volume "$abs_dir:/backups:ro" neo4j bash -c "neo4j-admin database load neo4j --from-path=/backups --overwrite-destination=true --force")
start_cmd=(docker compose "${compose_args[@]}" start neo4j)

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
  run_cmd "${load_cmd[@]}"
  run_cmd "${start_cmd[@]}"
  echo "Neo4j restore completed from $FILE"
fi
