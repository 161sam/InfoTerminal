#!/usr/bin/env bash
set -euo pipefail
TS=${IT_BACKUP_TIMESTAMP:-$(date +%Y%m%d_%H%M%S)}
OUT=${1:-backups}

usage() {
  cat <<'USAGE'
Usage: backup_postgres.sh [output-directory]

Creates a plain-text Postgres dump with DROP statements that can be restored
via scripts/restore_postgres.sh. The script uses docker compose to locate the
running postgres service. Override the compose files via IT_COMPOSE_FILES
(comma-separated) and the project name via IT_COMPOSE_PROJECT.
USAGE
}

if [[ "${1:-}" =~ ^(--help|-h)$ ]]; then
  usage
  exit 0
fi

mkdir -p "$OUT"
FILE="$OUT/postgres_$TS.sql"

read -r -a compose_files <<<"${IT_COMPOSE_FILES:-docker-compose.yml}"
compose_args=()
if [[ -n "${IT_COMPOSE_PROJECT:-}" ]]; then
  compose_args+=(-p "$IT_COMPOSE_PROJECT")
fi
for f in "${compose_files[@]}"; do
  compose_args+=(-f "$f")
done

tmp_path="/tmp/postgres_backup_$TS.sql"
dump_cmd=(docker compose "${compose_args[@]}" exec -T postgres pg_dump -U postgres --clean --if-exists --format=plain --file "$tmp_path")
copy_cmd=(docker compose "${compose_args[@]}" cp postgres:"$tmp_path" "$FILE")
cleanup_cmd=(docker compose "${compose_args[@]}" exec -T postgres rm -f "$tmp_path")

run_cmd() {
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    printf 'DRY_RUN: %s\n' "$*"
  else
    printf '+ %s\n' "$*"
    "$@"
  fi
}

run_cmd "${dump_cmd[@]}"
if [[ "${DRY_RUN:-0}" != "1" ]]; then
  run_cmd "${copy_cmd[@]}"
  run_cmd "${cleanup_cmd[@]}" || true
  printf 'Postgres backup written to %s\n' "$FILE"
fi
