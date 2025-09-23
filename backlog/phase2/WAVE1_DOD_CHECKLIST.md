# Phase 2 – Wave 1 DoD Checklist

_This checklist is idempotent: rerun after each merge to confirm gates remain green. Update issue references when tasks close._

> 📋 **Wave source of truth:** See [`PACKAGE_SEQUENCE.yaml`](PACKAGE_SEQUENCE.yaml) for the authoritative ordering,
> gates, and dependencies powering this checklist.

## Increment Tracking (Wave 1)

| Increment | Package | Status | Owner / Notes |
| --- | --- | --- | --- |
| A-1 | Ontologie & Graph | ☐ open | Validate analytics endpoints, pagination + metrics tests |
| A-2 | Ontologie & Graph | ☐ blocked | Depends on A-1 fixtures and metrics wiring |
| A-3 | Ontologie & Graph | ☐ open | Dashboard artefacts + docs refresh |
| F-1 | Dossier & Collaboration | ☐ open | Export service + templates |
| F-2 | Dossier & Collaboration | ☐ open | Notes MVP + metrics instrumentation |
| F-3 | Dossier & Collaboration | ☐ open | Docs/demo/smoke extension |

> ✅ Update status column (`☐` → `☑`) as increments close; reruns keep table idempotent.

## Package A – Ontologie & Graph (MVP)

### Increment A-1 – Analytics Endpoint Hardening
- [ ] `/graphs/analysis/degree` endpoint paginates + enforces timeout guardrails (pytest coverage `services/graph-api/tests/test_analysis_routes.py`).
- [ ] `/graphs/analysis/communities` exposes Louvain output with `community_id` column and Prometheus counters `graph_analysis_queries_total{algorithm="louvain"}` (validated via `services/graph-api/tests/test_analysis_routes.py`).
- [ ] `/graphs/analysis/shortest-path` returns deterministic fixture path ≤ konfiguriertem Hop-Limit und berichtet Dauer-Histogramm (`graph_analysis_duration_seconds_bucket`).

### Increment A-2 – Subgraph Export Hook
- [ ] Subgraph export endpoint (`/graphs/analysis/subgraph-export`) streams JSON + Markdown payload, increments `graph_subgraph_exports_total`.
- [ ] CLI/Docs snippet (`cli it graph export --case-id ...`) published for dossier pipeline integration.

### Increment A-3 – Observability & Dashboards
- [ ] Superset dashboard `graph_analytics_mvp` deployed via `apps/superset/assets/scripts/import.sh` und in README-Demo verlinkt.
- [ ] Grafana dashboard `graph-analytics-mvp.json` imported to observability stack.
- [ ] Smoke E2E (`scripts/smoke_graph_analysis.sh`, `scripts/smoke_graph_views.sh`) validieren Query → Subgraph → Dossier-Export.

## Package F – Dossier & Collaboration (MVP)

### Increment F-1 – Dossier Export Service
- [ ] `/dossier/export` generiert Markdown- und PDF-Artefakte mit Templates aus `examples/dossier/` (Smoke-Test `services/collab-hub/tests/test_dossier.py`).
- [ ] CLI command + sample exports dokumentiert; README referenziert Templates & Flags.

### Increment F-2 – Notes & Metrics MVP
- [ ] Feature-flagged notes endpoint persistiert fallbasierte Notizen mit Audit-Einträgen in `CH_AUDIT_PATH`-Logdateien.
- [ ] Metrics exposed: `dossier_exports_total`, `dossier_export_duration_seconds_bucket`, `collab_notes_total` (siehe `services/collab-hub/app/main.py`).
- [ ] Grafana stat panel reflects dossier export counters on the `graph-analytics-mvp` dashboard.

### Increment F-3 – Docs & Demo
- [ ] Superset dataset `graph_analytics_mvp` provides dossier-ready analytics context (centrality histogram + community count).
- [ ] README demo script documents Search → Graph → Dossier export walkthrough.
- [ ] Architecture/Observability review notes captured in `reports/architecture/phase2-wave1.md` post-completion.

## Gates Verification

- [ ] `scripts/generate_inventory.py` run post-merge (Inventory/Policy gate).
- [ ] `/metrics`, `/healthz`, `/readyz` endpoints verified via `scripts/check_gates.sh` (Health gate).
- [ ] Docs regenerated where inventories changed (API/Docs gate).
- [ ] Smoke E2E suite green in CI (`test_infoterminal_v030_features.sh`).
