#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   bash scripts/fix-react-versions.sh             # normal
#   DRY_RUN=1 bash scripts/fix-react-versions.sh   # nur zeigen, nichts schreiben
#   CLEAN=1 bash scripts/fix-react-versions.sh     # node_modules & Lockfiles säubern vor Install
#   REACT_VER=18.3.1 bash scripts/fix-react-versions.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/apps/frontend"
ROOT_PKG="$ROOT_DIR/package.json"
FE_PKG="$FRONTEND_DIR/package.json"
WORKSPACE_FILE="$ROOT_DIR/pnpm-workspace.yaml"

REACT_VER="${REACT_VER:-18.3.1}"
TYPES_REACT_VER="${TYPES_REACT_VER:-^18.3.3}"
TYPES_REACT_DOM_VER="${TYPES_REACT_DOM_VER:-^18.3.0}"

echo "==> InfoTerminal react/react-dom unify to ${REACT_VER}"
echo "Root: $ROOT_DIR"
echo "App : $FRONTEND_DIR"

have() { command -v "$1" >/dev/null 2>&1; }

pm_detect() {
  if have pnpm || [[ -f "$ROOT_DIR/pnpm-lock.yaml" ]]; then echo pnpm; return; fi
  if have yarn || [[ -f "$ROOT_DIR/yarn.lock" ]]; then echo yarn; return; fi
  echo npm
}

# write file only if content differs
write_if_changed() {
  local target="$1"; shift
  local tmp="$(mktemp)"
  cat >"$tmp"
  if [ ! -f "$target" ]; then
    if [ -n "${DRY_RUN:-}" ]; then
      echo "DRY create: $target"
      rm -f "$tmp"; return 0
    fi
    mkdir -p "$(dirname "$target")"
    mv "$tmp" "$target"
    echo "[OK] create: $target"
    return 0
  fi
  if cmp -s "$tmp" "$target"; then
    echo "[SKIP] unchanged: $target"
    rm -f "$tmp"
  else
    if [ -n "${DRY_RUN:-}" ]; then
      echo "DRY update: $target"
      rm -f "$tmp"
    else
      mv "$tmp" "$target"
      echo "[OK] update: $target"
    fi
  fi
}

json_merge_root() {
  # merge fragment into file root (jq preferred)
  local file="$1" fragment="$2"
  if have jq; then
    local tmp="${file}.tmp.$$"
    if [ -n "${DRY_RUN:-}" ]; then
      echo "DRY jq-merge: $file <- $fragment"
    else
      jq -S ". * (${fragment})" "$file" > "$tmp" && mv "$tmp" "$file"
      echo "[OK] jq-merge: $file"
    fi
  else
    echo "[WARN] jq not found; cannot safely merge into $file"
  fi
}

json_set_key() {
  # args: file json-path new-json
  local file="$1" path="$2" new="$3"
  if have jq; then
    if [ -n "${DRY_RUN:-}" ]; then
      echo "DRY jq-set: $file  $path <- $new"
    else
      local tmp="${file}.tmp.$$"
      jq "$path = $new" "$file" > "$tmp" && mv "$tmp" "$file"
      echo "[OK] jq-set: $file $path"
    fi
  else
    echo "[WARN] jq not found; best-effort sed for $file $path"
    # crude fallback: only for .dependencies or .devDependencies keys
    local section key
    section="$(echo "$path" | awk -F'.' '{print $2}')" # dependencies or devDependencies
    key="$(echo "$path" | awk -F'.' '{print $3}' | tr -d '[]\"')"
    if [ -z "$section" ] || [ -z "$key" ]; then
      echo "[WARN] cannot sed-set $path in $file"; return 0
    fi
    if [ -n "${DRY_RUN:-}" ]; then
      echo "DRY sed-set $section.$key in $file"
    else
      # Ensure section exists
      grep -q "\"$section\"" "$file" || sed -i -e "s|^{|{\"$section\":{},|" "$file"
      # naive replace or insert
      if grep -q "\"$key\"" "$file"; then
        sed -i -E "s/(\"$key\":[[:space:]]*\")([^\"]*)(\")/\1$(echo "$new" | sed 's/\"//g')\3/" "$file" || true
      else
        sed -i -E "s/\"$section\":[[:space:]]*{([[:space:]]*)/\"$section\": {\"$key\": $(echo "$new"), /" "$file" || true
      fi
      echo "[OK] sed-set: $file $section.$key"
    fi
  fi
}

ensure_workspace_file() {
  echo "==> Ensure pnpm-workspace.yaml"
  write_if_changed "$WORKSPACE_FILE" <<YAML
packages:
  - "apps/*"
  - "services/*"
  # - "packages/*"
YAML
}

ensure_root_package() {
  if [ ! -f "$ROOT_PKG" ]; then
    echo "ERROR: $ROOT_PKG not found"; exit 1
  fi
  echo "==> Ensure workspaces & overrides in root package.json"
  # ensure workspaces
  if ! grep -q '"workspaces"' "$ROOT_PKG"; then
    json_merge_root "$ROOT_PKG" '{
      "workspaces": ["apps/*", "services/*"]
    }'
  fi
  # npm/yarn overrides
  json_merge_root "$ROOT_PKG" "{
    \"overrides\": {
      \"react\": \"${REACT_VER}\",
      \"react-dom\": \"${REACT_VER}\"
    }
  }"
  # pnpm overrides
  if have jq; then
    json_merge_root "$ROOT_PKG" "{
      \"pnpm\": { \"overrides\": { \"react\": \"${REACT_VER}\", \"react-dom\": \"${REACT_VER}\" } }
    }"
  else
    # minimal fallback: append block if missing
    if ! grep -q '"pnpm"' "$ROOT_PKG"; then
      if [ -z "${DRY_RUN:-}" ]; then
        sed -i '$ s/}$/,\n  "pnpm": { "overrides": { "react": "'"$REACT_VER"'", "react-dom": "'"$REACT_VER"'" } }\n}/' "$ROOT_PKG" || true
        echo "[OK] append pnpm.overrides (fallback)"
      else
        echo "DRY append pnpm.overrides (fallback)"
      fi
    fi
  fi
}

ensure_frontend_package() {
  if [ ! -f "$FE_PKG" ]; then
    echo "ERROR: $FE_PKG not found"; exit 1
  fi
  echo "==> Ensure name/version/private in apps/frontend/package.json"
  json_merge_root "$FE_PKG" '{
    "name": "@infoterminal/frontend",
    "version": "0.1.0",
    "private": true
  }'

  echo "==> Pin react/react-dom & types in frontend"
  json_set_key "$FE_PKG" '.dependencies.react' "\"${REACT_VER}\""
  json_set_key "$FE_PKG" '.dependencies["react-dom"]' "\"${REACT_VER}\""

  # ensure react-router-dom exists (keine Versionserhöhung erzwingen)
  if ! grep -q '"react-router-dom"' "$FE_PKG"; then
    json_set_key "$FE_PKG" '.dependencies["react-router-dom"]' '"^6.30.1"'
  fi

  # types angleichen auf 18.x
  json_set_key "$FE_PKG" '.devDependencies["@types/react"]' "\"${TYPES_REACT_VER}\""
  json_set_key "$FE_PKG" '.devDependencies["@types/react-dom"]' "\"${TYPES_REACT_DOM_VER}\""
}

clean_install() {
  local pm; pm="$(pm_detect)"
  echo "==> Package manager: $pm"

  if [ -n "${CLEAN:-}" ]; then
    echo "==> Clean node_modules & lockfiles"
    rm -rf "$ROOT_DIR/node_modules" "$FRONTEND_DIR/node_modules"
    rm -f "$ROOT_DIR/pnpm-lock.yaml" "$ROOT_DIR/yarn.lock" "$ROOT_DIR/package-lock.json"
    rm -f "$FRONTEND_DIR/pnpm-lock.yaml" "$FRONTEND_DIR/yarn.lock" "$FRONTEND_DIR/package-lock.json"
  fi

  if [ -n "${DRY_RUN:-}" ]; then
    echo "DRY: skip install"; return
  fi

  case "$pm" in
    pnpm)
      # mit Workspace-Datei jetzt gültig:
      (cd "$ROOT_DIR" && pnpm install -w)
      ;;
    yarn)
      (cd "$ROOT_DIR" && yarn install)
      ;;
    npm)
      (cd "$ROOT_DIR" && npm install --workspaces)
      ;;
  esac
}

post_checks() {
  echo "==> Versions check (pnpm why preferred)"
  if have pnpm; then
    (cd "$ROOT_DIR" && pnpm why react || true)
    (cd "$ROOT_DIR" && pnpm why react-dom || true)
  else
    (cd "$ROOT_DIR" && npm ls react react-dom || true) | sed -n '1,120p'
  fi

  echo "==> Frontend scripts (for reference)"
  if [ -f "$FE_PKG" ] && have jq; then
    jq -r '.scripts' "$FE_PKG" 2>/dev/null || true
  fi
}

# --- run ---
ensure_workspace_file
ensure_root_package
ensure_frontend_package
clean_install
post_checks

echo "✅ Done. Try: pnpm -w -F @infoterminal/frontend run dev   (oder build)"
