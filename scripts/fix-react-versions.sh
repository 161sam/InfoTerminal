#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   bash scripts/fix-react-versions.sh            # normal
#   DRY_RUN=1 bash scripts/fix-react-versions.sh  # nur zeigen, nichts schreiben
#   CLEAN=1 bash scripts/fix-react-versions.sh    # node_modules & Lockfiles säubern vor Install

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/apps/frontend"
REACT_VER="${REACT_VER:-18.3.1}"

echo "==> InfoTerminal react/react-dom unify to ${REACT_VER}"
echo "Root: $ROOT_DIR"
echo "App : $FRONTEND_DIR"

# --- helpers ---
have() { command -v "$1" >/dev/null 2>&1; }
pm_detect() {
  if [ -f "$ROOT_DIR/pnpm-lock.yaml" ] || have pnpm; then echo pnpm; return; fi
  if [ -f "$ROOT_DIR/yarn.lock" ] || have yarn; then echo yarn; return; fi
  echo npm
}
json_set() {
  # args: file json-path new-json
  local file="$1" path="$2" new="$3"
  if have jq; then
    if [ -n "${DRY_RUN:-}" ]; then
      echo "DRY jq: $file  $path <- $new"
    else
      tmp="${file}.tmp.$$"
      jq "$path = $new" "$file" > "$tmp" && mv "$tmp" "$file"
    fi
  else
    # minimal sed fallback: naive replace, expects existing key
    # path must be top-level e.g. .dependencies.react
    local key="$(echo "$path" | awk -F'.' '{print $2}')"
    local sub="$(echo "$path" | awk -F'.' '{print $3}')"
    if [ -z "$sub" ]; then
      echo "WARN: no jq; cannot reliably set $path in $file"; return 0
    fi
    if [ -n "${DRY_RUN:-}" ]; then
      echo "DRY sed: set $key.$sub in $file to $new"
    else
      # crude: replace the line with the key if exists
      sed -i -E "s/(\"${sub}\":[[:space:]]*\")([^\"]+)(\")/\1$(echo "$new" | sed 's/\"//g')\3/" "$file" || true
    fi
  fi
}

json_merge() {
  # merge fragment into file root (jq required). If no jq, skip with warn.
  local file="$1" fragment="$2"
  if have jq; then
    if [ -n "${DRY_RUN:-}" ]; then
      echo "DRY merge: $file <- $fragment"
    else
      tmp="${file}.tmp.$$"
      jq -S ". * (${fragment})" "$file" > "$tmp" && mv "$tmp" "$file"
    fi
  else
    echo "WARN: jq not found; skipping merge for $file"
  fi
}

ensure_frontend_pkg() {
  local pkg="$FRONTEND_DIR/package.json"
  if [ ! -f "$pkg" ]; then
    echo "ERROR: $pkg not found"; exit 1
  fi
  echo "==> Ensure name/version/private in apps/frontend/package.json"
  json_merge "$pkg" '{
    "name": "@infoterminal/frontend",
    "version": "0.1.0",
    "private": true
  }'

  echo "==> Pin react/react-dom in frontend"
  json_set "$pkg" '.dependencies.react' "\"${REACT_VER}\""
  json_set "$pkg" '.dependencies["react-dom"]' "\"${REACT_VER}\""

  # react-router-dom bleibt wie ist; nur sicherstellen, dass vorhanden
  if ! grep -q '"react-router-dom"' "$pkg"; then
    json_set "$pkg" '.dependencies["react-router-dom"]' '"^6.30.1"'
  fi
}

ensure_root_overrides() {
  local pkg="$ROOT_DIR/package.json"
  if [ ! -f "$pkg" ]; then
    echo "ERROR: $pkg not found"; exit 1
  fi

  echo "==> Ensure workspaces and overrides in root package.json"
  # füge overrides hinzu (jq bevorzugt)
  json_merge "$pkg" "{
    \"overrides\": {
      \"react\": \"${REACT_VER}\",
      \"react-dom\": \"${REACT_VER}\"
    }
  }"

  # wenn keine workspaces gesetzt sind, versuche sie idempotent zu ergänzen
  if ! grep -q '"workspaces"' "$pkg"; then
    json_merge "$pkg" '{
      "workspaces": ["apps/*", "packages/*"]
    }'
  fi
}

clean_install() {
  local pm
  pm="$(pm_detect)"
  echo "==> Package manager: $pm"

  if [ -n "${CLEAN:-}" ]; then
    echo "==> Clean node_modules & lockfiles"
    rm -rf "$ROOT_DIR/node_modules" "$FRONTEND_DIR/node_modules"
    rm -f "$ROOT_DIR/package-lock.json" "$FRONTEND_DIR/package-lock.json"
    rm -f "$ROOT_DIR/pnpm-lock.yaml" "$FRONTEND_DIR/pnpm-lock.yaml"
    rm -f "$ROOT_DIR/yarn.lock" "$FRONTEND_DIR/yarn.lock"
  fi

  if [ -n "${DRY_RUN:-}" ]; then
    echo "DRY: skip install"
    return
  fi

  case "$pm" in
    pnpm) (cd "$ROOT_DIR" && pnpm install -w) ;;
    yarn) (cd "$ROOT_DIR" && yarn install) ;;
    npm)  (cd "$ROOT_DIR" && npm install --workspaces) ;;
  esac
}

post_checks() {
  echo "==> Versions check"
  (cd "$ROOT_DIR" && npx -y npm-which npm >/dev/null 2>&1 || true)
  (cd "$ROOT_DIR" && npm ls react react-dom || true) | sed -n '1,120p'

  echo "==> Frontend dev script availability (optional)"
  if [ -f "$FRONTEND_DIR/package.json" ]; then
    jq -r '.scripts' "$FRONTEND_DIR/package.json" 2>/dev/null || true
  fi
}

# --- run ---
ensure_frontend_pkg
ensure_root_overrides
clean_install
post_checks

echo "✅ Done. If install failed, try CLEAN=1 bash scripts/fix-react-versions.sh"
