#!/usr/bin/env bash
set -euo pipefail
# Wrapper that delegates to infrastructure seeding script.
# TODO: replace once demo data import is finalized.
ROOT="$(dirname "$0")/.."
exec "$ROOT/infra/scripts/seed-demo.sh"
