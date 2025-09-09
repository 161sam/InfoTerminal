#!/usr/bin/env bash
set -euo pipefail

# Runs Prettier only on a curated set of files (see scripts/prettier_safe.list).
# Skips unmatched globs quietly.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

have_jq=0
command -v jq >/dev/null 2>&1 && have_jq=1

mapfile -t GLOBS < "${ROOT}/scripts/prettier_safe.list"

FILES=()
for g in "${GLOBS[@]}"; do
  # Use git ls-files to respect repo tracking and .gitignore
  while IFS= read -r -d '' f; do
    FILES+=("$f")
  done < <(cd "$ROOT" && git ls-files -z "$g" 2>/dev/null || true)
done

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "[prettier-safe] no files matched; nothing to do."
  exit 0
fi

printf '%s\0' "${FILES[@]}" | xargs -0 npx -y prettier@3.3.3 --write --log-level warn --ignore-path "${ROOT}/.prettierignore"

echo "[prettier-safe] formatted ${#FILES[@]} files."
