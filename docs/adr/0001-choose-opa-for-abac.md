# ADR 0001: Choose OPA for ABAC
Date: 2025-09-02
## Status
Accepted
## Context
Need flexible attribute-based access control for multi-tenant data and policy-as-code requirements.
## Decision
Adopt Open Policy Agent (OPA) with Rego policies. Use Conftest in CI and normalize inputs at the gateway.
## Consequences
Centralized policies and auditability but requires learning Rego and maintaining policy bundles.
## Alternatives
- Hardcoded roles in services
- Custom policy engine
## References
- https://www.openpolicyagent.org/
