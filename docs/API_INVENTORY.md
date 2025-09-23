# API Inventory (Phase 1 Baseline)

_Last updated: 2025-09-23 via `python scripts/generate_inventory.py`._

The full machine-readable inventory lives in `inventory/apis.json` and is regenerated from the FastAPI/Typer AST (see `scripts/generate_inventory.py`). This document summarises key insights for v1.0 planning and points to the authoritative data.

## Overview
- **Services analysed**: 26 FastAPI services. 【F:inventory/apis.json†L1-L20】
- **Endpoint coverage**: Ops-controller (52), auth-service (51), graph-api (40), rag-api (38), collab-hub (36) lead the catalogue. 【260183†L1-L24】
- **Core health**: Search, graph, doc-entities, verification expose `/healthz` + `/readyz`; metrics coverage tracked in `inventory/findings.md`. 【F:inventory/services.json†L205-L329】【F:inventory/findings.md†L1-L69】

## Regeneration
```bash
python scripts/generate_inventory.py       # rewrites inventory/*.json
python scripts/generate_inventory.py --dry-run  # preview changes
```

## Quick Reference Tables

### Core APIs
| Service | Endpoint Count | Highlights |
| --- | --- | --- |
| search-api | 24 | `/healthz`, `/readyz`, `/v1/search`, `/v1/index`, rerank endpoints. 【F:inventory/apis.json†L280-L360】【F:services/search-api/src/search_api/app/main_v1.py†L1-L120】 |
| graph-api | 40 | Analytics (`/v1/algorithms/*`), geospatial (`/v1/geo/*`), export hooks. 【F:inventory/apis.json†L70-L140】【F:services/graph-api/analytics.py†L1-L120】 |
| doc-entities | 28 | NER, summarisation, relation extraction, fuzzy matching. 【F:inventory/apis.json†L360-L420】【F:services/doc-entities/routers/doc_entities_v1.py†L1-L120】 |
| verification | 32 | Claim extraction, media analysis, stance classification; Prometheus metrics at `/metrics`. 【F:inventory/apis.json†L560-L620】【F:services/verification/app_v1.py†L1-L120】 |
| ops-controller | 52 | Service orchestration, health aggregation, feature toggles. 【F:inventory/apis.json†L20-L70】【F:services/ops-controller/app/main.py†L1-L120】 |

### Automation & Agents
| Service | Endpoint Count | Highlights |
| --- | --- | --- |
| agent-connector | 28 | Plugin registry, tool invocation, health checks. 【F:inventory/apis.json†L1-L40】 |
| flowise-connector | 18 | Agent orchestration, health, Flowise proxying. 【F:inventory/apis.json†L420-L460】【F:services/flowise-connector/routers/agents_v1.py†L1-L120】 |
| plugin-runner | 32 | Sandbox execution, registry CRUD, metrics. 【F:inventory/apis.json†L460-L520】【F:services/plugin-runner/app_v1.py†L1-L120】 |

### Collaboration & UX
| Service | Endpoint Count | Highlights |
| --- | --- | --- |
| collab-hub | 36 | Task CRUD, audit logging, websocket broadcasts. 【F:inventory/apis.json†L520-L560】【F:services/collab-hub/app/main.py†L1-L120】 |
| federation-proxy | 28 | External data federation, health, caching. 【F:inventory/apis.json†L620-L660】【F:services/federation-proxy/app_v1.py†L1-L120】 |
| cache-manager | 30 | Cache CRUD + warm/invalidate operations. 【F:inventory/apis.json†L660-L700】【F:services/cache-manager/main.py†L670-L740】 |

## Using the Inventory
- Filter endpoints for a service:
  ```bash
  jq '.services["graph-api"]' inventory/apis.json | less
  ```
- Compare CLI coverage vs API: regenerate CLI inventory via `scripts/generate_parity_reports.py` and diff with JSON.
- Map endpoints back to source files via the `source` + `lineno` metadata embedded in `inventory/apis.json`.

## Known Gaps (tracked in `DOCS_DIFF.md`)
- Enhanced markdown inventories under `docs/*_ENHANCED.md` still reflect pre-Phase 1 data; replace with inventory excerpts.
- API docs for new services (flowise-connector, plugin-runner, ops-controller) require narrative explanations and auth examples.

For detailed roadmap alignment see `ROADMAP_STATUS.md`.
