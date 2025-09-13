#!/usr/bin/env bash
set -euo pipefail
svc="${1:-}"
[ -z "$svc" ] && { echo "Usage: $0 <path-to-service>"; exit 1; }
cd "$svc"
if [ -f requirements.txt ]; then
  uv venv .venv
  source .venv/bin/activate
  uv pip install -r requirements.txt
elif [ -f pyproject.toml ]; then
  uv venv .venv
  source .venv/bin/activate
  uv pip install -r pyproject.toml
else
  echo "No requirements.txt or pyproject.toml in $svc"
fi
