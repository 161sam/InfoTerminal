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

# -------- config --------
# 1 = App-Services lokal via dev_run.sh; 0 = App-Services dockerisiert
DEV_LOCAL="${DEV_LOCAL:-1}"
# Optional-Stacks
OBS="${OBS:-0}"        # Observability (Grafana=3412, Prometheus=3415, Tempo=3414, Loki=3413, OTEL gRPC=3416)
AGENTS="${AGENTS:-0}"  # Flowise-Connector (3417)
GW="${GW:-0}"          # Gateway (8610) + OPA

if [ "$DEV_LOCAL" = "1" ]; then
  # Telemetry-Noise für lokale Dev-Runs wirklich aus
  export OTEL_SDK_DISABLED=1
  export OTEL_TRACES_EXPORTER=none
  export OTEL_METRICS_EXPORTER=none
  export OTEL_LOGS_EXPORTER=none
  export GRPC_VERBOSITY=ERROR
fi

# -------- compose helpers --------
compose_services() {
  docker compose config --services 2>/dev/null || true
}
compose_has() {
  compose_services | grep -qx "$1"
}
compose_up_if_present() {
  local wanted=() s
  for s in "$@"; do compose_has "$s" && wanted+=("$s"); done
  if [ "${#wanted[@]}" -gt 0 ]; then
    log "Starting infra via compose: ${wanted[*]}"
    docker compose up -d "${wanted[@]}" >/dev/null
  else
    log "No matching infra services in docker-compose.yml (skipping)"
  fi
}

# -------- infra up (auto-detect) --------
# Häufige Infra-Dienste: opensearch, neo4j, postgres
compose_up_if_present opensearch neo4j postgres

# Health waits (nur für vorhandene)
if compose_has opensearch; then
  for i in {1..60}; do (echo >/dev/tcp/127.0.0.1/9200) >/dev/null 2>&1 && break || sleep 1; done
fi
if compose_has neo4j; then
  for i in {1..60}; do (echo >/dev/tcp/127.0.0.1/7687) >/dev/null 2>&1 && break || sleep 1; done
fi
if compose_has postgres; then
  for i in {1..60}; do (echo >/dev/tcp/127.0.0.1/5432) >/dev/null 2>&1 && break || sleep 1; done
fi

# -------- ensure free local/dev + docker host ports --------
# Lokale Dev-Ports (840x), Frontend (3411) sowie mögliche dockerisierte App-Hostports (861x)
for p in 8401 8402 8403 8404 8406 3411 8611 8612 8613; do kill_port "$p"; done

log "Ports: search-api=8401 graph-api=8402 graph-views=8403 nlp=8404 frontend=3411"
log "Neo4j user=${NEO4J_USER:-neo4j}"
log "Postgres user=${PG_USER:-it_user} db=${PG_DB:-it_graph} port=${PG_PORT:-5432}"

start_plain() {
  local path="$1" name="$2"
  log "Starting $name (local)"
  ( cd "$path" && bash dev_run.sh ) >"/tmp/it_${name}.log" 2>&1 &
}

# -------- start apps --------
if [ "$DEV_LOCAL" = "1" ]; then
  # search-api (local)
  [ -x services/search-api/dev_run.sh ] && start_plain "services/search-api" "search-api"

  # graph-api (local) mit Neo4j-Env
  if [ -x services/graph-api/dev_run.sh ]; then
    log "Starting graph-api (local, Neo4j env)"
    log "NEO4J_URI=bolt://127.0.0.1:7687 NEO4J_USER=neo4j"
    (
      cd services/graph-api
      NEO4J_URI="bolt://127.0.0.1:7687" \
      NEO4J_USER="neo4j" \
      NEO4J_PASSWORD="test12345" \
      bash dev_run.sh
    ) > /tmp/it_graph-api.log 2>&1 &
  fi

  # graph-views (local) mit Postgres-Env
  if [ -x services/graph-views/dev_run.sh ]; then
    log "Starting graph-views (local, PG env)"
    log "PG_HOST=127.0.0.1 PG_PORT=5432 PG_DB=it_graph PG_USER=it_user"
    (
      cd services/graph-views
      PG_HOST=127.0.0.1 PG_PORT=5432 PG_DB=it_graph PG_USER=it_user PG_PASSWORD=it_pass \
      bash dev_run.sh
    ) > /tmp/it_graph-views.log 2>&1 &
  fi

  # entity-resolution (local)
  [ -x services/entity-resolution/dev_run.sh ] && start_plain "services/entity-resolution" "entity-resolution"

else
  # Container-Betrieb der App-Services (Dockerfiles erforderlich)
  log "Starting app services in Docker (non-standard host ports)"
  # Nur existierende Services starten:
  docker compose up -d $(compose_services | grep -E '^(search-api|graph-api|graph-views|entity-resolution)$' || true) >/dev/null || true
fi

# --- frontend (immer lokal für DX, Port-Policy 3411) ---
if [ -f "apps/frontend/package.json" ]; then
  log "Starting frontend on 3411"
  ( cd apps/frontend && PORT=3411 npm run dev ) >/tmp/it_frontend.log 2>&1 &
fi

# --- optional: observability stack (isoliertes Compose-Projekt) ---
start_obs() {
  local services=(otel-collector loki promtail tempo prometheus grafana)
  echo "[dev-up] Starting observability (Grafana=3412, Prometheus=3415, Tempo=3414, Loki=3413, OTEL gRPC=3416)"
  docker compose -p infoterminal_obs -f docker-compose.observability.yml \
    --profile obs up -d --no-build --remove-orphans "${services[@]}"
}
[ "$OBS" = "1" ] && start_obs

# --- optional: flowise-connector (isoliertes Compose-Projekt) ---
start_agents() {
  local services=(flowise-connector)
  echo "[dev-up] Starting agents (flowise-connector on 3417)"
  docker compose -p infoterminal_agents -f docker-compose.agents.yml \
    --profile agents up -d --no-build --remove-orphans "${services[@]}"
}
[ "$AGENTS" = "1" ] && start_agents

# --- optional: gateway + opa ---
if [ "$GW" = "1" ]; then
  log "Starting gateway on 8610"
  # OPA isoliert starten (kein Host-Port; optional via OPA_EXPOSE=1)
  docker compose -p infoterminal_opa -f docker-compose.opa.yml up -d --no-build --remove-orphans opa
  # Gateway isoliert starten; Upstreams: lokal wenn DEV_LOCAL=1
  USE_LOCAL_UPSTREAMS=$([ "$DEV_LOCAL" = "1" ] && echo 1 || echo 0) \
  docker compose -p infoterminal_gateway -f docker-compose.gateway.yml up -d --no-build --remove-orphans gateway
fi

log "Tailing logs… (Ctrl-C to stop)"
tail -n +1 -f /tmp/it_*.log || true

