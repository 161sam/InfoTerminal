#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
[ -d "$ROOT/.git" ] || { echo "Bitte im Repo-Root ausführen"; exit 1; }

DRY="${DRY_RUN:-0}"
TS="$(date +%Y%m%d-%H%M%S)"
BRANCH="${TARGET_BRANCH:-chore/docs-v0.2-update-${TS}}"

log(){ printf "==> %s\n" "$*"; }
doit(){ if [ "$DRY" = "1" ]; then echo "DRY: $*"; else eval "$@"; fi }

DOCS_DIR="$ROOT/docs"
LEGACY_DIR="$DOCS_DIR/LEGACY"
DEV_DIR="$DOCS_DIR/dev"

mkdir -p "$DOCS_DIR" "$LEGACY_DIR" "$DEV_DIR"

# ---------- 0) Branch ----------
if [ "$DRY" != "1" ]; then
  git fetch --all --prune --tags
  git switch -c "$BRANCH" || git switch "$BRANCH"
fi
log "Branch: $(git rev-parse --abbrev-ref HEAD)"

# ---------- 1) README Sprachwechsel finalisieren ----------
# Regel:
# - Wenn docs/README.md.bak.new existiert → nach README.md übernehmen (DE).
# - Bestehendes README.md (vermutlich EN) sichern als README.en.md, falls es englisch ist oder falls bak.new existierte.
DE_BAK="$DOCS_DIR/README.md.bak.new"
README_DE="$DOCS_DIR/README.md"
README_EN="$DOCS_DIR/README.en.md"

is_probably_english(){
  # Heuristik: wenig Umlaute/DE-Stoppwörter → EN
  local f="$1"
  grep -qiE '\b(the|and|for|with|build|setup|deploy|feature|roadmap|contribution)\b' "$f" && return 0
  return 1
}

if [ -f "$DE_BAK" ]; then
  log "DE Entwurf gefunden: $DE_BAK → canonical README.md (DE)"
  if [ -f "$README_DE" ] && [ "$DRY" != "1" ]; then
    cp "$README_DE" "$README_DE.$TS.bak" || true
  fi
  doit "cp '$DE_BAK' '$README_DE'"
  # Wenn bisheriges README eher EN war → README.en.md sichern
  if [ -f "$README_DE.$TS.bak" ] && is_probably_english "$README_DE.$TS.bak"; then
    log "Sichere alte EN-README nach README.en.md"
    if [ "$DRY" != "1" ]; then
      cp "$README_DE.$TS.bak" "$README_EN"
      printf "\n> This file was preserved from pre-v0.2 as the English README. See docs/dev for developer docs.\n" >> "$README_EN"
    fi
  fi
  # bak.new entfernen
  doit "rm -f '$DE_BAK'"
fi

# ---------- 2) Übergangsartefakte entfernen (.bak) ----------
while IFS= read -r -d '' f; do
  log "Cleanup transitional artifact: $f"
  doit "rm -f '$f'"
done < <(find "$DOCS_DIR" -type f -name '*.bak' -print0)

# ---------- 3) AGENTS.md auf v0.2 heben ----------
AGENTS="$ROOT/AGENTS.md"
AGENTS_ARCHIVE="$LEGACY_DIR/AGENTS.v0.1.archive.md"
AGENTS_TMP="$(mktemp)"

AGENTS_TEMPLATE_EN='
# AGENTS — v0.2 (Developer Guide)

> Status: **Active** for v0.2.  
> Language: **English** (developer docs).  
> For product/user docs in German see `docs/`.

## Purpose
Define how AI automation (Codex/Claude/etc.) contributes to InfoTerminal:
- Keep **docs & code in sync** (idempotent scripts, small PRs).
- Implement **v0.2 must-haves**: Ontology layer, Graph algorithms (centrality/communities/pathfinding), NLP v1 (NER/Relations/Summary), OAuth2/OIDC, Observability profile, Dossier-Lite, NiFi ingestion + n8n playbooks, Flowise-based Assistant, Geospatial layer.

## Operating Principles
- **Idempotent by default**: prompts create rerunnable scripts with `DRY_RUN`.
- **Conventional Commits**; one logical change per PR.
- **Tests & docs first-class**: new services ship with healthz/readyz, metrics (opt-in), minimal tests and README updates.
- **No standard host ports**: respect project port policy (Frontend 3411; Observability 3412–3416; Flowise 3417; Dockerized apps e.g. search-api 8611, graph-api 8612). Use `patch_ports.sh` as source of truth.

## Tooling & Targets
- **Services**: search-api, graph-api, graph-views, doc-entities, gateway/OPA.
- **Data**: OpenSearch, Neo4j, Postgres.
- **Orchestration**: Docker Compose (infra), local dev scripts (dev_up.sh), future K8s/Helm.
- **Automation**: NiFi (ingest), n8n (playbooks), Flowise (Assistant).
- **Dashboards**: Superset (BI), Grafana (metrics/logs/traces).

## Guardrails
- Never commit secrets; use `.env` + `.env.example`.
- Keep **/healthz**/**/readyz** consistent; readiness gates before handling.
- Quiet OTEL by default in dev; enable via env flags.
- Respect **no standard host ports** policy across compose/helm/frontend.

## v0.2 Roadmap — Agent Work Packages
1. **Ontology Layer**: canonical schema (entities/relations), mappings; docs + examples.
2. **Graph Algorithms v1**: degree, betweenness, Louvain; API endpoints; FE visualization.
3. **NLP v1**: NER + Relation Extraction + Summaries; doc-entities service + FE highlighting.
4. **OAuth2/OIDC**: JWT at gateway; scopes/claims; minimal FE sign-in.
5. **Observability Profile**: Prometheus/Grafana/Loki/Tempo wiring; structured JSON logs; request IDs; basic alerts.
6. **Dossier-Lite**: build JSON/Markdown → export/download; FE action & templates.
7. **NiFi/n8n/Flowise**: demo ingest flows; 1–2 playbooks; Assistant with tools (search, graph, docs).
8. **Geospatial Layer**: MapLibre/Leaflet; GeoJSON ingest; FE overlays.

## How to Contribute (Agent)
- Produce **scripts + patches**; always idempotent; include `--help`, comments, and rollback hints.
- Update docs **in the same PR**; add short usage examples.
- Add smoke tests or curlable examples for new endpoints.

## Notes
- This document supersedes the pre-v0.2 AGENTS.md. The old version is archived under `docs/LEGACY/`.
'

if [ -f "$AGENTS" ]; then
  # Archivieren, falls alte v0.1-Variante
  if grep -qiE 'v0\.1|pre' "$AGENTS"; then
    log "Archiviere alte AGENTS.md → $AGENTS_ARCHIVE"
    if [ "$DRY" != "1" ]; then
      mkdir -p "$LEGACY_DIR"
      cp "$AGENTS" "$AGENTS_ARCHIVE"
      printf "\n> Archived on %s. Superseded by v0.2.\n" "$TS" >> "$AGENTS_ARCHIVE"
    fi
  fi
fi

# Neue v0.2-Version schreiben (idempotent overwrite)
log "Schreibe AGENTS.md v0.2"
if [ "$DRY" != "1" ]; then
  printf "%s\n" "$AGENTS_TEMPLATE_EN" > "$AGENTS"
fi

# ---------- 4) Historische Doku markieren & optional verschieben ----------
banner_legacy='
> **Legacy Notice (v0.1)**  
> This document describes pre-v0.2 behavior and is kept for historical reference.  
> See the updated docs in `docs/` and the v0.2 roadmap for current guidance.
'

add_legacy_banner_if_needed(){
  local f="$1"
  grep -q 'Legacy Notice (v0.1)' "$f" && return 0
  printf "\n%s\n" "$banner_legacy" | cat - "$f" > "$f.tmp" && mv "$f.tmp" "$f"
}

# Heuristik: markiere Dateien, die offensichtlich v0.1-docs sind
while IFS= read -r -d '' f; do
  if grep -qE 'v0\.1|pre\-v0\.2|0\.1\.' "$f"; then
    log "Markiere als Legacy: $f"
    if [ "$DRY" != "1" ]; then
      add_legacy_banner_if_needed "$f"
      # Option: in LEGACY verschieben, falls noch nicht dort
      case "$f" in
        $LEGACY_DIR/*) : ;; # already there
        *)
          rel="${f#$DOCS_DIR/}"
          tgt="$LEGACY_DIR/$rel"
          mkdir -p "$(dirname "$tgt")"
          mv "$f" "$tgt"
          ;;
      esac
    fi
  fi

done < <(find "$DOCS_DIR" -type f -name '*.md' -print0)

# ---------- 5) Link-Fixes ----------
# - AGENTS archive Link
# - Entferne Verweise auf .bak.new
fix_links_file(){
  local file="$1"
  local tmp="$file.tmp"
  cp "$file" "$tmp"

  sed -i -E \
    -e 's#\(README\.md\.bak\.new\)#(README.md)#g' \
    -e 's#\(AGENTS\.md\.old\)#(docs/LEGACY/AGENTS.v0.1.archive.md)#g' \
    "$tmp" || true

  if ! diff -q "$file" "$tmp" >/dev/null 2>&1; then
    if [ "$DRY" = "1" ]; then
      echo "DRY: würde Links fixen in $file"
      rm -f "$tmp"
    else
      mv "$tmp" "$file"
    fi
  else
    rm -f "$tmp"
  fi
}

while IFS= read -r -d '' f; do
  fix_links_file "$f"
done < <(find "$DOCS_DIR" -type f -name '*.md' -print0)

# ---------- 6) Übersicht LEGACY Index ----------
LEGACY_IDX="$LEGACY_DIR/README.md"
if [ "$DRY" != "1" ]; then
  {
    echo "# Legacy Documents (pre-v0.2)"
    echo
    echo "> This folder lists historical documents kept for reference."
    echo
    find "$LEGACY_DIR" -type f -name '*.md' -maxdepth 3 | sort | while read -r p; do
      rel="${p#$DOCS_DIR/}"
      echo "- [$rel]($rel)"
    done
  } > "$LEGACY_IDX"
fi

# ---------- 7) Git add/commit ----------
if [ "$DRY" != "1" ]; then
  git add AGENTS.md docs
  if ! git diff --cached --quiet; then
    git commit -m "docs(v0.2): update AGENTS.md, finalize DE README, mark legacy v0.1 docs, cleanup transitions"
    log "Commit erstellt."
  else
    log "Keine Änderungen zu committen."
  fi
  git status --short
fi

log "Fertig. DRY_RUN=${DRY}"
