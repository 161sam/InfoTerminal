#!/usr/bin/env bash
set -euo pipefail

CSS="apps/frontend/src/styles/globals.css"
ERR=0

echo "▶ Tailwind v4 guard: Prüfe verbotene @apply-Nutzungen & alte Opacity-Utilities"

# 1) @apply darf keine Custom-Klassen referenzieren (Liste erweiterbar)
if grep -nE '@apply\s+(heading|btn|input|card|select|textarea)\b' "$CSS"; then
  echo "✖ Verbotene @apply-Verwendung gefunden (Custom-Klasse)."
  ERR=1
fi

# 2) Alte Opacity-Utilities in @apply (bg-opacity-*, text-opacity-*, border-opacity-*)
if grep -nE '@apply[^;]*\b((bg|text|border|divide|placeholder)-opacity-[0-9]+)\b' "$CSS"; then
  echo "✖ Alte *-opacity-* Utilities in @apply gefunden. In CSS bitte CSS-Alpha (rgb/rgba) nutzen."
  ERR=1
fi

# 3) Nicht-existierende v4 Utilities (z. B. resize-vertical)
if grep -nE '@apply[^;]*\b(resize-vertical|resize-horizontal)\b' "$CSS"; then
  echo "✖ Ungültige Resize-Utility in @apply (nutze resize, resize-x, resize-y, resize-none)."
  ERR=1
fi

if [ "$ERR" -ne 0 ]; then
  echo "⚠ Bitte beheben – Build abgebrochen."
  exit 1
fi

echo "✔ Tailwind v4 guard: OK"
