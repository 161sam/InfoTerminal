#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DC="$ROOT/docker-compose.yml"
HELM_VALUES="$ROOT/charts/infoterminal/values.yaml"
FRONTEND_DIR="$ROOT/apps/frontend"
ENV_LOCAL="$FRONTEND_DIR/.env.local"
PKG="$FRONTEND_DIR/package.json"

# -----------------------------
# Desired (fixed) host ports
# -----------------------------
declare -A SERVICE_HOST_PORTS=(
  # docker-compose serviceName => hostPort
  [frontend]=3411
  [search-api]=8611
  [graph-api]=8612
  [aleph]=8613
  [superset]=8644
  [keycloak]=8643
  [grafana]=8641
  [prometheus]=8642
  [postgres]=55432
  [neo4j]=8744       # http (additional mapped below)
)

# Container ports (used when building "host:container" mappings)
declare -A SERVICE_CONTAINER_PORTS=(
  [frontend]=3000
  [search-api]=8080
  [graph-api]=8081
  [aleph]=8082
  [superset]=8088
  [keycloak]=8080
  [grafana]=3000
  [prometheus]=9090
  [postgres]=5432
  [neo4j_http]=7474
  [neo4j_https]=7473
  [neo4j_bolt]=7687
)

# Extra host ports for multi-port services (neo4j)
NEO4J_HOST_HTTP=8744
NEO4J_HOST_HTTPS=8743
NEO4J_HOST_BOLT=8767

# -----------------------------
# Helpers
# -----------------------------
ensure_yq() {
  if command -v yq >/dev/null 2>&1; then
    return 0
  fi
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

# Update or create ports mapping for a service in docker-compose
patch_dc_service_port() {
  local svc="$1"
  local host_port="$2"
  local container_port="${SERVICE_CONTAINER_PORTS[$svc]:-}"

  # Service may be "postgres" or "neo4j" multi-port special handling
  if [[ "$svc" == "neo4j" ]]; then
    # Create ports array with three entries
    yq -i "
      (.services.$svc // {}) as \$s |
      (.services.$svc.ports) = [
        \"${NEO4J_HOST_HTTP}:${SERVICE_CONTAINER_PORTS[neo4j_http]}\",
        \"${NEO4J_HOST_HTTPS}:${SERVICE_CONTAINER_PORTS[neo4j_https]}\",
        \"${NEO4J_HOST_BOLT}:${SERVICE_CONTAINER_PORTS[neo4j_bolt]}\"
      ]
    " "$DC" 2>/dev/null || true
    return
  fi

  [[ -n "$container_port" ]] || return 0

  # Set single mapping host:container
  yq -i "
    (.services.$svc // {}) as \$s |
    (.services.$svc.ports) = [ \"${host_port}:${container_port}\" ]
  " "$DC" 2>/dev/null || true
}

# -----------------------------
# 1) docker-compose.yml
# -----------------------------
if [[ -f "$DC" ]]; then
  echo "🔧 Patch docker-compose.yml"
  ensure_yq
  backup_file "$DC"

  # Iterate known services; only patch if present
  for svc in "${!SERVICE_HOST_PORTS[@]}"; do
    if yq ".services | has(\"$svc\")" "$DC" | grep -q true; then
      patch_dc_service_port "$svc" "${SERVICE_HOST_PORTS[$svc]}"
      echo "  • $svc → ${SERVICE_HOST_PORTS[$svc]}:${SERVICE_CONTAINER_PORTS[$svc]:-?}"
    fi
  done

  # If ports are also exposed via "environment" or labels, you can add further yq edits here as needed.
else
  echo "⚠️  Kein docker-compose.yml gefunden unter $DC – Schritt übersprungen."
fi

# -----------------------------
# 2) Helm values.yaml
# -----------------------------
if [[ -f "$HELM_VALUES" ]]; then
  echo "🔧 Patch Helm charts/infoterminal/values.yaml"
  ensure_yq
  backup_file "$HELM_VALUES"

  # These keys assume a values structure like:
  # frontend.service.port, searchApi.service.port, graphApi.service.port, superset.service.port, keycloak.service.port, grafana.service.port, prometheus.service.port, postgres.service.port, neo4j.service.ports
  # Adjust only if keys exist to avoid breaking unknown structures.

  yq -i "
    (.frontend.service.port) |= 3411
    | (.searchApi.service.port) |= 8611
    | (.graphApi.service.port) |= 8612
    | (.aleph.service.port) |= 8613
    | (.superset.service.port) |= 8644
    | (.keycloak.service.port) |= 8643
    | (.grafana.service.port) |= 8641
    | (.prometheus.service.port) |= 8642
    | (.postgres.service.port) |= 55432
    | (.neo4j.service.ports) |= {
        http: 8744,
        https: 8743,
        bolt: 8767
      }
  " "$HELM_VALUES" 2>/dev/null || true
else
  echo "⚠️  Keine Helm values.yaml gefunden unter $HELM_VALUES – Schritt übersprungen."
fi

# -----------------------------
# 3) Frontend .env.local + package.json
# -----------------------------
echo "🔧 Patch Frontend .env.local & package.json"
mkdir -p "$FRONTEND_DIR"
backup_file "$ENV_LOCAL"
{
  echo "PORT=3411"
  echo "NEXT_PUBLIC_SEARCH_API_URL=http://localhost:8611/health"
  echo "NEXT_PUBLIC_GRAPH_API_URL=http://localhost:8612/health"
} > "$ENV_LOCAL"

# Optional: adjust npm scripts to enforce 3411 even ohne env
if [[ -f "$PKG" ]]; then
  backup_file "$PKG"
  # dev/start → -p 3411
  tmp="$(mktemp)"
  jq '.scripts.dev = "next dev -p 3411" | .scripts.start = "next start -p 3411"' "$PKG" > "$tmp" 2>/dev/null || cp "$PKG" "$tmp"
  mv "$tmp" "$PKG"
fi

echo "✅ Ports gepatcht. Bitte nun:"
echo "   git add -A && git commit -m \"chore: set non-standard service ports (frontend=3411, etc.)\""
echo "   # lokal testen:"
echo "   docker compose up -d   # oder: make dev-up (nach Makefile-TAB-Fix)"
echo "   # Frontend:"
echo "   cd apps/frontend && npm run dev   # läuft nun auf http://localhost:3411"

