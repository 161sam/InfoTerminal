# OPA Policies

This directory contains example policies used in development:

- `forwardauth.rego` – gateway authorization example.
- `rbac.rego` – simple role-based access control.
- `abac.rego` – attribute-based access control stub.
- `agents/tool_policy.rego` – Flowise connector policy deciding tool access.

Tests live under `policy/tests` and can be executed via:

```bash
opa test -v policy
```
