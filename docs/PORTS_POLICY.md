# Dev Port & Profile Policy (Phase 1 Baseline)

_Last updated: 2025-09-23 via `scripts/generate_inventory.py`._

## Principles
- Prefer project-specific host ports (3000/3411/861x/864x ranges) to avoid collisions; document any temporary standard-port exposure.
- Expose databases/search engines to the host **only** for debug overlays; default profiles keep Postgres/OpenSearch internal.
- Each compose profile must document its host bindings; regenerate the canonical view with `python scripts/generate_inventory.py` (writes `inventory/services.json`).

## Host Port Matrix (excerpt)
| Service | Host → Container | Profiles | Notes |
| --- | --- | --- | --- |
| frontend | `${IT_PORT_FRONTEND:-3000}:3000` | default | Next.js dev server; disable in prod behind gateway. 【F:inventory/services.json†L207-L246】 |
| gateway | `8610:8080` | default | Express reverse proxy; injects `/metrics` at `:8610/metrics`. 【F:inventory/services.json†L207-L246】【F:services/gateway/index.ts†L1-L80】 |
| search-api | `${IT_PORT_SEARCH:-8001}:8001`, `${IT_PORT_SEARCH_API:-8611}:8080` | default | Legacy port retained for backward compatibility; prefer gateway access on 8610. 【F:inventory/services.json†L205-L226】 |
| graph-api | `${IT_PORT_GRAPH:-8612}:8612`, `${IT_PORT_GRAPH_API:-8612}:8080` | default | Consolidate to 8612 once gateway paths verified; inventory flags duplicate mapping. 【F:inventory/services.json†L227-L246】 |
| graph-views | `${GRAPH_VIEWS_PORT:-8403}:8403` | graph-views | Serves dossier/geo APIs; metrics gated by `IT_ENABLE_METRICS`. 【F:inventory/services.json†L227-L266】 |
| doc-entities | `${IT_PORT_DOC_ENTITIES:-8613}:8000` | default | NLP service; avoid exposing in prod. 【F:inventory/services.json†L161-L184】 |
| ops-controller | `${IT_PORT_OPS_CONTROLLER:-8614}:8000` *(twice)* | default | Duplicate mapping detected; rationalise to a single binding. 【F:inventory/services.json†L184-L205】 |
| egress-gateway | `${IT_PORT_EGRESS_GATEWAY:-8615}:8615` | default | Mandatory for egress policy validation; pair with OPA. 【F:inventory/services.json†L184-L205】 |
| auth-service | `${IT_PORT_AUTH_SERVICE:-8616}:8080` | default | OAuth2/OIDC backend; front with gateway or Keycloak. 【F:inventory/services.json†L184-L205】 |
| verification | `${IT_PORT_VERIFICATION:-8617}:8617` | default | Fact-checking API; ensure Prometheus scrape configured. 【F:inventory/services.json†L289-L329】 |
| media-forensics | `${IT_PORT_MEDIA_FORENSICS:-8618}:8000` | default | Video pipeline worker (Phase E). 【F:inventory/services.json†L289-L329】 |
| nifi | `${IT_PORT_NIFI:-8619}:8080`, `${IT_PORT_NIFI_CLUSTER:-11443}:11443` | nifi | Cluster port 11443 exposes HTTPS; restrict to localhost. 【F:inventory/services.json†L266-L289】 |
| plugin-runner | `${IT_PORT_PLUGIN_RUNNER:-8621}:8000` | default | Sandbox runner; enforce timeouts + OPA before prod exposure. 【F:inventory/services.json†L353-L392】 |
| flowise-connector | `3417:8080` | agents | Fixed host port for Flowise UI/connector (per ports policy). 【F:inventory/services.json†L330-L352】 |
| superset | `${IT_PORT_SUPERSET:-8644}:8088` | superset, sso | Airflow/superset overlays expose OAuth proxies at `:4180`. 【F:inventory/services.json†L1-L80】 |
| Prometheus / Grafana / Loki / Tempo | `3412:9090`, `3413:3000`, `3415:3100`, `3416:3200` | observability | Observability stack; secure with basic auth before remote access. 【F:inventory/services.json†L266-L289】 |
| postgres | `${IT_PORT_POSTGRES:-5432}:5432` | verification overlay | Only exposed when using verification compose; default keep internal. 【F:inventory/services.json†L266-L289】 |
| opensearch | `${IT_PORT_OPENSEARCH:-9200}:9200`, `${IT_PORT_OPENSEARCH_PERF:-9600}:9600` | default | Disable host exposure for prod; prefer gateway/CLI access. 【F:inventory/services.json†L266-L289】 |
| neo4j | `${IT_PORT_NEO4J:-7474}:7474`, `${IT_PORT_NEO4J_BOLT:-7687}:7687`, `8743/8744/8767` | default | Multiple host bindings detected; clean up duplicates (`auth-service-compose.yml`). 【F:inventory/services.json†L266-L289】 |

> **Tip**: For a complete list (including infra jobs), inspect `inventory/services.json` and filter by `ports`.

## Profile Guidance
- **default**: Core stack (gateway, search, graph, doc-entities, verification). Keep database ports internal.
- **agents**: Flowise connector + agent services; ensure OPA policies loaded before enabling host access. 【F:inventory/services.json†L330-L352】
- **nifi / n8n**: Enable only when running ingest demos; restrict host access to local network.
- **observability**: Prometheus/Grafana/Loki/Tempo; secure with auth and network policies before exposing beyond localhost.
- **sso / superset / airflow**: Use behind oauth2-proxy containers; confirm callback URLs in Keycloak configuration.

## Regeneration Workflow
1. Run `python scripts/generate_inventory.py` (optionally `--dry-run`) after compose changes.
2. Review `inventory/services.json` diffs; ensure new ports comply with policy ranges.
3. Update this document with notable changes and link to relevant compose/profile files.

## Outstanding Actions
- Deduplicate `ops-controller`, `neo4j`, and other services exposing multiple host ports. 【F:inventory/services.json†L184-L205】【F:inventory/services.json†L266-L289】
- Document temporary standard-port exposures (Postgres 5432, OpenSearch 9200) in compose readmes and restrict in prod overlays.
- Link generated findings (`inventory/findings.md`) into observability runbooks to enforce probe coverage. 【F:inventory/findings.md†L1-L69】
