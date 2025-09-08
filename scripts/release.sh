mkdir -p scripts
cat > scripts/release.sh <<'BASH'
#!/usr/bin/env bash
set -euo pipefail

# Usage:
#  scripts/release.sh [-v vX.Y.Z] [-r owner/repo] [--rc] [--notes path] [--assets "path1 path2 ..."]
#
# Examples:
#  scripts/release.sh -v v0.2.0
#  scripts/release.sh -v v0.2.1 --assets "scripts/smoke_graph_views.sh services/graph-views/samples/people.csv"
#  scripts/release.sh -v v0.3.0-rc.1 --rc

REPO_DEFAULT="161sam/InfoTerminal"
VERSION=""
REPO="${REPO_DEFAULT}"
NOTES_FILE=""
ASSETS=""
IS_RC=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -v|--version) VERSION="$2"; shift 2;;
    -r|--repo)    REPO="$2"; shift 2;;
    --rc)         IS_RC=1; shift;;
    --notes)      NOTES_FILE="$2"; shift 2;;
    --assets)     ASSETS="$2"; shift 2;;
    -h|--help)
      grep '^# ' "$0" | sed 's/^# //'; exit 0;;
    *) echo "Unknown arg: $1"; exit 2;;
  esac
done

if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: gh CLI not found. Install via https://cli.github.com/" >&2
  exit 1
fi

# Determine version:
if [[ -z "${VERSION}" ]]; then
  if [[ -f VERSION ]]; then
    VERSION="v$(tr -d ' \n' < VERSION)"
  else
    echo "ERROR: no version provided and no VERSION file found." >&2
    exit 1
  fi
fi

# Basic repo state checks
git fetch --tags origin >/dev/null 2>&1 || true
if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: Working tree not clean. Commit or stash first." >&2
  exit 1
fi

# Create release notes file if not supplied
TMP_NOTES=""
if [[ -z "${NOTES_FILE}" ]]; then
  TMP_NOTES="$(mktemp)"
  VER_NO_V="${VERSION#v}"
  if [[ -f CHANGELOG.md ]]; then
    awk -v ver="${VER_NO_V}" '
      BEGIN{show=0}
      tolower($0) ~ "^##[[:space:]]*\\[?"ver"\\]?" {show=1; next}
      show && tolower($0) ~ "^##[[:space:]]*\\[" {exit}
      show {print}
    ' CHANGELOG.md > "${TMP_NOTES}" || true
  fi
  if [[ ! -s "${TMP_NOTES}" ]]; then
    echo "Release ${VERSION}" > "${TMP_NOTES}"
  fi
  NOTES_FILE="${TMP_NOTES}"
fi

# Create tag if missing
if ! git rev-parse "${VERSION}" >/dev/null 2>&1; then
  git tag -a "${VERSION}" -m "Release ${VERSION}"
  git push origin "${VERSION}"
else
  echo "Tag ${VERSION} already exists."
fi

# Create GitHub release if missing
if ! gh release view -R "${REPO}" "${VERSION}" >/dev/null 2>&1; then
  args=(release create "${VERSION}" -R "${REPO}" --title "InfoTerminal ${VERSION}" --notes-file "${NOTES_FILE}")
  (( IS_RC == 1 )) && args+=(--prerelease)
  gh "${args[@]}"
else
  echo "Release ${VERSION} already exists on GitHub."
fi

# Upload assets if provided
if [[ -n "${ASSETS}" ]]; then
  # shellcheck disable=SC2086
  gh release upload -R "${REPO}" "${VERSION}" ${ASSETS}
fi

# Cleanup
[[ -n "${TMP_NOTES}" ]] && rm -f "${TMP_NOTES}"
echo "Done: ${VERSION}"
BASH
chmod +x scripts/release.sh
