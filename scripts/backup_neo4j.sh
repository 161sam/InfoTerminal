#!/usr/bin/env bash
set -euo pipefail
if [[ ${1:-} =~ ^(--help|-h)$ ]]; then
  cat <<'USAGE'
Usage: backup_neo4j.sh [output-directory]

Creates a database dump of the `neo4j` database by running neo4j-admin in an
ephemeral container that mounts the shared data volume. The output is a
`.dump` file compatible with scripts/restore_neo4j.sh. Override compose files
via IT_COMPOSE_FILES (comma-separated list) and the project name via
IT_COMPOSE_PROJECT.
USAGE
  exit 0
fi

TS=${IT_BACKUP_TIMESTAMP:-$(date +%Y%m%d_%H%M%S)}
OUT=${1:-backups}
mkdir -p "$OUT"
FILE="$OUT/neo4j_$TS.dump"

read -r -a compose_files <<<"${IT_COMPOSE_FILES:-docker-compose.yml}"
compose_args=()
if [[ -n "${IT_COMPOSE_PROJECT:-}" ]]; then
  compose_args+=(-p "$IT_COMPOSE_PROJECT")
fi
for f in "${compose_files[@]}"; do
  compose_args+=(-f "$f")
done

abs_out=$(cd "$OUT" && pwd)
dump_cmd=(docker compose "${compose_args[@]}" run --rm --volume "$abs_out:/backups" neo4j bash -c "neo4j-admin database dump neo4j --to-path=/backups --overwrite-destination=true && mv /backups/neo4j.dump /backups/neo4j_$TS.dump")

if [[ "${DRY_RUN:-0}" == "1" ]]; then
  printf 'DRY_RUN: %s\n' "${dump_cmd[*]}"
  exit 0
fi

printf '+ %s\n' "${dump_cmd[*]}"
"${dump_cmd[@]}"
printf 'Neo4j backup written to %s\n' "$FILE"
