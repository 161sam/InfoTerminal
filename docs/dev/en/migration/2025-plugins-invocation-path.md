# Migration: Single Plugin Invocation Path (2025)

- Write manifests for flowise, openbb, n8n.
- Refactor frontend tool calls to use `/api/plugins`.
- Add ESLint rule and CI guard against direct provider hosts.
- Deprecate `nlp-service` routes via gateway redirect/410 policy.
- Rollback: restore removed routes and disable rule if needed.
