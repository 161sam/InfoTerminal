#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# ---- Helpers ---------------------------------------------------------------
log() { printf "\033[1;36m[dev-install]\033[0m %s\n" "$*"; }

# Kill a TCP port safely
kill_port() {
  local p="$1"
  fuser -k "${p}/tcp" 2>/dev/null || true
  ss -ltnp 2>/dev/null | awk -v P=":$p" '$4 ~ P {print $6}' \
    | sed -En 's/.*pid=([0-9]+),.*/\1/p' \
    | while read -r PID; do [ -n "$PID" ] && kill -9 "$PID" 2>/dev/null || true; done
}

safe_activate() { set +u; . "$1/bin/activate"; set -u; }  # avoid set -u issues

ensure_uv() {
  if ! command -v uv >/dev/null 2>&1; then
    log "Installing uv (via pipx or pip)"
    command -v pipx >/dev/null 2>&1 && pipx install uv || python3 -m pip install --user uv
    hash -r || true
  fi
}

# ---- Infra: Neo4j + Postgres via Docker -----------------------------------
log "Starting Docker infra (Neo4j + Postgres)"
docker network inspect infoterminal-dev >/dev/null 2>&1 || docker network create infoterminal-dev

docker rm -f it-neo4j >/dev/null 2>&1 || true
docker run -d --name it-neo4j --network infoterminal-dev \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/test123 \
  -e NEO4J_dbms_security_auth__enabled=true \
  neo4j:5.22 >/dev/null

docker rm -f it-postgres >/dev/null 2>&1 || true
docker run -d --name it-postgres --network infoterminal-dev \
  -p 5432:5432 \
  -e POSTGRES_USER=it_user \
  -e POSTGRES_PASSWORD=it_pass \
  -e POSTGRES_DB=it_graph \
  postgres:16 >/dev/null

log "Waiting for Postgres@5432 and Neo4j@7687"
for i in {1..30}; do (echo >/dev/tcp/127.0.0.1/5432) >/dev/null 2>&1 && break || sleep 1; done
for i in {1..30}; do (echo >/dev/tcp/127.0.0.1/7687) >/dev/null 2>&1 && break || sleep 1; done

# ---- Frontend env ----------------------------------------------------------
log "Writing apps/frontend/.env.local"
mkdir -p apps/frontend
cat > apps/frontend/.env.local <<'ENV'
NEXT_PUBLIC_SEARCH_API=http://127.0.0.1:8401
NEXT_PUBLIC_GRAPH_API=http://127.0.0.1:8402
NEXT_PUBLIC_DOCENTITIES_API=http://127.0.0.1:8406
NEXT_PUBLIC_NLP_API=http://127.0.0.1:8404
ENV

# ---- Python deps per service (uv) ------------------------------------------
ensure_uv

# All Python services in this repo:
PY_SERVICES=(
  "services/search-api"
  "services/graph-api"
  "services/graph-views"
  "services/entity-resolution"
  "services/doc-entities"
  "services/opa-audit-sink"
  "services/openbb-connector"
)

for svc in "${PY_SERVICES[@]}"; do
  if [ -d "$svc" ]; then
    log "uv sync -> $svc"
    ( cd "$svc" && uv sync )
  fi
done

# ---- Fix common missing deps (import checks) ------------------------------
# search-api needs pydantic-settings + prometheus-fastapi-instrumentator
fix_missing() {
  local svc="$1"; shift
  local -a pkgs=("$@")
  [ -d "$svc" ] || return 0
  log "Checking imports in $svc"
  if [ -d "$svc/.venv" ]; then
    safe_activate "$svc/.venv"
    for spec in "${pkgs[@]}"; do
      mod="${spec%%=*}"                 # module name heuristic
      pyname="$mod"
      # special-cases for module import names
      [ "$mod" = "pydantic-settings" ] && pyname="pydantic_settings"
      [ "$mod" = "prometheus-fastapi-instrumentator" ] && pyname="prometheus_fastapi_instrumentator"
      python - <<PY 2>/dev/null || (deactivate || true; cd "$svc" && uv add "$spec" && safe_activate ".venv")
try:
    __import__("'"$pyname"'")
except Exception as e:
    raise SystemExit(1)
PY
    done
    deactivate || true
  fi
}

fix_missing "services/search-api" "pydantic-settings==2.*" "prometheus-fastapi-instrumentator==6.1.0" "uvicorn[standard]" "fastapi"
fix_missing "services/graph-api"  "prometheus-fastapi-instrumentator==6.1.0"
fix_missing "services/doc-entities" "prometheus-fastapi-instrumentator==6.1.0"

# ---- Frontend deps ---------------------------------------------------------
if [ -f "apps/frontend/package.json" ]; then
  log "Installing frontend deps"
  ( cd apps/frontend && (npm ci || npm i) )
fi

log "Install done."
