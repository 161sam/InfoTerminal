#!/usr/bin/env bash
# Simple health check for local services
set -euo pipefail
h(){ curl -sf "$1" >/dev/null && echo "OK  $1" || echo "ERR $1"; }
h http://127.0.0.1:8401/healthz   # search-api
h http://127.0.0.1:8402/healthz   # graph-api
h http://127.0.0.1:8403/healthz   # graph-views
h http://127.0.0.1:8404/healthz   # entity-resolution (fix erwartet)
h http://127.0.0.1:8406/healthz   # doc-entities
h http://localhost:3411/api/health # frontend
