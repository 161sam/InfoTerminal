# Agent Connector

This service provides a lightweight API layer in front of Flowise.

## Routes
- `GET /tools` — lists available tools such as `search.query`, `graph.neighbors`, and `docs.ner`.
- `POST /playbooks/run` — executes a static playbook, e.g. `InvestigatePerson`.
- `POST /chat` — proxies chat messages to Flowise when `AGENT_BASE_URL` is set; otherwise returns a stub response.

Enable metrics with `IT_ENABLE_METRICS=1`. Health endpoints are available at `/healthz` and `/readyz`.
