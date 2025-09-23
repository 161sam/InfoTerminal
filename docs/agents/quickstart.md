# Agent MVP Quickstart (Iteration 04a)

This guide explains how to run the Wave 4 mini-iteration (H1) agent MVP. The
focus is a mocked single-turn agent flow that enforces tool governance,
rate-limiting, and exposes new Prometheus counters.

## Prerequisites

- Python environment for the `services/flowise-connector` service.
- Frontend (`apps/frontend`) dependencies installed via `pnpm install`.
- Feature flag `AGENTS_ENABLED=1` exported in the environment for both the
  connector and frontend (the default remains disabled to keep the surface
  secure by default).

```bash
export AGENTS_ENABLED=1
```

## Start the connector (mocked tools)

Run the FastAPI app locally; the tests ship a deterministic tool registry with
six tools:

```bash
cd services/flowise-connector
uvicorn app.main:app --reload --port 8610
```

Available endpoints:

- `GET /tools` → returns the policy-governed tools (`search`, `graph.query`,
  `dossier.build`, `doc-entities.ner`, `plugin-runner.run`, `video.analyze`)
  including parameter schema.
- `POST /chat` → executes at most one mocked tool call and returns the summary
  plus tool steps.
- `POST /chat/{conversation_id}/cancel` → stub that logs cancel requests.
- Metrics: `/metrics` exposes `agent_tool_calls_total`,
  `agent_policy_denied_total`, `agent_rate_limit_block_total`,
  `agent_rate_limited_total`, and the latency histogram
  `agent_tool_latency_seconds` (labelled by tool and hashed user).

Example request:

```bash
curl -s http://localhost:8610/chat \
  -H 'Content-Type: application/json' \
  -d '{
        "message": "Draft a dossier for ACME Corp",
        "tool": "dossier.build",
        "tool_params": {"subject": "ACME Corp"}
      }' | jq
```

Expected response fragment:

```json
{
  "reply": "Executed dossier.build with max 1 step...",
  "tool_call": {
    "tool": "dossier.build",
    "result": {
      "summary": "Mocked dossier.build run for 'Draft a dossier for ACME Corp'"
    }
  },
  "steps": [
    {"status": "started", "tool": "dossier.build"},
    {"status": "completed", "tool": "dossier.build"}
  ]
}
```

## Frontend MVP chat

The lightweight MVP chat lives at `/agent/mvp` in the Next.js frontend. The
page renders a simple prompt form, tool selector, and progress badges showing
when the mocked tool call starts and completes.

```bash
cd apps/frontend
pnpm dev -- --port 3411
```

Then open http://localhost:3411/agent/mvp and send a prompt. Denied requests
(for example selecting a non-existent tool or a policy-blocked action) return a
red error badge and surface the reason from the backend.

## Offline demo script

1. Enable the flag and start the connector with `uvicorn` as shown above.
2. Use `curl http://localhost:8610/tools` to confirm the six-tool registry.
3. Trigger `dossier.build` using the sample `curl` snippet and observe the
   counters via `curl http://localhost:8610/metrics`.
4. Start the frontend (`pnpm dev`) and visit `/agent/mvp`; submit the same
   prompt to view the tool call progress badge and the mocked summary.
5. Hit the rate limit by sending six quick requests → the UI surfaces a clear
   error and the `agent_rate_limited_total{scope="global"}` counter increments
   alongside the legacy `agent_rate_limit_block_total` (visible in Grafana’s
   Infra Overview dashboard panels).

## Policy enforcement with OPA

The connector now loads `policy/agents/tool_policy.rego` (override via
`AGENT_POLICY_PATH`) together with `policy/agents/tool_data.json`. At runtime the
service calls the OPA decision endpoint configured via `AGENT_OPA_URL` (default
`http://localhost:8181/v1/data`) and `AGENT_OPA_DECISION` (default
`agents/tool/decision`). Every `/chat` request sends `{tool, route, context}` to
OPA; the decision result supplies both the verdict and the human-readable
message shown in the Assistant UI.

Sample rule from the bundled policy:

```rego
package agents.tool

decision = {
    "allow": true,
    "reason": entry.reason,
    "message": entry.message,
} {
    entry := data.agents.allowed_tools[_]
    entry.tool == input.tool
    route_matches(entry.route)
    not entry.effect
}
```

To deny a tool, add an entry with `"effect": "deny"` and customise the
`message` in `tool_data.json`. Environment flags:

- `AGENT_OPA_ENABLED` (default `1`) toggles enforcement.
- `AGENT_OPA_FAIL_OPEN` (default `1`) allows falling back to legacy behaviour if
  OPA is unreachable.
- `AGENT_OPA_TIMEOUT` configures the HTTP timeout in seconds.

## Where to observe metrics

- Prometheus scrape target: Flowise connector (`agent_tool_calls_total`,
  `agent_policy_denied_total`, `agent_rate_limit_block_total`,
  `agent_rate_limited_total`, `agent_tool_latency_seconds`).
- Grafana dashboard: `grafana/dashboards/infra-overview.json` now ships a tile
  for each counter.

## Tests

Execute the dedicated API and policy tests before shipping changes:

```bash
cd services/flowise-connector
pytest

# optional, validates Rego bundle
opa test ../../policy
```

The suite validates tool registry size, OPA enforcement, rate limits, and
metrics exposure. `opa test` ensures the Rego policy remains in sync with the
Python integration.
