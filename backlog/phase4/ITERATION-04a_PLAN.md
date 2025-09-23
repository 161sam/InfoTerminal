# Iteration 04a – Wave 4 (H1) Plan

_Idempotent planning sheet for the AI-Agenten mini-iteration. Update the status
column instead of duplicating entries._

| Deliverable | Status | Notes |
| --- | --- | --- |
| Flowise connector MVP (`/tools`, `/chat`, `/chat/{id}/cancel`) with static allowlist and global rate limit | ✅ | `services/flowise-connector/app/main.py`, new tests under `tests/test_agents_mvp.py` |
| Prometheus metrics + Grafana tiles (`agent_tool_calls_total`, `agent_policy_denied_total`, `agent_rate_limit_block_total`) | ✅ | Counters in service, panels in `grafana/dashboards/infra-overview.json` |
| Lightweight frontend chat at `/agent/mvp` with progress badges + API proxy route | ✅ | `apps/frontend/pages/agent/mvp.tsx`, `pages/api/agent/mvp-chat.ts`, banner in `agent.tsx` |
| Docs & artefacts refreshed (quickstart, backlog entries, STATUS/ROADMAP/DOCS_DIFF) | ✅ | `docs/agents/quickstart.md`, `backlog/phase4/WAVE4_DOD_CHECKLIST.md`, status docs |

> Next: deliver Iteration 04b (RSS connector) once the checklist and status
updates below are green.
