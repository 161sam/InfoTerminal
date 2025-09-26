#!/usr/bin/env bash
set -euo pipefail

# fix_frontend_lints.sh — Idempotent helper to lint/typecheck and optionally apply autofixes
# Usage:
#   DRY_RUN=1 ./scripts/fix_frontend_lints.sh           # default; no changes, just reports
#   DRY_RUN=0 ./scripts/fix_frontend_lints.sh           # apply eslint --fix where safe
#   ./scripts/fix_frontend_lints.sh --help              # show help

help() {
  cat <<EOF
Usage: DRY_RUN=1 $0 [--help]

Runs ESLint and TypeScript checks for apps/frontend, writes reports to reports/frontend/.
If DRY_RUN=0, applies eslint --fix to TS/TSX files.

Env:
  DRY_RUN=1   Do not modify files, only report (default)

Outputs:
  reports/frontend/eslint.txt
  reports/frontend/tsc.txt

EOF
}

if [[ "${1:-}" == "--help" ]]; then
  help
  exit 0
fi

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
FRONTEND_DIR="$ROOT_DIR/apps/frontend"
REPORT_DIR="$ROOT_DIR/reports/frontend"
mkdir -p "$REPORT_DIR"

echo "[fix_frontend_lints] Running ESLint (report -> $REPORT_DIR/eslint.txt)"
(
  cd "$FRONTEND_DIR"
  pnpm lint || true
) | tee "$REPORT_DIR/eslint.txt"

echo "[fix_frontend_lints] Running TypeScript typecheck (report -> $REPORT_DIR/tsc.txt)"
(
  cd "$FRONTEND_DIR"
  pnpm typecheck || true
) | tee "$REPORT_DIR/tsc.txt"

if [[ "${DRY_RUN:-1}" != "0" ]]; then
  echo "[fix_frontend_lints] DRY_RUN enabled; skipping autofix"
  exit 0
fi

echo "[fix_frontend_lints] Applying eslint --fix to TS/TSX files"
(
  cd "$FRONTEND_DIR"
  pnpm lint:fix || true
)

echo "[fix_frontend_lints] Re-running checks after autofix"
(
  cd "$FRONTEND_DIR"
  pnpm lint || true
  pnpm typecheck || true
)

echo "[fix_frontend_lints] Done"

