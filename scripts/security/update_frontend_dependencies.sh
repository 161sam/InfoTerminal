#!/usr/bin/env bash
# Update vulnerable frontend dependencies to the pinned safe versions.
# Usage: DRY_RUN=1 ./scripts/security/update_frontend_dependencies.sh
# Requires: python3 (for JSON manipulation).

set -euo pipefail

ROOT_DIR=$(cd -- "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
FRONTEND_PKG="$ROOT_DIR/apps/frontend/package.json"
ROOT_PKG="$ROOT_DIR/package.json"
LOCKFILE="$ROOT_DIR/pnpm-lock.yaml"

deps_py() {
  python3 - "$@" <<'PY'
import json
import sys
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit("expected path argument")
path = Path(sys.argv[1])
data = json.loads(path.read_text())
updates = {
    "next": "14.2.7",
    "form-data": "4.0.2",
    "https-proxy-agent": "7.0.6",
    "deep-extend": "0.6.1",
    "json-schema": "0.5.2"
}
changed = False
for section in ("dependencies", "devDependencies"):
    deps = data.get(section)
    if not isinstance(deps, dict):
        continue
    for name, version in updates.items():
        if name in deps and deps[name] != version:
            deps[name] = version
            changed = True
path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n")
print("changed" if changed else "unchanged")
PY
}

overrides_py() {
  python3 - "$@" <<'PY'
import json
import sys
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit("expected path argument")
path = Path(sys.argv[1])
data = json.loads(path.read_text())
overrides = data.setdefault("overrides", {})
updates = {
    "minimist": "1.2.8",
    "deep-extend": "0.6.1",
    "https-proxy-agent": "7.0.6",
    "form-data": "4.0.2",
    "json-schema": "0.5.2",
    "next": "14.2.7"
}
changed = False
for name, version in updates.items():
    if overrides.get(name) != version:
        overrides[name] = version
        changed = True
path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n")
print("changed" if changed else "unchanged")
PY
}

note() { printf '>> %s\n' "$*"; }

dry_run=${DRY_RUN:-0}
if [[ "$dry_run" == "1" ]]; then
  note "DRY_RUN=1 -> no files will be modified"
fi

if [[ ! -f "$FRONTEND_PKG" ]]; then
  echo "Frontend package.json not found: $FRONTEND_PKG" >&2
  exit 1
fi

if [[ "$dry_run" != "1" ]]; then
  note "Updating apps/frontend/package.json"
  deps_py "$FRONTEND_PKG"
  note "Enforcing overrides in package.json"
  overrides_py "$ROOT_PKG"
else
  note "Would update apps/frontend/package.json with pinned versions"
  note "Would enforce overrides (minimist, deep-extend, https-proxy-agent, form-data, json-schema, next)"
fi

cat <<'EOF'

Next steps (manual):
  1. pnpm install --filter @infoterminal/frontend... --no-frozen-lockfile
  2. pnpm --filter @infoterminal/frontend run lint
  3. pnpm --filter @infoterminal/frontend test
  4. pnpm --filter @infoterminal/frontend run build
  5. Review pnpm-lock.yaml updates and commit alongside regenerated container artefacts.

EOF

if [[ -f "$LOCKFILE" ]]; then
  note "Reminder: regenerate pnpm-lock.yaml after running the install step." >&2
fi
