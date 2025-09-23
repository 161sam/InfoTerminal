# Architecture & Observability Review – Phase 2 Wave 1

_This template captures findings once packages A (Ontologie & Graph) and F (Dossier & Collaboration) meet their MVP Definition of Done._

## Session Metadata

- **Date:** YYYY-MM-DD
- **Participants:** <!-- add names/roles -->
- **Scope:** Graph analytics endpoints, dossier export pipeline, shared notes feature flag, observability assets (Grafana + Superset)
- **Inputs Reviewed:**
  - `/metrics` outputs for graph-api, graph-views, dossier service
  - Superset dashboard `graph_analytics_mvp`
  - Grafana dashboard `graph-analytics-mvp.json`
  - Smoke E2E logs (`test_infoterminal_v030_features.sh --suite graph-dossier`)

## Findings

| Category | Observation | Impact | Action Item | Owner | Due |
| --- | --- | --- | --- | --- | --- |
| Architecture | <!-- e.g. Neo4j timeout defaults need tuning --> |  |  |  |  |
| Observability |  |  |  |  |  |
| Security / Policy |  |  |  |  |  |
| Docs & Demo |  |  |  |  |  |

## Decisions & Follow-ups

- [ ] All critical findings captured as GitHub issues (label `architecture-review`, `pkg-A-graph`, `pkg-F-dossier`).
- [ ] Metrics thresholds agreed and encoded into Grafana alert rules (link to PR/commit).
- [ ] README demo script updated if flow changes.

## Attachments

- Paste Prometheus query snippets, Grafana panel screenshots, or Superset exports as needed.
- Link to raw logs (`reports/logs/phase2-wave1/*.log`) once generated.

> ✅ **Idempotent usage:** Re-open this file after each review rerun; append dated entries instead of duplicating templates.
