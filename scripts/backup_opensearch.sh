#!/usr/bin/env bash
set -euo pipefail
if [[ ${1:-} =~ ^(--help|-h)$ ]]; then
  cat <<'USAGE'
Usage: backup_opensearch.sh [output-directory]

Creates a tar.gz archive of the OpenSearch data directory by running an
ephemeral container that shares the service volume. The resulting archive is
compatible with scripts/restore_opensearch.sh. Override compose files with
IT_COMPOSE_FILES (comma-separated) and IT_COMPOSE_PROJECT.
USAGE
  exit 0
fi

TS=${IT_BACKUP_TIMESTAMP:-$(date +%Y%m%d_%H%M%S)}
OUT=${1:-backups}
mkdir -p "$OUT"
FILE="$OUT/opensearch_$TS.tar.gz"

read -r -a compose_files <<<"${IT_COMPOSE_FILES:-docker-compose.yml}"
compose_args=()
if [[ -n "${IT_COMPOSE_PROJECT:-}" ]]; then
  compose_args+=(-p "$IT_COMPOSE_PROJECT")
fi
for f in "${compose_files[@]}"; do
  compose_args+=(-f "$f")
done

abs_out=$(cd "$OUT" && pwd)
dump_cmd=(docker compose "${compose_args[@]}" run --rm --volume "$abs_out:/backups" opensearch bash -c "tar -czf /backups/opensearch_$TS.tar.gz -C /usr/share/opensearch data")

if [[ "${DRY_RUN:-0}" == "1" ]]; then
  printf 'DRY_RUN: %s\n' "${dump_cmd[*]}"
  exit 0
fi

printf '+ %s\n' "${dump_cmd[*]}"
"${dump_cmd[@]}"
printf 'OpenSearch backup written to %s\n' "$FILE"
