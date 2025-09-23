# InfoTerminal Plugin Developer Guide

## 1. Architecture Overview
- **Contract**: Plugins are described by versioned manifests (`docs/dev/en/architecture/adr/ADR-0001-plugin-system-v1.md:1`) and validated via the shared TypeScript/Pydantic models (`packages/plugin-sdk/src/types.ts:13`, `services/common/plugin_sdk/__init__.py:15`).
- **Discovery & Routing**: Manifests under `plugins/<name>/plugin.yaml` are cached by the Agent Connector loader (`services/agent-connector/plugins/loader.py:31`). Frontend calls `/api/plugins/...`, Next.js rewrites to the Gateway, which proxies to the Agent Connector (`apps/frontend/next.config.js:23`, `services/gateway/app/app.py:89`).
- **Execution Paths**:
  - *Remote integrations* proxy tool invocations to the provider's `/tools/{tool}` API (`services/agent-connector/plugins/loader.py:87`).
  - *Sandboxed tools* execute inside the Plugin Runner service with Docker isolation, parsing, and result enrichment (`services/plugin-runner/app.py:117`, `services/plugin-runner/registry.py:151`).
- **State & RBAC**: Enablement/config state is persisted per user and globally under `IT_PLUGINS_STATE_DIR` with admin gating for global scope (`services/agent-connector/plugins/state.py:1`, `services/agent-connector/plugins/api.py:53`).

```
Frontend → Gateway → Agent Connector
            │             └── Loader (manifests, invoke)
            └──► OPA
Loader ─► Remote API or Plugin Runner (Docker) ─► Results → Search/Graph
```

## 2. Manifest Specification (`apiVersion: v1`)
| Field | Required | Description |
|-------|----------|-------------|
| `name`, `version` | yes | Unique identifier & semantic version. |
| `provider`, `description` | optional | Display metadata surfaced in UI (`apps/frontend/pages/plugins/index.tsx:131`). |
| `capabilities.tools[]` | yes | Each tool exposes `name`, `description`, `argsSchema` (JSON Schema), optional `resultSchema`, `timeoutMs`, `auth`, `permissions` (`packages/plugin-sdk/src/types.ts:3`). |
| `endpoints.baseUrl` | required for remote plugins | HTTP base for `/tools/{tool}` and optional `health` route (`plugins/openbb/plugin.yaml:13`). |
| `security`, `command_templates`, etc. | required for sandboxed CLI plugins | Define Docker policy, parameter validation, parsers, and integration targets (`plugins/nmap/plugin.yaml:41`). |

**Validation**
1. Loader enforces `apiVersion == IT_PLUGIN_API_VERSION` (`services/agent-connector/plugins/loader.py:38`).
2. Optional request schema validation uses `jsonschema` if available (`services/agent-connector/plugins/loader.py:82`).
3. Plugin Runner rejects configs that exceed timeout/memory policies or violate sandbox requirements (`services/plugin-runner/registry.py:106`).

## 3. Implementation Patterns
### 3.1 Remote Service Plugin
1. Create `plugins/<plugin>/plugin.yaml` with `apiVersion: v1`, `capabilities.tools`, and `endpoints.baseUrl` referencing env vars where possible (`plugins/flowise/plugin.yaml:13`).
2. Expose provider endpoints: implement `/tools/<tool>` handlers and a health check (default `healthz`).
3. If the plugin requires user auth, choose `auth: "inherit"` so gateway-injected headers propagate downstream.
4. For local development, update `.env` to inject `NEXT_PROXY_PLUGINS` or provider base URL; no fixed ports outside policy (`docs/PORTS_POLICY.md`).

### 3.2 Sandboxed CLI Plugin
1. Provide Docker image reference (`docker_image`) and command templates (`plugins/nmap/plugin.yaml:44`).
2. Describe parameters with type, validation, defaults, and choices for automated UI forms (`plugins/nmap/plugin.yaml:10`).
3. Specify `security` guardrails (sandbox type, time/memory limits). The registry enforces high-risk plugins to use Docker and sane resources (`services/plugin-runner/registry.py:110`).
4. Configure `output_parsing` to convert raw output into structured entities, plus optional `integration.graph_entities`/`search_indexing` mappings.
5. Ensure the Docker image runs non-interactively and writes outputs to `/tmp` or stdout only. Runner mounts no writable host paths.

## 4. Lifecycle & Operations
- **Enablement Flow**: Users toggle plugins in the UI; global scope requires admin (`services/agent-connector/plugins/api.py:55`). Loader merges user/global state when responding (`services/agent-connector/plugins/api.py:33`).
- **Health Monitoring**: Health calls reuse manifest endpoint, capturing latency for telemetry (`services/agent-connector/plugins/api.py:95`). Plugin Runner exposes `/healthz` and `/readyz` for container orchestration (`services/plugin-runner/app.py:195`).
- **Observability**: Gateway logs every sensitive `/plugins/invoke` decision with OPA verdict (`services/gateway/app/app.py:91`). Plugin Runner records job metrics, durations, and persists JSON results under `RESULTS_DIR` (`services/plugin-runner/app.py:174`).
- **Audit & Compliance**: All invocations log to the shared audit stream (`services/agent-connector/plugins/loader.py:102`). Secrets must stay in env/vault; API rejects secret-looking config keys (`services/agent-connector/plugins/api.py:80`).

## 5. Development Workflow
1. **Plan & ADR alignment** – confirm features align with ADR-0001 and roadmap entries (`ROADMAP.md`).
2. **Author manifest** – follow the patterns above, validate via `jsonschema`/`ajv` locally using your manifest schema.
3. **Implement provider service** – ensure readiness, `/healthz`, tracing, and request-ID propagation (`services/plugin-runner/app.py:58`).
4. **Write tests** – mirror `services/agent-connector/tests/test_plugins_api.py:47` for registry/state behaviour. For runner-based plugins, add async execution tests via `pytest.mark.asyncio`.
5. **Update docs** – extend `docs/plugin/USER.md` and service READMEs with usage examples.
6. **Verify end-to-end** – use `curl` or `invokeTool()` from `apps/frontend/lib/plugins.ts:1` against the Dev stack. Capture audit logs via `docker logs gateway`.

## 6. Checklists
### Remote Plugin Submission
- [ ] Manifest validated (`apiVersion: v1`, schema complete).
- [ ] Health endpoint returns 200/JSON.
- [ ] Tool endpoint enforces auth/tenant headers if required.
- [ ] User + global configuration documented.
- [ ] Tests cover registry discovery & invocation errors.

### Sandboxed Plugin Submission
- [ ] Docker image hosted/declared.
- [ ] Command templates parameterised; defaults safe.
- [ ] Security section passes registry validation.
- [ ] Parser extracts structured data; errors handled.
- [ ] Graph/Search integration mappings reviewed with data team.

## 7. Reference Commands
```bash
# Run agent-connector plugin API tests
pytest services/agent-connector/tests/test_plugins_api.py -q

# Trigger Plugin Runner readiness check
curl http://localhost:8621/readyz
```

## 8. Troubleshooting
| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| 404 on `/api/plugins/invoke` | Manifest missing/invalid cache | Restart Agent Connector or touch manifest file. |
| HTTP 403 from Gateway | OPA policy denied sensitive path | Check OPA logs and update policy (`services/gateway/app/app.py:89`). |
| Plugin Runner timeout | Security `timeout` too low or command hanging | Adjust manifest security block; verify command locally. |
| UI shows `unknown` health | Manifest lacks `endpoints.health` or provider offline | Add explicit `health` path or restore provider service. |

## 9. Related Documents
- ADR: `docs/dev/en/architecture/adr/ADR-0001-plugin-system-v1.md:1`
- Migration plan: `docs/dev/en/migration/2025-plugins-invocation-path.md:1`
- Port policy: `docs/PORTS_POLICY.md`
- Legacy reference: `docs/LEGACY/dev/roadmap/v0.3-plus/master-todo.md`
