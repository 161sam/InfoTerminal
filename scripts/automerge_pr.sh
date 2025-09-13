#!/usr/bin/env bash
# =============================================================================
# Automerge PR → main mit gezielter Konfliktauflösung
#  - bevorzugt PR-Inhalte für Layout/Theme/Panel/Tests/TS-Config
#  - Lockfile wird neu erzeugt (kein manueller Merge)
#  - Build + Tests am Ende
# =============================================================================
set -euo pipefail

BASE="${BASE_REF:-origin/main}"
PR="${PR_NUMBER:-169}"
WORK="merge/pr-${PR}"

echo "→ Setup: BASE=$BASE PR=$PR WORK=$WORK" >&2

git fetch --all --prune --tags

# 1) Arbeitsbranch von main
git switch -C "$WORK" "$BASE"

# 2) PR-Head ermitteln & mergen (gh bevorzugt, sonst remote-branch annehmen)
if command -v gh >/dev/null 2>&1; then
  HEAD_BRANCH="$(gh pr view "$PR" --json headRefName -q .headRefName)"
  : "${HEAD_BRANCH:?Head-Branch nicht gefunden}"
  echo "→ PR #$PR headRef: $HEAD_BRANCH" >&2
  git fetch origin "$HEAD_BRANCH":"tmp/$HEAD_BRANCH"
  set +e
  git merge --no-commit --no-ff "tmp/$HEAD_BRANCH"
  MERGE_RC=$?
  set -e
  echo "→ Merge exit code: $MERGE_RC" >&2
else
  echo "✗ gh CLI fehlt – bitte HEAD Branch von PR #$PR manuell setzen (HEAD_BRANCH=...)." >&2
  exit 1
fi

# 3) Konflikte gezielt auflösen (theirs = PR soll gewinnen)
resolve_theirs() {
  for f in "$@"; do
    if [ -e "$f" ] || git ls-files --error-unmatch "$f" >/dev/null 2>&1; then
      git checkout --theirs -- "$f" 2>/dev/null || true
      git add "$f" 2>/dev/null || true
      echo "→ prefer theirs: $f" >&2
    fi
  done
}
resolve_ours() {
  for f in "$@"; do
    if [ -e "$f" ] || git ls-files --error-unmatch "$f" >/dev/null 2>&1; then
      git checkout --ours -- "$f" 2>/dev/null || true
      git add "$f" 2>/dev/null || true
      echo "→ prefer ours: $f" >&2
    fi
  done
}

# 3a) PR gewinnen lassen
resolve_theirs \
  apps/frontend/pages/_document.tsx \
  apps/frontend/src/styles/globals.css \
  apps/frontend/src/components/layout/Panel.tsx \
  apps/frontend/src/components/layout/DashboardLayout.tsx \
  apps/frontend/pages/graphx.tsx \
  apps/frontend/pages/search.tsx \
  apps/frontend/pages/documents/index.tsx \
  apps/frontend/src/lib/api.ts \
  apps/frontend/vitest.config.ts \
  apps/frontend/vitest.setup.ts \
  apps/frontend/src/test/setupTests.tsx \
  apps/frontend/src/setupTests.ts \
  apps/frontend/tsconfig.json \
  apps/frontend/package.json \
  scripts/tailwind_v4_guard.sh

# 3b) Routen/Legacy entfernen – sicherstellen, dass Löschungen übernommen sind
for dead in \
  apps/frontend/src/components/Layout.tsx \
  apps/frontend/src/components/layout/AppLayout.tsx \
  apps/frontend/src/components/layout/Sidebar.tsx \
  apps/frontend/src/pages/ExternalAppPage.tsx \
  apps/frontend/src/pages/Home.tsx \
  "apps/frontend/pages/apps/[app].tsx" \
  apps/frontend/src/routes/appRoutes.ts
do
  if git ls-files --error-unmatch "$dead" >/dev/null 2>&1; then
    git rm -f "$dead" || true
    echo "→ removed: $dead" >&2
  fi
done

# 3c) Lockfile nicht mergen – neu generieren
if [ -f pnpm-lock.yaml ]; then
  git rm -f pnpm-lock.yaml || true
  echo "→ removed pnpm-lock.yaml to regenerate" >&2
fi

# 4) Merge committen
git commit -m "merge: PR #$PR into main with conflict resolution (prefer #$PR for layout/theme/panel/tests); lockfile regenerated" || true

# 5) Lockfile neu erzeugen (Workspace-respektierend)
if command -v pnpm >/dev/null 2>&1; then
  echo "→ Installing workspace deps (pnpm)…" >&2
  pnpm install --no-frozen-lockfile
  git add pnpm-lock.yaml || true
  git commit -m "chore: regenerate pnpm-lock.yaml after merge #$PR" || true

  # 6) Build + (optional) Tests
  echo "→ Building frontend…" >&2
  pnpm -w -F @infoterminal/frontend build || true
  echo "→ Running frontend tests…" >&2
  if pnpm -w -F @infoterminal/frontend -s test; then
    echo "✓ Tests OK" >&2
  else
    echo "⚠ Tests haben Fehler – bitte Report prüfen" >&2
  fi
else
  echo "⚠ pnpm nicht gefunden – Überspringe Install/Build/Test" >&2
fi

# 7) Push
git push -u origin "$WORK"

echo "✓ Fertig: Branch $WORK bereit. Erstelle jetzt einen PR → main."

