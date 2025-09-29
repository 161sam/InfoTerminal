#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPORT_FILE="${SCRIPT_DIR}/report.md"

show_help() {
  cat <<'USAGE'
Usage: v02_to_v10_demo.sh [options]

Synthetic upgrade rehearsal for InfoTerminal v0.2 → v1.0.

Options:
  --workspace <path>   Working directory for the simulated environment (default: ./artifacts/upgrade/workspace)
  --dry-run            Print the commands without executing them.
  --keep-workspace     Preserve the workspace after completion (default: workspace removed on success).
  --help               Display this help message.

Environment variables:
  DRY_RUN=1            Equivalent to passing --dry-run.

Examples:
  bash artifacts/upgrade/v02_to_v10_demo.sh --workspace /tmp/infoterminal-demo
  DRY_RUN=1 bash artifacts/upgrade/v02_to_v10_demo.sh
USAGE
}

DRY_RUN=${DRY_RUN:-0}
KEEP_WORKSPACE=0
WORKSPACE="${SCRIPT_DIR}/workspace"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace)
      WORKSPACE="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --keep-workspace)
      KEEP_WORKSPACE=1
      shift
      ;;
    --help|-h)
      show_help
      exit 0
      ;;
    *)
      echo "[ERROR] Unknown option: $1" >&2
      show_help
      exit 1
      ;;
  esac
done

run_cmd() {
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[DRY_RUN] %s\n' "$*"
  else
    "$@"
  fi
}

log_step() {
  printf '\n==> %s\n' "$1"
}

append_report() {
  local text="$1"
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[DRY_RUN] report += %s\n' "$text"
  else
    printf '%s\n' "$text" >> "$REPORT_FILE"
  fi
}

prepare_report() {
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[DRY_RUN] truncate %s\n' "$REPORT_FILE"
  else
    cat <<'HEADER' > "$REPORT_FILE"
# v0.2 → v1.0 Synthetic Upgrade Report

| Step | Result | Notes |
| --- | --- | --- |
HEADER
  fi
}

clean_workspace() {
  if [[ -d "$WORKSPACE" ]]; then
    log_step "Cleaning existing workspace at $WORKSPACE"
    run_cmd rm -rf "$WORKSPACE"
  fi
  if [[ "$DRY_RUN" != "1" ]]; then
    rm -f "$REPORT_FILE"
  fi
}

create_workspace() {
  log_step "Creating workspace at $WORKSPACE"
  run_cmd mkdir -p "$WORKSPACE"/v0_2/{config,data} "$WORKSPACE"/backups "$WORKSPACE"/logs
}

seed_v02_dataset() {
  log_step "Seeding synthetic v0.2 dataset"
  run_cmd bash -c "cat <<'DATA' > '$WORKSPACE/v0_2/data/entities.csv'
entity_id,name,type
1,Acme Corp,organization
2,Jane Doe,person
DATA"
  run_cmd bash -c "cat <<'DATA' > '$WORKSPACE/v0_2/config/flags.env'
DOC_ENTITY_V1=false
GRAPH_ALGO_V1=false
GATEWAY_OIDC_ENFORCE=false
OBS_ENRICH_TRACES=false
DATA"
  append_report "| Seed v0.2 dataset | ✅ | Sample entities and feature flags generated. |"
}

create_backups() {
  log_step "Creating backup artifacts"
  run_cmd bash -c "tar -czf '$WORKSPACE/backups/postgres-v0_2.tgz' -C '$WORKSPACE/v0_2/data' entities.csv"
  run_cmd bash -c "cp '$WORKSPACE/v0_2/data/entities.csv' '$WORKSPACE/backups/neo4j-v0_2.export'"
  run_cmd bash -c "cp '$WORKSPACE/v0_2/data/entities.csv' '$WORKSPACE/backups/opensearch-v0_2.snapshot'"
  append_report "| Backups | ✅ | Postgres/Neo4j/OpenSearch snapshots written. |"
}

apply_migrations() {
  log_step "Applying simulated migrations"
  run_cmd mkdir -p "$WORKSPACE/v1_0/data" "$WORKSPACE/v1_0/config"
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[DRY_RUN] python transform %s to %s\n' "$WORKSPACE/v0_2/data/entities.csv" "$WORKSPACE/v1_0/data/entities.csv"
  else
    python - "$WORKSPACE/v0_2/data/entities.csv" "$WORKSPACE/v1_0/data/entities.csv" <<'PY'
import csv
import sys
from pathlib import Path

source = Path(sys.argv[1])
destination = Path(sys.argv[2])
with source.open(newline="") as handle, destination.open("w", newline="") as output:
    reader = csv.reader(handle)
    writer = csv.writer(output)
    header = next(reader)
    header.append("graph_score")
    writer.writerow(header)
    for idx, row in enumerate(reader, start=1):
        row.append(f"{idx * 0.42:.2f}")
        writer.writerow(row)
PY
  fi
  run_cmd bash -c "cat <<'DATA' > '$WORKSPACE/v1_0/config/flags.env'
DOC_ENTITY_V1=true
GRAPH_ALGO_V1=true
GATEWAY_OIDC_ENFORCE=false
OBS_ENRICH_TRACES=true
DATA"
  append_report "| Run migrations | ✅ | Added graph scores and staged new flag defaults. |"
}

verify_upgrade() {
  log_step "Running synthetic verifications"
  run_cmd bash -c "grep -q 'graph_score' '$WORKSPACE/v1_0/data/entities.csv'"
  run_cmd bash -c "grep -q 'DOC_ENTITY_V1=true' '$WORKSPACE/v1_0/config/flags.env'"
  append_report "| Validate results | ✅ | v1.0 dataset contains new column and updated flags. |"
}

finalize_report() {
  if [[ "$DRY_RUN" != "1" ]]; then
    append_report "| Cleanup | ✅ | Workspace $( [[ "$KEEP_WORKSPACE" == "1" ]] && echo 'preserved' || echo 'archived') after run. |"
  else
    printf '[DRY_RUN] report += | Cleanup | ...\n'
  fi
}

cleanup() {
  if [[ "$KEEP_WORKSPACE" == "1" ]]; then
    log_step "Preserving workspace at $WORKSPACE"
  else
    log_step "Removing workspace"
    run_cmd rm -rf "$WORKSPACE"
  fi
}

main() {
  clean_workspace
  prepare_report
  create_workspace
  seed_v02_dataset
  create_backups
  apply_migrations
  verify_upgrade
  finalize_report
  cleanup
  log_step "Synthetic upgrade complete"
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '\nReport would be stored at %s\n' "$REPORT_FILE"
  else
    printf '\nReport stored at %s\n' "$REPORT_FILE"
  fi
}

main "$@"
