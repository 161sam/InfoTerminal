# Roadmap Intelligence – Phase 2 Kick-off

_Phase 2 start date: 2025-09-23_

This document distils the active execution plan for packages A–L, aligning the roadmap narrative with the generated inventory and
`ROADMAP_STATUS.md`. Updates are idempotent – rerun the planning scripts to refresh artefacts without duplicating content.

## Prioritised Package Order

| Wave | Active Packages | Key Outcomes | Dependencies & Risk Notes |
| --- | --- | --- | --- |
| Wave 1 (In Progress) | **A – Ontologie & Graph**, **F – Dossier & Collaboration** | Graph analytics endpoints (degree, Louvain, shortest path) with dossier subgraph exports; Dossier-Lite MD/PDF templates + shared notes MVP. | Unlocks Search → Graph → Dossier demo flow; dossier export relies on graph subgraph hook. |
| Wave 2 | **B – NLP & Resolver**, **C – Geospatial** | Relation extraction + entity linking feeding graph; geospatial overlays consuming node metadata. | Requires Wave 1 graph metrics and dossier export to contextualise outputs. |
| Wave 3 | **G – Plugins**, **D – Daten-Ingest & Workflows** | Plugin registry + nmap example; ingest automation hooking NiFi/n8n. | Builds on graph observability and dossier pipelines from Waves 1–2. |
| Wave 4 | **H – AI-Agenten**, **I – Externe Feeds** | Hardened agent orchestration + feed connectors with monitoring. | Needs plugin + ingest infrastructure from Wave 3. |
| Wave 5 | **J – Performance & Infra**, **K – Frontend & UX** | Infra hardening, OIDC UX updates, performance tuning. | Executes once core analytics + collaboration stable. |
| Wave 6 | **L – Doku & Tests**, **Hardening**, **Release** | Documentation refresh, security validation, release playbooks. | Final consolidation after feature delivery. |

## Wave 1 Deliverables Snapshot

- **Analytics Endpoints**: `/graphs/analysis/degree`, `/graphs/analysis/communities`, `/graphs/analysis/shortest-path` with Prometheus metrics `graph_analysis_queries_total`, `graph_analysis_duration_seconds_bucket`.
- **Dossier Hook**: `/graphs/analysis/subgraph-export` streaming JSON + Markdown for Dossier-Lite ingestion.
- **Dossier-Lite**: `/dossier/export` generating Markdown/PDF using templates in `examples/dossier/`, triggered from Search or Graph contexts.
- **Collaboration MVP**: Feature-flagged notes endpoint emitting audit logs to Loki-compatible sinks.
- **Dashboards**:
  - Superset dataset + dashboard exports under `apps/superset/assets/*graph_analytics_mvp*`.
  - Grafana dashboard `grafana/dashboards/graph-analytics-mvp.json` tracking query rate, duration p95, subgraph exports.
- **Tests & Gates**: Smoke suite `test_infoterminal_v030_features.sh --suite graph-dossier`, analytics pytest coverage, inventory regeneration script.
- **Observability Review**: Findings captured in `reports/architecture/phase2-wave1.md` once both packages meet DoD.

## Governance Guardrails

1. **Concurrency Limit**: Maximum two packages active; next wave unlocked only after all four delivery gates report green.
2. **Idempotent Assets**: CLI commands, dashboards, and export scripts must tolerate re-import without duplication (`apps/superset/assets/scripts/import.sh`).
3. **Feature Flags Default Off**: Graph write toggles, collaboration notes, and dossier hooks remain disabled until readiness checks pass.
4. **Documentation Sync**: README demo script references Superset + Grafana artefacts; `DOCS_DIFF.md` entries reference this roadmap for alignment.
5. **Metrics Coverage**: New counters/histograms registered under `/metrics` with labels (`algorithm`, `status`, `format`). Grafana alert rules inherit from `api-slo` defaults.

## Execution Artefacts

- [Iteration Plan](../backlog/phase2/ITERATION-01_PLAN.md)
- [Wave 1 DoD Checklist](../backlog/phase2/WAVE1_DOD_CHECKLIST.md)
- [Status Dashboard](../ROADMAP_STATUS.md)
- [Inventory Generation Script](../scripts/generate_inventory.py)

Maintain this document alongside `STATUS.md` to ensure roadmap transparency for stakeholders and reviewers.
