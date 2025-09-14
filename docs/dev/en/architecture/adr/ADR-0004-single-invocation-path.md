# ADR-0004: Single Invocation Path for Tools

- **Decision**: All user-facing tool invocations MUST go through `agent-connector /plugins` (`/plugins/tools`, `/plugins/invoke/{plugin}/{tool}`).
- **Rationale**: Avoid duplicate code paths, centralize auth/tenant/audit, enable plugin registry & policy.
- **Scope**: Frontend, other services (no direct calls to flowise/openbb/etc).
- **Migration**: old routes receive 308 until IT_DEPRECATION_CUTOFF_DATE, then 410.
- **Guards**: ESLint custom rule + CI grep.
