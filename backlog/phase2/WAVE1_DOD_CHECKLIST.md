# Phase 2 – Wave 1 DoD Checklist

_This checklist is idempotent: rerun after each merge to confirm gates remain green. Update issue references when tasks close._

> 📋 **Wave source of truth:** See [`PACKAGE_SEQUENCE.yaml`](PACKAGE_SEQUENCE.yaml) for the authoritative ordering,
> gates, and dependencies powering this checklist.

## Increment Tracking (Wave 1)

| Increment | Package | Status | Owner / Notes |
| --- | --- | --- | --- |
| A-1 | Ontologie & Graph | ☑ done | Degree/Louvain/shortest-path endpoints hardened; pytest + smoke cover metrics. |
| A-2 | Ontologie & Graph | ☑ done | Subgraph export delivers JSON/Markdown + counters; CLI/docs wired to dossier hook. |
| A-3 | Ontologie & Graph | ☑ done | Superset & Grafana assets committed; README & smoke scripts reference them. |
| F-1 | Dossier & Collaboration | ☑ done | Markdown/PDF export service, templates & tests shipped. |
| F-2 | Dossier & Collaboration | ☑ done | Feature-flagged notes, audit log + metrics operational and documented. |
| F-3 | Dossier & Collaboration | ☑ done | README demo + Superset dataset + smoke suites refreshed. |

> ✅ Update status column (`☐` → `☑`) as increments close; reruns keep table idempotent.

## Package A – Ontologie & Graph (MVP)

### Increment A-1 – Analytics Endpoint Hardening
- [x] `/graphs/analysis/degree` endpoint paginates + enforces timeout guardrails (pytest coverage `services/graph-api/tests/test_analysis_routes.py`). 【F:services/graph-api/app/routes/analytics.py†L28-L84】【F:services/graph-api/tests/test_analysis_routes.py†L12-L65】
- [x] `/graphs/analysis/communities` exposes Louvain output mit `community_id` column and Prometheus counters `graph_analysis_queries_total{algorithm="louvain"}` (validated via `services/graph-api/tests/test_analysis_routes.py`). 【F:services/graph-api/app/routes/analytics.py†L86-L138】【F:services/graph-api/metrics.py†L12-L26】
- [x] `/graphs/analysis/shortest-path` returns deterministic fixture path ≤ konfiguriertem Hop-Limit und berichtet Dauer-Histogramm (`graph_analysis_duration_seconds_bucket`). 【F:services/graph-api/app/routes/analytics.py†L140-L216】【F:services/graph-api/tests/test_analysis_routes.py†L66-L106】【F:services/graph-api/metrics.py†L12-L26】

### Increment A-2 – Subgraph Export Hook
- [x] Subgraph export endpoint (`/graphs/analysis/subgraph-export`) streams JSON + Markdown payload, increments `graph_subgraph_exports_total`. 【F:services/graph-api/app/routes/analytics.py†L218-L308】【F:services/graph-api/metrics.py†L28-L40】
- [x] CLI/Docs snippet (`cli it graph export --case-id ...`) published for dossier pipeline integration. 【F:docs/api/graph-analysis.md†L1-L60】【F:README.md†L63-L94】

### Increment A-3 – Observability & Dashboards
- [x] Superset dashboard `graph_analytics_mvp` deployed via `apps/superset/assets/scripts/import.sh` und in README-Demo verlinkt. 【F:apps/superset/assets/dashboard/graph_analytics_mvp.json†L1-L34】【F:README.md†L63-L94】
- [x] Grafana dashboard `graph-analytics-mvp.json` imported to observability stack. 【F:grafana/dashboards/graph-analytics-mvp.json†L1-L44】
- [x] Smoke E2E (`scripts/smoke_graph_analysis.sh`, `scripts/smoke_graph_views.sh`) validieren Query → Subgraph → Dossier-Export. 【F:scripts/smoke_graph_analysis.sh†L1-L76】

## Package F – Dossier & Collaboration (MVP)

### Increment F-1 – Dossier Export Service
- [x] `/dossier/export` generiert Markdown- und PDF-Artefakte mit Templates aus `examples/dossier/` (Smoke-Test `services/collab-hub/tests/test_dossier.py`). 【F:services/collab-hub/app/main.py†L204-L312】【F:services/collab-hub/templates/dossier/brief.md.j2†L1-L20】【F:services/collab-hub/tests/test_dossier.py†L1-L48】【F:examples/dossier/README.md†L1-L8】
- [x] CLI command + sample exports dokumentiert; README referenziert Templates & Flags. 【F:README.md†L63-L94】【F:examples/dossier/README.md†L1-L8】

### Increment F-2 – Notes & Metrics MVP
- [x] Feature-flagged notes endpoint persistiert fallbasierte Notizen mit Audit-Einträgen in `CH_AUDIT_PATH`-Logdateien. 【F:services/collab-hub/app/main.py†L40-L118】【F:services/collab-hub/app/main.py†L362-L388】
- [x] Metrics exposed: `dossier_exports_total`, `dossier_export_duration_seconds_bucket`, `collab_notes_total` (siehe `services/collab-hub/app/main.py`). 【F:services/collab-hub/app/main.py†L24-L49】【F:services/collab-hub/app/main.py†L204-L312】
- [x] Grafana stat panel reflects dossier export counters on the `graph-analytics-mvp` dashboard. 【F:grafana/dashboards/graph-analytics-mvp.json†L1-L44】

### Increment F-3 – Docs & Demo
- [x] Superset dataset `graph_analytics_mvp` provides dossier-ready analytics context (centrality histogram + community count). 【F:apps/superset/assets/datasets/graph_analytics_mvp.yaml†L1-L32】
- [x] README demo script documents Search → Graph → Dossier export walkthrough. 【F:README.md†L63-L94】
- [ ] Architecture/Observability review notes captured in `reports/architecture/phase2-wave1.md` post-completion.

## Gates Verification

- [ ] `scripts/generate_inventory.py` run post-merge (Inventory/Policy gate).
- [ ] `/metrics`, `/healthz`, `/readyz` endpoints verified via `scripts/check_gates.sh` (Health gate).
- [ ] Docs regenerated where inventories changed (API/Docs gate).
- [ ] Smoke E2E suite green in CI (`test_infoterminal_v030_features.sh`).
