# Phase 2 – Wave 2 DoD Checklist

_Idempotent overview for Wave 2 (Packages B & C). Update checkmarks as increments land; reruns keep table consistent._

> 📋 **Wave source of truth:** [`PACKAGE_SEQUENCE.yaml`](PACKAGE_SEQUENCE.yaml) drives the active packages and gates.

## Increment Tracking (Wave 2)

| Increment | Package | Status | Owner / Notes |
| --- | --- | --- | --- |
| B-1 | NLP & Resolver | ☑ done | Alias-aware linking, resolver metrics + `/metrics` instrumentation shipped. |
| B-2 | NLP & Resolver | ☑ done | Gold sample regression tests cover alias linking + annotate metadata. |
| B-3 | NLP & Resolver | ☑ done | Frontend badges for resolved/unmatched entities with metadata surfacing. |
| C-1 | Geospatial Layer | ☑ done | BBox/nearby endpoints instrumented with Prometheus counters + tests. |
| C-2 | Geospatial Layer | ☑ done | Map panel consumes bbox API and README demo covers geo overlay. |

## Package B – NLP & Resolver (Wave 2 MVP)

### Increment B-1 – Resolver Metrics & Alias Linking
- [x] `resolver.py` normalises aliases, merges heuristic/fuzzy candidates, exposes resolution metadata per entity. 【F:services/doc-entities/resolver.py†L1-L220】
- [x] Prometheus collectors (`doc_entities_resolver_runs_total`, `doc_entities_resolver_outcomes_total`, `doc_entities_resolver_latency_seconds`, confidence histogram) registered idempotently. 【F:services/doc-entities/metrics.py†L1-L52】
- [x] `/v1/documents/{id}` returns resolution status/target/score plus metadata counts. 【F:services/doc-entities/routers/doc_entities_v1.py†L240-L390】

### Increment B-2 – Gold Sample Validation
- [x] `test_resolver_gold.py` seeds in-memory DB, verifies alias resolution + metadata exposure. 【F:services/doc-entities/tests/test_resolver_gold.py†L1-L80】
- [x] Annotate endpoint test asserts pending badges + metadata counts. 【F:services/doc-entities/tests/test_resolver_gold.py†L82-L115】

### Increment B-3 – Frontend Linking Surface
- [x] Entity badges show resolved/ambiguous/pending status with confidence chip; Document detail renders resolver stats. 【F:apps/frontend/src/components/entities/EntityBadge.tsx†L1-L120】【F:apps/frontend/src/components/docs/DocumentDetail.tsx†L1-L320】
- [x] README demo extended with resolver + metrics walkthrough. 【F:README.md†L48-L96】

## Package C – Geospatial Layer (Wave 2 MVP)

### Increment C-1 – API & Metrics
- [x] Graph API `/geo` routes increment `graph_geo_queries_total` & `graph_geo_query_errors_total`; external geocoding gated behind `GRAPH_ENABLE_GEOCODING`. 【F:services/graph-api/app/routes/geospatial.py†L1-L220】【F:services/graph-api/geospatial.py†L1-L120】
- [x] Geospatial unit test stubs Neo4j driver, asserts bbox query + metrics. 【F:services/graph-api/tests/test_geospatial.py†L1-L80】

### Increment C-2 – Map Integration & Observability
- [x] Frontend document detail consumes `/v1/documents/{id}` output; map panel already binds bbox API; demo script documents geo query. 【F:apps/frontend/src/components/docs/DocumentDetail.tsx†L1-L320】【F:README.md†L63-L96】
- [x] Grafana dashboard includes Wave 2 row with resolver outcomes + geo query volume panels. 【F:monitoring/grafana-dashboards/infoterminal-overview.json†L1-L400】

## Gates Verification

- [ ] Inventory regenerated (`scripts/generate_inventory.py`) after Wave 2 merges.
- [ ] `/metrics` + `/healthz` + `/readyz` smoke checked post-deploy.
- [ ] Docs & README updated alongside feature PRs (API/Docs gate).
- [ ] Smoke suites (graph + doc-entities) green in CI.
