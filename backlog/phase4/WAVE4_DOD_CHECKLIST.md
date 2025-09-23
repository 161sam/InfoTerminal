# Phase 4 – Wave 4 DoD Checklist

_Idempotent checklist for Wave 4 mini-iterations. Update the status markers
instead of duplicating rows._

## Increment Tracking (Wave 4)

| Increment | Package | Status | Notes |
| --- | --- | --- | --- |
| H1 | AI-Agenten MVP | ☑ done | Flowise connector single-turn MVP with governance + UI. |
| I1 | Externe Feeds (RSS) | ☑ done | RSS connector MVP with metrics, docs, and tests delivered. |

## Package H – AI-Agenten (H1 MVP)

- [x] Feature flag `AGENTS_ENABLED` default `0`, enabling `/tools`, `/chat`,
  `/chat/{id}/cancel`. 【F:services/flowise-connector/app/main.py†L164-L244】
- [x] Tool registry exposes exactly three tools (`search`, `graph.query`,
  `dossier.build`) with parameter schema. 【F:services/flowise-connector/app/main.py†L47-L107】
- [x] `/chat` enforces static allowlist, max one mocked tool call, global
  rate-limit (5/min). 【F:services/flowise-connector/app/main.py†L209-L281】
- [x] Metrics counters (`agent_tool_calls_total`, `agent_policy_denied_total`,
  `agent_rate_limit_block_total`) plus Grafana tiles. 【F:services/flowise-connector/app/main.py†L118-L148】【F:grafana/dashboards/infra-overview.json†L7-L40】
- [x] Cancel hook stub logs cancellation requests. 【F:services/flowise-connector/app/main.py†L299-L306】
- [x] API tests cover tool list, allowlist deny, rate limit, metrics exposure.
  【F:services/flowise-connector/tests/test_agents_mvp.py†L1-L74】
- [x] Frontend MVP chat displays progress badges + error states. 【F:apps/frontend/pages/agent/mvp.tsx†L1-L265】
- [x] Quickstart + backlog artefacts refreshed. 【F:docs/agents/quickstart.md†L1-L120】【F:backlog/phase4/ITERATION-04a_PLAN.md†L1-L16】

## Package I – Externe Feeds (I1 MVP)

- [x] RSS connector normalises id/title/url/published_at. 【F:services/feed-ingestor/app/main.py†L180-L190】
- [x] De-duplication + dry-run job scaffolded. 【F:services/feed-ingestor/app/main.py†L206-L234】
- [x] Metrics + Grafana panels (`feed_items_*`). 【F:services/feed-ingestor/app/main.py†L118-L134】【F:grafana/dashboards/infra-overview.json†L7-L64】
- [x] Quickstart + backlog updated. 【F:docs/feeds/quickstart.md†L1-L120】【F:backlog/phase4/ITERATION-04b_PLAN.md†L1-L8】

## Gates Verification

- [x] API tests (`services/flowise-connector` pytest suite) green locally.
- [x] Metrics appear in `/metrics` endpoint and Grafana dashboard updated.
- [ ] Smoke E2E for feeds pending Iteration 04b.
