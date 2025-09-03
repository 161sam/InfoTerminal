#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

log() { printf "\033[1;35m[dev-up]\033[0m %s\n" "$*"; }

kill_port() {
  local p="$1"
  fuser -k "${p}/tcp" 2>/dev/null || true
  ss -ltnp 2>/dev/null | awk -v P=":$p" '$4 ~ P {print $6}' \
    | sed -En 's/.*pid=([0-9]+),.*/\1/p' \
    | while read -r PID; do [ -n "$PID" ] && kill -9 "$PID" 2>/dev/null || true; done
}

# --- Disable telemetry noise (really off)
export OTEL_SDK_DISABLED=1
export OTEL_TRACES_EXPORTER=none
export OTEL_METRICS_EXPORTER=none
export OTEL_LOGS_EXPORTER=none
export GRPC_VERBOSITY=ERROR

# --- Ensure Docker infra is up
docker start it-postgres it-neo4j 2>/dev/null || true
# wait a bit for ports
for i in {1..20}; do (echo >/dev/tcp/127.0.0.1/5432) >/dev/null 2>&1 && break || sleep 1; done
for i in {1..20}; do (echo >/dev/tcp/127.0.0.1/7687) >/dev/null 2>&1 && break || sleep 1; done

# Free ports
for p in 8401 8402 8403 8404 8406 3411; do kill_port "$p"; done

start_plain() {
  local path="$1" name="$2"
  log "Starting $name"
  ( cd "$path" && bash dev_run.sh ) >"/tmp/it_${name}.log" 2>&1 &
}

# --- search-api (plain)
[ -x services/search-api/dev_run.sh ] && start_plain "services/search-api" "search-api"

# --- graph-api with Neo4j env
if [ -x services/graph-api/dev_run.sh ]; then
  log "Starting graph-api (with Neo4j env)"
  (
    cd services/graph-api
    NEO4J_URI="bolt://127.0.0.1:7687" \
    NEO4J_USER="neo4j" \
    NEO4J_PASSWORD="test123" \
      bash dev_run.sh
  ) > /tmp/it_graph-api.log 2>&1 &
fi

# --- graph-views with Postgres env
if [ -x services/graph-views/dev_run.sh ]; then
  log "Starting graph-views (with PG env)"
  (
    cd services/graph-views
    PG_HOST=127.0.0.1 PG_PORT=5432 PG_DB=it_graph PG_USER=it_user PG_PASSWORD=it_pass \
      bash dev_run.sh
  ) > /tmp/it_graph-views.log 2>&1 &
fi

# --- entity-resolution (plain)
[ -x services/entity-resolution/dev_run.sh ] && start_plain "services/entity-resolution" "entity-resolution"

# --- doc-entities with SQLAlchemy URL
if [ -x services/doc-entities/dev_run.sh ]; then
  log "Starting doc-entities (with DATABASE_URL)"
  (
    cd services/doc-entities
    DATABASE_URL="postgresql://it_user:it_pass@127.0.0.1:5432/it_graph" \
      bash dev_run.sh
  ) > /tmp/it_doc-entities.log 2>&1 &
fi

# --- frontend
if [ -f "apps/frontend/package.json" ]; then
  log "Starting frontend on 3411"
  ( cd apps/frontend && PORT=3411 npm run dev ) >/tmp/it_frontend.log 2>&1 &
fi

log "Tailing logs… (Ctrl-C to stop)"
tail -n +1 -f /tmp/it_*.log
