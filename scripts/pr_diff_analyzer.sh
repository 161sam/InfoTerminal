#!/usr/bin/env bash
###############################################################################
# InfoTerminal – PR/Branch Diff & Merge-Conflict Analyzer
#  - Analysiert PRs/Branches (standardmäßig PRs 169 und 168)
#  - Holt Metadaten & Diffs (gh CLI wenn verfügbar)
#  - Simuliert Merge in Base (z.B. origin/main) + Cross-Merge beider PRs
#  - Generiert reports/DIFF_REPORT.md und druckt den Report auf stdout
#  - Idempotent (benutzt tmp-Branches, räumt auf)
###############################################################################
set -euo pipefail

# -------- Parameter --------
PRS="${PRS:-169 168}"              # PR-Nummern, Leerzeichen-getrennt
BASE_REF="${BASE_REF:-origin/main}" # Baseline zum Mergen/Simulieren
REPORT_DIR="reports"
TS="$(date +%Y%m%d-%H%M%S)"

mkdir -p "$REPORT_DIR"

# -------- Helpers --------
log() { printf "→ %s\n" "$*" >&2; }
warn() { printf "⚠ %s\n" "$*" >&2; }
die() { printf "✗ %s\n" "$*" >&2; exit 1; }

have() { command -v "$1" >/dev/null 2>&1; }

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
[ -n "$ROOT" ] || die "Kein Git-Repository gefunden."
cd "$ROOT"

CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
git fetch --all --prune --tags >/dev/null 2>&1 || true

have gh && GH_OK=1 || GH_OK=0
have jq && JQ_OK=1 || JQ_OK=0

# Datei-Header
REPORT_MD="$REPORT_DIR/DIFF_REPORT.md"
: > "$REPORT_MD"
{
  echo "# Diff & Merge-Conflict Report"
  echo
  echo "- Zeitpunkt: $(date -Is)"
  echo "- Base: \`$BASE_REF\`"
  echo "- Analyse von: \`$PRS\`"
  echo
} >> "$REPORT_MD"

# -------- Funktion: PR/Branch Materialisieren --------
# Erwartet: eine „ID“, die PR-Nummer oder Branch sein kann.
# Liefert:  VARS: HEAD_BRANCH, BASE_OF_PR, META_JSON, DIFF_PATH
materialize_ref() {
  local ref_id="$1"
  local work_branch=""
  local base_ref="$BASE_REF"
  local meta_json="$REPORT_DIR/ref-${ref_id}-meta.json"
  local diff_path="$REPORT_DIR/ref-${ref_id}.diff"

  if [ "$GH_OK" = 1 ] && [[ "$ref_id" =~ ^[0-9]+$ ]]; then
    # PR via gh
    log "PR #$ref_id: Metadaten abfragen"
    if [ "$JQ_OK" = 1 ]; then
      gh pr view "$ref_id" --json number,title,headRefName,baseRefName,mergeable,author,additions,deletions,changedFiles,url > "$meta_json"
      head_ref="$(jq -r '.headRefName' "$meta_json" 2>/dev/null || echo "")"
      base_ref="$(jq -r '.baseRefName' "$meta_json" 2>/dev/null || echo "$BASE_REF")"
    else
      gh pr view "$ref_id" --json number,title,headRefName,baseRefName,mergeable,author,additions,deletions,changedFiles,url > "$meta_json" || true
      head_ref="$(sed -n 's/.*"headRefName":"\([^"]*\)".*/\1/p' "$meta_json" | head -n1 || true)"
      base_ref="$(sed -n 's/.*"baseRefName":"\([^"]*\)".*/\1/p' "$meta_json" | head -n1 || echo "$BASE_REF")"
    fi

    # PR-Checkout in tmp-Branch (fork-sicher)
    work_branch="tmp/pr-${ref_id}"
    if git show-ref --verify --quiet "refs/heads/$work_branch"; then
      git branch -D "$work_branch" >/dev/null 2>&1 || true
    fi
    log "PR #$ref_id: checkout in $work_branch"
    gh pr checkout "$ref_id" -b "$work_branch" >/dev/null

    # Diff sichern
    log "PR #$ref_id: Diff speichern -> $diff_path"
    gh pr diff "$ref_id" > "$diff_path"

    printf "%s;%s;%s;%s\n" "$ref_id" "$work_branch" "$base_ref" "$meta_json"
  else
    # Behandle ref_id als lokalen Branch/Commit
    work_branch="$ref_id"
    git show-ref --verify --quiet "refs/heads/$work_branch" || die "Branch '$work_branch' existiert nicht."
    # diff ggü Base
    log "Branch $work_branch: Diff ggü $BASE_REF -> $diff_path"
    git diff "$BASE_REF"..."$work_branch" > "$diff_path"
    printf "%s;%s;%s;%s\n" "$ref_id" "$work_branch" "$base_ref" ""
  fi
}

# -------- Funktion: Merge-Simulation --------
# Simuliert Merge von $from_branch in $base_ref, listet Konflikte & Hunks
simulate_merge() {
  local base_ref="$1" from_branch="$2" tag="$3"
  local sim_branch="tmp/merge-sim-${tag}-${TS}"

  log "Simuliere Merge: $from_branch → $base_ref (Branch: $sim_branch)"
  git switch -C "$sim_branch" "$base_ref" >/dev/null 2>&1 || die "Konnte $base_ref nicht auschecken."
  set +e
  git merge --no-commit --no-ff "$from_branch" >/tmp/merge-${tag}.log 2>&1
  local rc=$?
  set -e

  local conflict_files
  conflict_files="$(git diff --name-only --diff-filter=U || true)"
  {
    echo "## Merge-Simulation: \`$from_branch\` → \`$base_ref\`"
    echo
    echo "- Exit Code: \`$rc\` (0=kein Konflikt)"
    echo "- Konfliktdateien:"
    if [ -n "$conflict_files" ]; then
      echo
      echo '```'
      echo "$conflict_files"
      echo '```'
      echo
      echo "### Konflikt-Hunks (Ausschnitte)"
      for f in $conflict_files; do
        echo "#### \`$f\`"
        # Zeige die Zeilen mit Konfliktmarkern + 3 Zeilen Kontext
        echo '```diff'
        nl -ba "$f" | sed -n '/<<<<<<<\|=======\|>>>>>>>/p' || true
        echo '```'
        echo
      done
    else
      echo "  (keine)"
    fi
    echo
  } >> "$REPORT_MD"

  # Aufräumen
  git merge --abort >/dev/null 2>&1 || true
  git switch - >/dev/null 2>&1 || git switch "$CURRENT_BRANCH" >/dev/null 2>&1 || true
  git branch -D "$sim_branch" >/dev/null 2>&1 || true
}

# -------- Verarbeitung --------
# 1) Materialisieren
declare -a REFS=()
declare -a WORK_BRANCHES=()
declare -a BASES=()
declare -a METAS=()

for ref in $PRS; do
  IFS=';' read -r rid wbranch base meta <<<"$(materialize_ref "$ref")"
  REFS+=("$rid"); WORK_BRANCHES+=("$wbranch"); BASES+=("${base:-$BASE_REF}"); METAS+=("$meta")
done

# 2) Zusammenfassung je Ref (geänderte Dateien, Größen, Top-Pfade)
{
  echo "## PR/Branch Zusammenfassung"
  echo
} >> "$REPORT_MD"

for i in "${!REFS[@]}"; do
  rid="${REFS[$i]}"; wbranch="${WORK_BRANCHES[$i]}"; base="${BASES[$i]}"; meta="${METAS[$i]}"
  echo "### $rid" >> "$REPORT_MD"
  if [ -n "$meta" ] && [ -f "$meta" ]; then
    echo "" >> "$REPORT_MD"
    echo "Metadaten:" >> "$REPORT_MD"
    echo "" >> "$REPORT_MD"
    echo '```json' >> "$REPORT_MD"
    cat "$meta" >> "$REPORT_MD"
    echo '```' >> "$REPORT_MD"
    echo "" >> "$REPORT_MD"
  fi
  # Datei-Liste und Stat
  echo "- Diff ggü \`$base\`:" >> "$REPORT_MD"
  echo '' >> "$REPORT_MD"
  echo '```' >> "$REPORT_MD"
  git diff --stat "$base...$wbranch" >> "$REPORT_MD" || true
  echo '```' >> "$REPORT_MD"
  echo '' >> "$REPORT_MD"
  echo "- Top geänderte Dateien:" >> "$REPORT_MD"
  echo '' >> "$REPORT_MD"
  echo '```' >> "$REPORT_MD"
  git diff --name-only "$base...$wbranch" | sort | sed 's/^/- /' | sed -n '1,100p' >> "$REPORT_MD" || true
  echo '```' >> "$REPORT_MD"
  echo '' >> "$REPORT_MD"
done

# 3) Merge-Simulation je Ref in Base (z.B. origin/main)
{
  echo "## Merge-Simulation in Base (\`$BASE_REF\`)"
  echo
} >> "$REPORT_MD"
for i in "${!REFS[@]}"; do
  simulate_merge "$BASE_REF" "${WORK_BRANCHES[$i]}" "base-${REFS[$i]}"
done

# 4) Cross-Merge-Simulation (Reihenfolgen A→B und B→A)
if [ "${#REFS[@]}" -ge 2 ]; then
  A="${WORK_BRANCHES[0]}"; AID="${REFS[0]}"; ABASE="${BASES[0]}"
  B="${WORK_BRANCHES[1]}"; BID="${REFS[1]}"; BBASE="${BASES[1]}"

  {
    echo "## Cross-Merge Simulation (Stacking)"
    echo
    echo "### Reihenfolge: $AID → $BID (auf Base: \`$ABASE\`)"
  } >> "$REPORT_MD"

  # Stack A dann B
  TMPA="tmp/stack-A-${TS}"
  git switch -C "$TMPA" "$ABASE" >/dev/null 2>&1 || die "Konnte $ABASE nicht auschecken."
  set +e
  git merge --no-commit --no-ff "$A" >/dev/null 2>&1
  rcA=$?
  set -e
  if [ $rcA -ne 0 ]; then
    {
      echo
      echo "- Konflikt bereits bei Merge von $AID in $ABASE"
      echo
    } >> "$REPORT_MD"
  else
    # nun B
    set +e
    git merge --no-commit --no-ff "$B" >/tmp/merge-stack-A-then-B.log 2>&1
    rcAB=$?
    set -e
    conf="$(git diff --name-only --diff-filter=U || true)"
    {
      echo
      echo "- Exit Code (B auf A): \`$rcAB\`"
      echo "- Konfliktdateien:"
      echo
      echo '```'
      [ -n "$conf" ] && echo "$conf" || echo "(keine)"
      echo '```'
      if [ -n "$conf" ]; then
        echo
        echo "#### Konflikt-Hunks (Ausschnitte)"
        for f in $conf; do
          echo "##### \`$f\`"
          echo '```diff'
          nl -ba "$f" | sed -n '/<<<<<<<\|=======\|>>>>>>>/p' || true
          echo '```'
        done
      fi
      echo
    } >> "$REPORT_MD"
  fi
  git merge --abort >/dev/null 2>&1 || true
  git switch - >/dev/null 2>&1 || git switch "$CURRENT_BRANCH" >/dev/null 2>&1 || true
  git branch -D "$TMPA" >/dev/null 2>&1 || true

  {
    echo "### Reihenfolge: $BID → $AID (auf Base: \`$BBASE\`)"
  } >> "$REPORT_MD"

  # Stack B dann A
  TMPB="tmp/stack-B-${TS}"
  git switch -C "$TMPB" "$BBASE" >/dev/null 2>&1 || die "Konnte $BBASE nicht auschecken."
  set +e
  git merge --no-commit --no-ff "$B" >/dev/null 2>&1
  rcB=$?
  set -e
  if [ $rcB -ne 0 ]; then
    {
      echo
      echo "- Konflikt bereits bei Merge von $BID in $BBASE"
      echo
    } >> "$REPORT_MD"
  else
    set +e
    git merge --no-commit --no-ff "$A" >/tmp/merge-stack-B-then-A.log 2>&1
    rcBA=$?
    set -e
    conf="$(git diff --name-only --diff-filter=U || true)"
    {
      echo
      echo "- Exit Code (A auf B): \`$rcBA\`"
      echo "- Konfliktdateien:"
      echo
      echo '```'
      [ -n "$conf" ] && echo "$conf" || echo "(keine)"
      echo '```'
      if [ -n "$conf" ]; then
        echo
        echo "#### Konflikt-Hunks (Ausschnitte)"
        for f in $conf; do
          echo "##### \`$f\`"
          echo '```diff'
          nl -ba "$f" | sed -n '/<<<<<<<\|=======\|>>>>>>>/p' || true
          echo '```'
        done
      fi
      echo
    } >> "$REPORT_MD"
  fi
  git merge --abort >/dev/null 2>&1 || true
  git switch - >/dev/null 2>&1 || git switch "$CURRENT_BRANCH" >/dev/null 2>&1 || true
  git branch -D "$TMPB" >/dev/null 2>&1 || true
fi

# 5) Kurze Risiko-Bewertung (heuristisch)
{
  echo "## Heuristische Risiko-Bewertung"
  echo
  echo "- Hohe Konfliktgefahr bei Dateien:"
  echo
  echo '```'
  git diff --name-only "$BASE_REF...${WORK_BRANCHES[0]}" 2>/dev/null || true
  git diff --name-only "$BASE_REF...${WORK_BRANCHES[1]:-}" 2>/dev/null || true
  echo '```'
  echo
  echo "- Besondere Aufmerksamkeit für:"
  echo "  - apps/frontend/src/components/layout/DashboardLayout.tsx (Layout, Theme, Sidebar)"
  echo "  - apps/frontend/src/styles/globals.css (Tailwind v4 & Theme-Base)"
  echo "  - apps/frontend/pages/_document.tsx (pre-hydration theme init)"
  echo "  - apps/frontend/src/lib/theme-provider.tsx (global theme state)"
  echo "  - apps/frontend/src/components/layout/Panel.tsx (dark-surface Konsistenz)"
  echo
} >> "$REPORT_MD"

# 6) Als Antwort in der Konsole ausgeben
echo "==================== BEGIN DIFF REPORT ===================="
cat "$REPORT_MD"
echo "===================== END DIFF REPORT ====================="

# 7) Optional: als PR-Kommentar posten (nur wenn gh vorhanden + PRs)
if [ "$GH_OK" = 1 ]; then
  for ref in $PRS; do
    if [[ "$ref" =~ ^[0-9]+$ ]]; then
      gh pr comment "$ref" --body-file "$REPORT_MD" >/dev/null 2>&1 || true
      log "Report als Kommentar an PR #$ref (falls Berechtigung vorhanden)."
    fi
  done
fi

# 8) Cleanup: tmp PR-Branches entfernen (wir haben sie nur für Analyse benötigt)
for ref in $PRS; do
  if git show-ref --verify --quiet "refs/heads/tmp/pr-$ref"; then
    git branch -D "tmp/pr-$ref" >/dev/null 2>&1 || true
  fi
done

log "Fertig. Report: $REPORT_MD"
