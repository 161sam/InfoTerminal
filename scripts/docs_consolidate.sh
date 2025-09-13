#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
DRY="${DRY_RUN:-0}"
TS="$(date +%Y%m%d-%H%M%S)"
BRANCH_DEFAULT="chore/docs-consolidation-${TS}"

log(){ printf "==> %s\n" "$*"; }
doit(){ if [ "$DRY" = "1" ]; then echo "DRY: $*"; else eval "$@"; fi }

# ---------- 0) Vorbedingungen ----------
[ -d "$ROOT/.git" ] || { echo "Bitte im Repo-Root ausführen."; exit 1; }
[ -d "$ROOT/docs" ] || { echo "Kein docs/ gefunden."; exit 1; }

# ---------- 1) Branch anlegen ----------
CUR_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
TARGET_BRANCH="${TARGET_BRANCH:-$BRANCH_DEFAULT}"
if [ "$DRY" != "1" ]; then
  git fetch --all --prune --tags
  git switch -c "$TARGET_BRANCH" || git switch "$TARGET_BRANCH"
fi
log "Arbeitsbranch: $(git rev-parse --abbrev-ref HEAD)"

# ---------- 2) Zielstruktur definieren ----------
DOCS_DIR="$ROOT/docs"
DEV_DIR="$DOCS_DIR/dev"
ROADMAP_DIR="$DEV_DIR/roadmap"
CHECKLIST_DIR="$DEV_DIR/checklists"

doit "mkdir -p '$ROADMAP_DIR' '$CHECKLIST_DIR'"

# Kanonische Zieldateien
KAN_TODO="$ROADMAP_DIR/TODO-Index.md"          # zentrale Roadmap/ToDo
KAN_CHECKLIST="$CHECKLIST_DIR/Ticket-Checkliste.md"  # zentrale Checkliste
KAN_README="$DOCS_DIR/README.md"               # docs-Einstieg

# ---------- 3) Quellartefakte lokalisieren ----------
dup_candidates=()
while IFS= read -r -d '' f; do dup_candidates+=("$f"); done < <(
  find "$DOCS_DIR" -maxdepth 4 -type f \
    \( -iname "TODO-Index.md" -o -iname "Ticket-Checkliste.md" -o -iname "To-Build-Liste.md" \) -print0
)

# WORK-ON-new_docs Inhalte sammeln
NEW_DOCS_DIR="$DOCS_DIR/WORK-ON-new_docs"
newdocs_candidates=()
if [ -d "$NEW_DOCS_DIR" ]; then
  while IFS= read -r -d '' f; do newdocs_candidates+=("$f"); done < <(find "$NEW_DOCS_DIR" -type f -print0)
fi

log "Gefundene Duplikate: ${#dup_candidates[@]}"
log "Gefundene WORK-ON-new_docs Dateien: ${#newdocs_candidates[@]}"

# ---------- 4) Merge-Helfer ----------
merge_md_unique(){
  # $1 = Zieldatei, $2..$n = Quellen
  local out="$1"; shift
  local tmp="$(mktemp)"
  : > "$tmp"

  # dedupliziere per Überschrift & Hash
  declare -A seen
  for src in "$@"; do
    [ -f "$src" ] || continue
    # Abschnittsweise: einfache Heuristik – ganze Datei, Überschriften werden entdoppelt
    while IFS= read -r line; do
      key="$(printf "%s" "$line" | sed 's/[[:space:]]\+/_/g' | tr '[:upper:]' '[:lower:]' | md5sum | cut -d' ' -f1)"
      if [[ "$line" =~ ^\# ]]; then
        if [ -n "${seen[$key]:-}" ]; then
          continue
        else
          seen[$key]=1
        fi
      fi
      printf "%s\n" "$line" >> "$tmp"
    done < "$src"
    printf "\n" >> "$tmp"
  done

  if [ "$DRY" = "1" ]; then
    echo "DRY: würde mergen -> $out"
  else
    mkdir -p "$(dirname "$out")"
    cp "$tmp" "$out"
    echo "<!-- merged:${TS} -->" >> "$out"
  fi
  rm -f "$tmp"
}

# ---------- 5) ToDo/Roadmap zusammenführen ----------
# Quellen nach Typ trennen
todo_sources=()
checklist_sources=()
for f in "${dup_candidates[@]}"; do
  base="$(basename "$f")"
  case "$base" in
    TODO-Index.md|To-Build-Liste.md) todo_sources+=("$f") ;;
    Ticket-Checkliste.md)            checklist_sources+=("$f") ;;
  esac
done

# Merge ausführen
if [ "${#todo_sources[@]}" -gt 0 ]; then
  log "Mergen TODO-Index → $KAN_TODO"
  merge_md_unique "$KAN_TODO" "${todo_sources[@]}"
fi
if [ "${#checklist_sources[@]}" -gt 0 ]; then
  log "Mergen Ticket-Checkliste → $KAN_CHECKLIST"
  merge_md_unique "$KAN_CHECKLIST" "${checklist_sources[@]}"
fi

# ---------- 6) WORK-ON-new_docs integrieren ----------
for f in "${newdocs_candidates[@]}"; do
  rel="${f#$NEW_DOCS_DIR/}"
  target="$DOCS_DIR/$rel"
  log "Integriere $rel"
  doit "mkdir -p '$(dirname "$target")'"
  doit "cp -n '$f' '$target' || true"
done

# ---------- 7) Verweise/Links reparieren ----------
# Ziel: alte Pfade auf neue Kanon-Pfade umschreiben
# Beispiele:
#  - */Checkliste.md → Verweise auf TODO-Index.md → ../roadmap/TODO-Index.md
#  - allgemeine Verweise auf To-Build-Liste.md → roadmap/TODO-Index.md (integriert)
fix_ref(){
  local file="$1"
  # nur Markdown
  grep -qE '\.md\)' "$file" || return 0

  sed_cmds=(
    # TODO-Index relative→kanonisch
    "-E s#\\(([^)]*)TODO-Index\\.md\\)#(../roadmap/TODO-Index.md)#g"
    "-E s#\\(([^)]*)To-Build-Liste\\.md\\)#(../roadmap/TODO-Index.md)#g"
    "-E s#\\(([^)]*)Ticket-Checkliste\\.md\\)#(../checklists/Ticket-Checkliste.md)#g"
    # .bak Referenzen entfernen
    "-E s#\\(([^)]*)README\\.md\\.bak\\.new\\)#(README.md)#g"
  )

  local tmp="$(mktemp)"
  cp "$file" "$tmp"
  for expr in "${sed_cmds[@]}"; do
    sed -i $expr "$tmp"
  done

  if ! diff -q "$file" "$tmp" >/dev/null 2>&1; then
    if [ "$DRY" = "1" ]; then
      echo "DRY: würde Links fixen in $file"
    else
      mv "$tmp" "$file"
    fi
  else
    rm -f "$tmp"
  fi
}

while IFS= read -r -d '' md; do
  fix_ref "$md"
done < <(find "$DOCS_DIR" -type f -name '*.md' -print0)

# ---------- 8) README.md (Wurzel & docs/) prüfen ----------
# Falls es eine docs/README.md.bak.new gibt, mit docs/README.md mergen oder verwerfen
if [ -f "$DOCS_DIR/README.md.bak.new" ]; then
  log "Found docs/README.md.bak.new → integriere priorisierte Abschnitte (Titel/Intro), sonst verwerfen"
  if [ "$DRY" != "1" ]; then
    # Primitive Heuristik: Wenn docs/README.md klein ist (<20 Zeilen), ersetze; sonst .bak.new löschen
    if [ ! -f "$KAN_README" ] || [ "$(wc -l < "$KAN_README")" -lt 20 ]; then
      cp "$DOCS_DIR/README.md.bak.new" "$KAN_README"
      echo "<!-- adopted from README.md.bak.new @ ${TS} -->" >> "$KAN_README"
    fi
  fi
fi

# ---------- 9) Bereinigung: .bak / .bak.* / WORK-ON-new_docs ----------
# Nur löschen, wenn Inhalte übernommen wurden
cleanup_paths=()
[ -d "$NEW_DOCS_DIR" ] && cleanup_paths+=("$NEW_DOCS_DIR")
while IFS= read -r -d '' b; do cleanup_paths+=("$b"); done < <(find "$DOCS_DIR" -type f -name '*.bak*' -print0)

for p in "${cleanup_paths[@]}"; do
  log "Cleanup: $p"
  doit "rm -rf '$p'"
done

# ---------- 10) Dead link check (einfach) ----------
log "Prüfe auf offensichtliche tote Links (nur einfache Prüfung)..."
while IFS= read -r -d '' md; do
  while read -r link; do
    target="${link#*(}"
    target="${target%)*}"
    [[ "$target" == http* ]] && continue
    # relative Pfade
    [ -f "$(dirname "$md")/$target" ] || echo "WARN: Broken link in $md -> $target"
  done < <(grep -oE '\([^)]+\.md\)' "$md" || true)
  done < <(find "$DOCS_DIR" -type f -name '*.md' -print0)

# ---------- 11) Git add/commit ----------
if [ "$DRY" != "1" ]; then
  git add docs
  if ! git diff --cached --quiet; then
    git commit -m "chore(docs): consolidate roadmap/checklists, fix refs, cleanup WORK-ON-new_docs and .bak"
    log "Commit erstellt."
  else
    log "Keine Änderungen zu committen."
  fi
  git status --short
fi

log "Fertig. DRY_RUN=${DRY}"
