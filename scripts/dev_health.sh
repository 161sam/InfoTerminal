#!/usr/bin/env bash
set -euo pipefail
function h() { curl -sf "$1" >/dev/null && echo "OK  $1" || echo "ERR $1"; }
h http://127.0.0.1:8401/healthz  # search-api (local)
h http://127.0.0.1:8402/healthz  # graph-api (local)
h http://127.0.0.1:8403/healthz  # graph-views (local)
h http://127.0.0.1:8404/healthz  # entity-resolution (expected 404 earlier; should be fixed)
h http://127.0.0.1:8406/healthz  # doc-entities
h http://localhost:3411/api/health  # frontend
