#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DC="$ROOT/docker-compose.yml"
DC_OBS="$ROOT/docker-compose.observability.yml"
DC_AGENTS="$ROOT/docker-compose.agents.yml"
HELM_VALUES="$ROOT/charts/infoterminal/values.yaml"
FRONTEND_DIR="$ROOT/apps/frontend"
ENV_LOCAL="$FRONTEND_DIR/.env.local"
PKG="$FRONTEND_DIR/package.json"

# -----------------------------
# Host ports (policy)
# -----------------------------
declare -A HOST_PORTS_COMPOSE=(
  # App services (dockerized mode)
  [search-api]=8611
  [graph-api]=8612
  [aleph]=8613

  # Optional other apps
  [superset]=8644
  [keycloak]=8643
)

# Container ports (internal)
declare -A CONTAINER_PORTS=(
  [search-api]=8080
  [graph-api]=8080
  [aleph]=8080
  [superset]=8088
  [keycloak]=8080
)

# Observability fixed
OBS_PROM=3412
OBS_GRAFANA=3413
OBS_ALERT=3414
OBS_LOKI=3415
OBS_TEMPO=3416
AGENTS_FLOWISE=3417

# -----------------------------
# Helpers
# -----------------------------
ensure_yq() {
  if command -v yq >/dev/null 2>&1; then return 0; fi
  echo "ℹ️  yq nicht gefunden – installiere lokales Binary in ~/.local/bin ..."
  mkdir -p "$HOME/.local/bin"
  YQ_URL="https://github.com/mikefarah/yq/releases/download/v4.44.3/yq_linux_amd64"
  curl -fsSL "$YQ_URL" -o "$HOME/.local/bin/yq"
  chmod +x "$HOME/.local/bin/yq"
  export PATH="$HOME/.local/bin:$PATH"
  command -v yq >/dev/null 2>&1 || { echo "❌ yq Installation fehlgeschlagen"; exit 1; }
}

backup_file() {
  local f="$1"
  [[ -f "$f" ]] || return 0
  cp -f "$f" "${f}.bak.$(date +%Y%m%d-%H%M%S)"
}

patch_port_yaml_simple() { # file service host_port container_port
  local f="$1" svc="$2" hp="$3" cp="$4"
  [ -f "$f" ] || return 0
  # Falls ports nicht existieren: anlegen
  if ! yq ".services | has(\"$svc\")" "$f" >/dev/null 2>&1; then
    return 0
  fi
  yq -i "
    (.services.$svc // {}) as \$s |
    (.services.$svc.ports) = ((.services.$svc.ports // []) + [\"${hp}:${cp}\"]) |
    (.services.$svc.ports) |= unique
  " "$f" 2>/dev/null || true
}

# -----------------------------
# 1) docker-compose.yml (App-Services)
# -----------------------------
if [[ -f "$DC" ]]; then
  echo "🔧 Patch docker-compose.yml"
  ensure_yq
  backup_file "$DC"
  for svc in "${!HOST_PORTS_COMPOSE[@]}"; do
    if yq ".services | has(\"$svc\")" "$DC" | grep -q true; then
      patch_port_yaml_simple "$DC" "$svc" "${HOST_PORTS_COMPOSE[$svc]}" "${CONTAINER_PORTS[$svc]}"
      echo "  • $svc → ${HOST_PORTS_COMPOSE[$svc]}:${CONTAINER_PORTS[$svc]}"
    fi
  done
else
  echo "⚠️  Kein docker-compose.yml gefunden unter $DC – Schritt übersprungen."
fi

# -----------------------------
# 2) Observability Overrides
# -----------------------------
if [[ -f "$DC_OBS" ]]; then
  echo "🔧 Patch docker-compose.observability.yml"
  ensure_yq
  backup_file "$DC_OBS"
  # Ports are referenced via environment variables in compose file
fi

# -----------------------------
# 3) Agents Override
# -----------------------------
if [[ -f "$DC_AGENTS" ]]; then
  echo "🔧 Patch docker-compose.agents.yml"
  ensure_yq
  backup_file "$DC_AGENTS"
  patch_port_yaml_simple "$DC_AGENTS" "flowise-connector" "$AGENTS_FLOWISE" "8080"
fi

# -----------------------------
# 4) Helm values.yaml (best effort)
# -----------------------------
if [[ -f "$HELM_VALUES" ]]; then
  echo "🔧 Patch Helm charts/infoterminal/values.yaml"
  ensure_yq
  backup_file "$HELM_VALUES"
  yq -i "
    (.frontend.service.port) |= 3411
    | (.searchApi.service.port) |= 8611
    | (.graphApi.service.port) |= 8612
    | (.aleph.service.port) |= 8613
    | (.observability.ports) = {
        prometheus: $OBS_PROM,
        grafana: $OBS_GRAFANA,
        alertmanager: $OBS_ALERT,
        loki: $OBS_LOKI,
        tempo: $OBS_TEMPO
      }
    | (.agents.flowise.port) |= $AGENTS_FLOWISE
  " "$HELM_VALUES" 2>/dev/null || true
fi

# -----------------------------
# 5) .env.dev.ports
# -----------------------------
ENV_PORTS="$ROOT/.env.dev.ports"
echo "🔧 Patch .env.dev.ports"
backup_file "$ENV_PORTS"
{
  echo "SEARCH_API_URL=http://127.0.0.1:8401"
  echo "GRAPH_API_URL=http://127.0.0.1:8402"
  echo "GRAPH_VIEWS_URL=http://127.0.0.1:8403"
  echo "ENTITY_RESOLUTION_URL=http://127.0.0.1:8404"
  echo "DOC_ENTITIES_URL=http://127.0.0.1:8406"
  echo "PROMETHEUS_PORT=$OBS_PROM"
  echo "GRAFANA_PORT=$OBS_GRAFANA"
  echo "ALERTMANAGER_PORT=$OBS_ALERT"
  echo "LOKI_PORT=$OBS_LOKI"
  echo "TEMPO_PORT=$OBS_TEMPO"
} > "$ENV_PORTS"

# -----------------------------
# 6) Frontend .env.local + package.json
# -----------------------------
echo "🔧 Patch Frontend .env.local & package.json"
mkdir -p "$FRONTEND_DIR"
backup_file "$ENV_LOCAL"
{
  echo "PORT=3411"
  echo "NEXT_PUBLIC_SEARCH_API=http://127.0.0.1:8401"
  echo "NEXT_PUBLIC_GRAPH_API=http://127.0.0.1:8402"
  echo "NEXT_PUBLIC_VIEWS_API=http://127.0.0.1:8403"
} > "$ENV_LOCAL"

if [[ -f "$PKG" ]]; then
  backup_file "$PKG"
  tmp="$(mktemp)"
  jq '.scripts.dev = "next dev -p 3411" | .scripts.start = "next start -p 3411"' "$PKG" > "$tmp" 2>/dev/null || cp "$PKG" "$tmp"
  mv "$tmp" "$PKG"
fi

echo "✅ Ports gepatcht. (Frontend 3411; Obs 3412–3416; Agents 3417; Apps dockerized 8611/8612/8613)"

