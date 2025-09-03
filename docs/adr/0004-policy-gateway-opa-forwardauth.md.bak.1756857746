# ADR 0004: Policy Gateway via OPA ForwardAuth
Date: 2025-09-02
## Status
Accepted
## Context
APIs require centralized authorization with pluggable policies.
## Decision
Deploy an edge gateway using OPA as a forward auth service to evaluate Rego policies before routing.
## Consequences
Unifies authorization checks but adds latency and coupling to gateway availability.
## Alternatives
- Embed policy checks in each service
- Custom gateway plugin
## References
- https://traefik.io/
- https://www.openpolicyagent.org/docs/latest/edge/
