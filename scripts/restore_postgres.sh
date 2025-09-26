#!/usr/bin/env bash
set -euo pipefail
if [[ ${1:-} =~ ^(--help|-h)$ || $# -eq 0 ]]; then
  cat <<'USAGE'
Usage: restore_postgres.sh <sql-file>

Restores a plain SQL dump created by scripts/backup_postgres.sh into the
postgres service managed via docker compose. Compose files can be overridden by
setting IT_COMPOSE_FILES (comma-separated list) and IT_COMPOSE_PROJECT.
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

abs_file=$(cd "$(dirname "$FILE")" && pwd)/$(basename "$FILE")
remote_path="/tmp/restore_postgres.sql"

copy_cmd=(docker compose "${compose_args[@]}" cp "$abs_file" postgres:"$remote_path")
restore_cmd=(docker compose "${compose_args[@]}" exec -T postgres bash -c "psql -U postgres -v ON_ERROR_STOP=1 -f '$remote_path'")
cleanup_cmd=(docker compose "${compose_args[@]}" exec -T postgres rm -f "$remote_path")

run_cmd() {
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    printf 'DRY_RUN: %s\n' "$*"
  else
    printf '+ %s\n' "$*"
    "$@"
  fi
}

run_cmd "${copy_cmd[@]}"
if [[ "${DRY_RUN:-0}" != "1" ]]; then
  run_cmd "${restore_cmd[@]}"
  run_cmd "${cleanup_cmd[@]}" || true
  echo "Postgres restore completed from $FILE"
fi
