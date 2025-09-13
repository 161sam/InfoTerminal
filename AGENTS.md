
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

