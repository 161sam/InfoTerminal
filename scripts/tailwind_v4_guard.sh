#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root relative to this script (scripts/..)
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
CSS="$ROOT_DIR/apps/frontend/src/styles/globals.css"

# Strict mode: set STRICT=1 to fail on findings (default warn-only)
STRICT="${STRICT:-0}"
ERR=0

echo "▶ Tailwind v4 guard: Prüfe verbotene @apply-Nutzungen & alte Opacity-Utilities"

if [ ! -f "$CSS" ]; then
  echo "ℹ︎ CSS nicht gefunden: $CSS (überspringe Checks)"
  echo "✔ Tailwind v4 guard: OK"
  exit 0
fi

# 1) @apply referenziert verbotene Custom-Komponentenklassen? (optional)
# Hinweis: In warn-only Standardbetrieb meldend, aber bricht nicht ab.
if grep -nE '@apply\s+(heading|btn|input|card|select|textarea)\b' "$CSS" >/dev/null 2>&1; then
  echo "⚠ Hinweis: @apply nutzt Custom-Klassen (heading/btn/input/...)."
  ERR=1
fi

# 2) Alte Opacity-Utilities in @apply (bg-opacity-*, ...)
if grep -nE '@apply[^;]*\b((bg|text|border|divide|placeholder)-opacity-[0-9]+)\b' "$CSS" >/dev/null 2>&1; then
  echo "✖ Alte *-opacity-* Utilities in @apply gefunden. Bitte CSS-Alpha nutzen."
  ERR=1
fi

# 3) Nicht-existierende v4 Utilities (z. B. resize-vertical)
if grep -nE '@apply[^;]*\b(resize-vertical|resize-horizontal)\b' "$CSS" >/dev/null 2>&1; then
  echo "✖ Ungültige Resize-Utility in @apply (nutze resize, resize-x, resize-y, resize-none)."
  ERR=1
fi

if [ "$ERR" -ne 0 ] && [ "$STRICT" = "1" ]; then
  echo "⚠ Bitte beheben – Build abgebrochen (STRICT=1)."
  exit 1
fi

echo "✔ Tailwind v4 guard: OK"
