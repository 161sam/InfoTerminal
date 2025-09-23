# InfoTerminal Service Catalog (Developer)

This catalog summarizes all InfoTerminal backend services with their role, tech stack, default ports, data dependencies, and operational references. Use it as the single stop when bootstrapping local stacks, aligning deployments, or wiring new automation around the platform.

## At-a-Glance Matrix

| Service | Domain | Stack | Host Port (dev) | Core Dependencies | Primary Docs |
| --- | --- | --- | --- | --- | --- |
| agent-connector | Agents & Plugins | Python · FastAPI | `PORT` (defaults 8617; align with gateway 8610) | Plugin manifests, `plugin-runner`, Flowise | `services/agent-connector/app_v1.py`, `docs/plugins/DEVELOPER.md` |
| archive (nlp backup) | Legacy / Archive | n/a | internal only | Filesystem | `services/archive/` |
| auth-service | Security | Python · FastAPI | `${IT_PORT_AUTH_SERVICE:-8616}` | Postgres (`AUTH_DATABASE_URL`) | `services/auth-service/README.md` |
| cache-manager | Platform Infra | Python · FastAPI | `PORT` (default 8082) | Redis, Postgres (optional) | `services/cache-manager/app_v1.py` |
| collab-hub | Collaboration | Python · FastAPI | `${IT_PORT_COLLAB:-8625}` | Postgres (tasks), Redis (presence) | `services/collab-hub/app_v1.py` |
| doc-entities | NLP & Extraction | Python · FastAPI | `${IT_PORT_DOC_ENTITIES:-8613}` | Postgres, optional Neo4j | `services/doc-entities/README.md` |
| egress-gateway | Network | Python · FastAPI | `${IT_PORT_EGRESS_GATEWAY:-8615}` | Tor/SOCKS, internal policy | `services/egress-gateway/app.py` |
| entity-resolution | Graph Intelligence | Python · FastAPI | internal only | Neo4j, doc-entities | `services/entity-resolution/` |
| federation-proxy | Federation | Python · FastAPI | `${IT_PORT_FEDERATION:-8628}` | Remote InfoTerminal peers | `services/federation-proxy/app_v1.py` |
| feedback-aggregator | Feedback | Python · FastAPI | `PORT` (default 8085) | Postgres (feedback), Redis (queues) | `services/feedback-aggregator/app_v1.py` |
| flowise-connector | Agents & Plugins | Python · FastAPI | `3417 → 8080` | Flowise (`FLOWISE_URL`), Gateway | `services/flowise-connector/app_v1.py` |
| forensics | Evidence Chain | Python · FastAPI | `${IT_PORT_FORENSICS:-8627}` | Object storage (`/data`), Postgres | `services/forensics/app_v1.py` |
| gateway | Access | Node.js · Fastify | `8610` (configurable via compose) | Upstream APIs, OPA, OIDC | `services/gateway/app/app.py`, `docker-compose.gateway.yml` |
| graph-api | Graph Data | Python · FastAPI | `${IT_PORT_GRAPH_API:-8612}` | Neo4j | `services/graph-api/app/main_v1.py` |
| graph-views | Graph Views | Python · FastAPI | container `:8000` (no host by default) | Postgres, Neo4j | `services/graph-views/README.md` |
| media-forensics | Media Analysis | Python · FastAPI | `${IT_PORT_MEDIA_FORENSICS:-8618}` | External reverse image search | `services/media-forensics/app_v1.py` |
| openbb-connector | Market Data | Python | batch job | OpenBB API, Postgres | `services/openbb-connector/main.py` |
| opa-audit-sink | Policy Audit | Python · FastAPI | internal only | OPA, object storage | `services/opa-audit-sink/app_v1.py` |
| ops-controller | Operations | Python · FastAPI | `${IT_PORT_OPS_CONTROLLER:-8614}` | Docker socket, `infra/ops/stacks.yaml` | `services/ops-controller/app_v1.py` |
| performance-monitor | Observability | Python · FastAPI | `PORT` (default 8086) | Prometheus, Loki | `services/performance-monitor/app_v1.py` |
| plugin-runner | Agents & Plugins | Python · FastAPI | `${IT_PORT_PLUGIN_RUNNER:-8621}` | Docker daemon, `/tmp` workspace | `services/plugin-runner/app.py` |
| policy | Policy | OPA Rego | n/a | OPA | `services/policy/` |
| rag-api | Retrieval (Legal) | Python · FastAPI | `${IT_PORT_RAG_API:-8622}` | OpenSearch, Neo4j | `services/rag-api/README.md` |
| search-api | Search | Python · FastAPI | `${IT_PORT_SEARCH_API:-8611}` | OpenSearch, optional embeddings | `services/search-api/README.md` |
| verification | Fact-Checking | Python · FastAPI | `${IT_PORT_VERIFICATION:-8617}` | Search, Graph, NLP | `services/verification/app_v1.py` |
| websocket-manager | Realtime | Python · FastAPI | `PORT` (default 8087) | Redis, plugin-runner | `services/websocket-manager/app_v1.py` |
| xai | Explainability | Python · FastAPI | `${IT_PORT_XAI:-8626}` | Model store | `services/xai/app_v1.py` |

## Core Data & Intelligence Services

### search-api
- **Role:** Full-text and hybrid (BM25 + embeddings) search across the OpenSearch cluster. Handles indexing, document lifecycle, and reranking.
- **Interfaces:** `/v1/search`, `/v1/index/documents`, `/v1/documents/{id}` (see `docs/API_INVENTORY_ENHANCED.md`).
- **Data dependencies:** OpenSearch (`OPENSEARCH_URL`), optional rerank model served locally.
- **Running locally:** `cd services/search-api && uvicorn search_api.app.main:app --port 8001` or `docker compose up search-api`.
- **Testing:** `pytest services/search-api -q` (coverage thresholds documented in `services/search-api/README.md`).
- **Observability:** Emits OTLP when `IT_OTEL=1`; Prometheus metrics like `search_requests_total` (`docs/dev/observability.md`).

### graph-api
- **Role:** Core graph storage API wrapping Neo4j; exposes traversal, analytics (degree, betweenness, Louvain), and mutation endpoints under `/v1`.
- **Data dependencies:** Neo4j (`NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASS`). Optional GDS toggles via `IT_NEO4J_GDS`.
- **Running locally:** `docker compose up graph-api` or `services/graph-api/dev_run.sh` (auto loads `.env.local`).
- **Testing:** `pytest services/graph-api/tests -q` with driver mocking; health tests cover dependency checks.
- **Docs:** `services/graph-api/app/main_v1.py`, `docs/API_INVENTORY_ENHANCED.md`, `docs/dev/graph-linking.md`.

### graph-views
- **Role:** Materializes graph egocentric views, exports dossiers, and performs CSV ingestion for demo data. Integrates with Postgres and Neo4j.
- **Ports:** Internal `:8000` only; enable host bind with override if needed (`docs/runbooks/stack.md` explains).
- **Usage:** See `services/graph-views/README.md` for CSV loader, dossier export, rate limiting, and audit logging.
- **Smoke:** `make smoke.gv` sets up environment variables (`GV_ALLOW_WRITES`, `GV_RATE_LIMIT_WRITE`, etc.).

### doc-entities
- **Role:** Named entity extraction, storage, and (future) resolution triggers for ingested documents.
- **API:** `/annotate`, `/docs/{id}`, `/resolve/*` placeholders (501 until resolver lands).
- **Dependencies:** Postgres migrations under `services/doc-entities/migrations`. `.env.example` documents env flags.
- **Testing:** `pytest services/doc-entities/tests -q` (fixtures stub NLP outputs).
- **Docs:** `services/doc-entities/README.md`, `docs/dev/en/plugins/REGISTRY_APIS.md` (integration context).

### rag-api
- **Role:** Legal/compliance retrieval; bridges OpenSearch (statutes) and Neo4j (law entity graph) to power `/law/retrieve` and `/law/context`.
- **Bootstrap:** Index auto-creates on first write; use provided `curl` samples in `services/rag-api/README.md`.
- **Ports:** `${IT_PORT_RAG_API:-8622}` to container `:8000`.
- **Observability:** Standard `/healthz` `/readyz`; enable OTEL with `IT_OTEL=1`.

### verification
- **Role:** Claim ingestion, evidence retrieval, stance classification, and report generation for fact-checking workflows.
- **Routers:** `routers/verifications_v1.py` merges search, graph, and doc-entities results; integrates with media-forensics for attachments.
- **Dependencies:** Search API, graph API, doc-entities, media-forensics; configure via env (`VERIFICATION_*`).
- **Testing:** `pytest services/verification -k v1`.
- **Docs:** `docs/blueprints/VERIFICATION-BLUEPRINT.md`, `docs/dev/VERIFICATION-BLUEPRINT.md`.

### entity-resolution (WIP)
- **Status:** Migration in progress (`services/entity-resolution/DEPRECATED.md`). Legacy scripts provide context for connecting doc-entities with Neo4j.
- **Action:** Track progress in `docs/PHASE2_MIGRATION_STATUS.md` and `docs/SERVICE_MIGRATION_GUIDE.md`.

## Agents, Plugins & Automation

### agent-connector
- **Role:** Central broker for agent plugins: discovery (`/v1/plugins/tools`), configuration, and invocation.
- **Upstream dependencies:** `plugin-runner` (executes tools), Flowise pipelines, plugin manifests under `services/agent-connector/plugins`.
- **Port alignment:** Current default `PORT=8617` in `app_v1.py`; gateway docs expect 8610. Adjust via env or patch script until reconciled.
- **Docs:** `docs/plugins/DEVELOPER.md`, `apps/frontend/AGENT_SERVICES_README.md`.
- **Testing:** `pytest services/agent-connector/tests -q`.

### plugin-runner
- **Role:** Sandboxes plugin processes (Docker or subprocess) and streams audit logs.
- **Dependencies:** Docker socket mount, plugin registry definitions (`services/plugin-runner/registry.py`).
- **Operational notes:** Manage temp dirs under `/tmp/plugin-runner`; supports `RequestIdMiddleware` for traceability.
- **Docs:** `docs/plugins/DEVELOPER.md`, `docs/dev/en/architecture/adr/ADR-0004-single-invocation-path.md`.

### flowise-connector
- **Role:** Gateway between InfoTerminal agent flows and Flowise instances. Handles chat proxies and tool orchestration.
- **Ports:** Host `3417` 3 -> container `8080` (non-standard per port policy; patch via `scripts/patch_ports.sh`).
- **Env flags:** `FLOWISE_URL`, `FLOWISE_TIMEOUT_S`, OTEL exporters.
- **Docs:** `services/flowise-connector/app_v1.py`, `docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md`.

### websocket-manager
- **Role:** Real-time update hub for investigations, plugin progress, and alerts; uses Redis pub/sub for scaling.
- **Integration:** Frontend subscribes via `apps/frontend/src/lib/ws-client.ts`. Configurable channels & auth tokens.

### ops-controller
- **Role:** Automation orchestrator for docker-compose stacks and remediation tasks. Exposes `/ops/stacks`, `/ops/logs` etc.
- **Dependencies:** Docker socket (mounted read-write) and `infra/ops/stacks.yaml` definitions.
- **Security:** See `services/ops-controller/security/` for policy stubs.
- **Docs:** `docs/runbooks/stack.md`, `docs/dev/observability.md`.

### n8n / NiFi integrations
- **Containers:** Configured via `docker-compose.nifi.yml`, `docs/nifi/` and `docs/n8n/`; interplay described in `docs/user/8.Integrationen&Erweiterbarkeit.md`.

## Access, Security & Networking

### gateway
- **Role:** Single entry point for frontend and external clients. Handles OIDC (when enabled), OPA checks, rate limiting, and metrics.
- **Upstreams:** Configurable via `USE_LOCAL_UPSTREAMS`, `SEARCH_TARGET`, `GRAPH_TARGET`, etc. (`docker-compose.gateway.yml`).
- **Security:** Integrates `_shared.audit` and optionally `OPA_URL` for allow/deny decisions.
- **Observability:** Prometheus counters/histograms (`gateway_requests_total`, `gateway_request_duration_seconds`).
- **Docs:** `docs/API_INVENTORY_ENHANCED.md:gateway`, `docs/adr/0004-policy-gateway-opa-forwardauth.md`.

### auth-service
- **Role:** JWT issuing, OAuth2/OIDC bridging, MFA, RBAC. Hosts admin APIs for user management.
- **Dependencies:** Postgres, OTP secrets storage (env / Redis optional).
- **Testing:** `pytest services/auth-service/tests -q`; formatting via `ruff` and `black` (see README).
- **Docs:** `services/auth-service/README.md`, `docs/AUTH_IMPLEMENTATION_COMPLETE.md`.

### egress-gateway
- **Role:** Outbound proxy for sensitive research traffic (Tor, rotating identities). Offers `/proxy/request`, `/proxy/status`.
- **Dependencies:** Local Tor or custom proxies defined in `services/egress-gateway/config`.
- **Docs:** `docs/API_INVENTORY_ENHANCED.md:egress-gateway`, `docs/runbooks/stack.md`.

### policy / opa-audit-sink
- **Role:** Policy-as-code via Rego (`services/policy/*.rego`) and audit sink capturing OPA decisions.
- **Deployment:** Compose profile `agents` contains `opa-audit-sink` (internal only).
- **Docs:** `docs/adr/0001-choose-opa-for-abac.md`, `docs/adr/0004-policy-gateway-opa-forwardauth.md`.

## Analytics, Forensics & Explainability

### forensics & media-forensics
- **Roles:** Chain-of-custody logging (`forensics`) and media analysis (EXIF, reverse image search) via `media-forensics`.
- **Storage:** Binds `./data/forensics` or `./data/media` for artifact retention.
- **Config:** `MEDIA_MAX_FILE_SIZE`, `REVERSE_SEARCH_ENABLED`, API keys (`BING_SEARCH_API_KEY`).
- **Docs:** `services/forensics/app_v1.py`, `services/media-forensics/app_v1.py`, `docs/dev/VERIFICATION-BLUEPRINT.md`.

### xai
- **Role:** Explainable AI endpoints for models integrated into verification/workflows.
- **Observability:** Ships with Prometheus middleware; set `IT_OTEL=1` to emit spans.

### performance-monitor & cache-manager
- **Roles:** Performance telemetry aggregator and smart caching layer for outbound calls/responses.
- **Status:** Both follow `_shared.api_standards` patterns; align persistence backends before enabling in prod.

### feedback-aggregator
- **Role:** Collects in-app and platform feedback, normalizes via `FeedbackService`, ships metrics.
- **Docs:** `services/feedback-aggregator/app_v1.py`, `docs/user/5.Erweiterte-Funktionen.md`.

### collab-hub
- **Role:** Team workspace; handles tasks, boards, comments, and notifications.
- **Status:** Core scaffolding ready; connect to frontend modules under `apps/frontend/src/components/collab`.

## Connectors & Pipelines

### openbb-connector
- **Role:** Batch importer for market data into Postgres staging tables.
- **Usage:** `python services/openbb-connector/main.py` with env overrides (`OPENBB_SYMBOLS`, `PG_*`).
- **Docs:** `services/openbb-connector/main.py`.

### cache-manager, websocket-manager, performance-monitor
- Provide platform-level infrastructure to improve responsiveness and realtime updates. Follow same startup/testing patterns as other standardised services.

## Related Documentation & Runbooks

- **API index:** `docs/API_INVENTORY_ENHANCED.md`
- **CLI utilities:** `docs/CLI_INVENTORY_ENHANCED.md`
- **Runbooks:** `docs/runbooks/stack.md`, `docs/dev/runbooks/` for service-specific recovery steps.
- **Ports:** `docs/PORTS_POLICY.md`, `scripts/patch_ports.sh`
- **Service migration status:** `docs/PHASE2_MIGRATION_STATUS.md`

Maintain this catalog alongside service changes: update tables after adjusting ports, dependencies, or critical docs so that developers and automation agents can rely on it as the definitive map of InfoTerminal services.
