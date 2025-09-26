#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: backup_restore_synthetic.sh [--timestamp TS]

Runs a synthetic backup/restore validation across OpenSearch, Neo4j, and
Postgres. Inserts a tiny dataset, triggers scripts/backup.sh and
scripts/restore.sh, and verifies that the data reappears afterwards.

Environment:
  IT_COMPOSE_FILES    Comma-separated docker compose files (default: docker-compose.yml)
  IT_COMPOSE_PROJECT  Compose project name
  DRY_RUN             If set to 1, commands are only printed
USAGE
}

TIMESTAMP=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --timestamp)
      TIMESTAMP=$2
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

if [[ -z "$TIMESTAMP" ]]; then
  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
fi

read -r -a compose_files <<<"${IT_COMPOSE_FILES:-docker-compose.yml}"
compose_args=()
if [[ -n "${IT_COMPOSE_PROJECT:-}" ]]; then
  compose_args+=(-p "$IT_COMPOSE_PROJECT")
fi
for f in "${compose_files[@]}"; do
  compose_args+=(-f "$f")
done

compose_exec() {
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    printf 'DRY_RUN: docker compose %s exec -T %s %s\n' "${compose_args[*]}" "$1" "${*:2}"
  else
    docker compose "${compose_args[@]}" exec -T "$@"
  fi
}

if [[ "${DRY_RUN:-0}" == "1" ]]; then
  echo "Synthetic test DRY_RUN – skipping execution"
  exit 0
fi

TARGET_DIR="artifacts/backup/synthetic-$TIMESTAMP"
mkdir -p "$TARGET_DIR"

log() {
  printf '[synthetic] %s\n' "$1"
}

postgres_prepare() {
  log "Preparing Postgres dataset"
  compose_exec postgres bash -c "psql -U postgres -v ON_ERROR_STOP=1 <<'SQL'\nCREATE TABLE IF NOT EXISTS backup_smoke(id SERIAL PRIMARY KEY, message TEXT);\nTRUNCATE TABLE backup_smoke;\nINSERT INTO backup_smoke(message) VALUES ('first entry'), ('second entry');\nSQL"
}

neo4j_prepare() {
  log "Preparing Neo4j dataset"
  local password=${NEO4J_PASSWORD:-test12345}
  compose_exec neo4j cypher-shell -u neo4j -p "$password" "MATCH (n:BackupSmoke) DETACH DELETE n"
  compose_exec neo4j cypher-shell -u neo4j -p "$password" "CREATE (:BackupSmoke {name: 'alpha'}), (:BackupSmoke {name: 'beta'})"
}

opensearch_prepare() {
  log "Preparing OpenSearch dataset"
  compose_exec opensearch bash -c "curl -fsS -XDELETE http://localhost:9200/backup-smoke || true"
  compose_exec opensearch bash -c "curl -fsS -H 'Content-Type: application/json' -XPUT http://localhost:9200/backup-smoke -d '{\"settings\":{\"number_of_shards\":1,\"number_of_replicas\":0}}'"
  compose_exec opensearch bash -c "curl -fsS -H 'Content-Type: application/json' -XPOST http://localhost:9200/backup-smoke/_doc/1?refresh=true -d '{\"title\":\"backup smoke\",\"tags\":[\"alpha\",\"beta\"]}'"
}

postgres_wipe() {
  log "Wiping Postgres dataset"
  compose_exec postgres bash -c "psql -U postgres -c 'DROP TABLE IF EXISTS backup_smoke'"
}

neo4j_wipe() {
  log "Wiping Neo4j dataset"
  local password=${NEO4J_PASSWORD:-test12345}
  compose_exec neo4j cypher-shell -u neo4j -p "$password" "MATCH (n:BackupSmoke) DETACH DELETE n"
}

opensearch_wipe() {
  log "Wiping OpenSearch dataset"
  compose_exec opensearch bash -c "curl -fsS -XDELETE http://localhost:9200/backup-smoke || true"
}

postgres_verify() {
  compose_exec postgres psql -U postgres -tA -c "SELECT COUNT(*) FROM backup_smoke"
}

neo4j_verify() {
  local password=${NEO4J_PASSWORD:-test12345}
  compose_exec neo4j bash -c "cypher-shell -u neo4j -p '$password' --format plain \"MATCH (n:BackupSmoke) RETURN count(n)\" | tail -n1"
}

opensearch_verify() {
  compose_exec opensearch bash -c "curl -fsS http://localhost:9200/backup-smoke/_doc/1"
}

postgres_prepare
neo4j_prepare
opensearch_prepare

log "Running backup.sh"
IT_BACKUP_TIMESTAMP="$TIMESTAMP" scripts/backup.sh --out "$TARGET_DIR"

postgres_wipe
neo4j_wipe
opensearch_wipe

log "Running restore.sh"
scripts/restore.sh --path "$TARGET_DIR" --services opensearch,neo4j,postgres

log "Validating datasets"
postgres_count=$(postgres_verify | tr -d '[:space:]')
neo4j_count=$(neo4j_verify | tr -d '[:space:]')
opensearch_doc=$(opensearch_verify)

python <<'PY' "$TARGET_DIR/synthetic-validation.json" "$postgres_count" "$neo4j_count" "$opensearch_doc"
import json
import sys
from pathlib import Path

target, pg_count, neo_count, os_doc = sys.argv[1:5]
Path(target).write_text(json.dumps({
    "postgres_rows": int(pg_count),
    "neo4j_nodes": int(neo_count),
    "opensearch_doc": json.loads(os_doc),
}, indent=2) + "\n", encoding="utf-8")
PY

log "Synthetic backup/restore test complete"
