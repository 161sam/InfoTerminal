# API Versioning & Compatibility

InfoTerminal APIs follow **Semantic Versioning**. The `v1` namespace of the Search API is frozen at version `1.0.0`; all changes are validated against the committed OpenAPI artefact at `artifacts/api/openapi-v1.0.json`.

## Versioning Policy

- **MAJOR (1.x → 2.0)** – Breaking changes that remove endpoints, change request/response schemas, or relax required authentication. Requires a new `/v{N}` namespace and migration guide.
- **MINOR (1.0 → 1.1)** – Backwards-compatible feature work. You may add optional fields, new endpoints, or new response codes that do not break existing consumers.
- **PATCH (1.0.0 → 1.0.1)** – Backwards-compatible fixes such as documentation updates, bug fixes, or performance improvements that do not alter request/response contracts.

Changes to shared schemas, parameters, or responses that invalidate existing clients are considered **breaking** and must ship behind a new major version.

## Compatibility Gate

CI runs `scripts/check_api_compat.py` via the `api_compat` job. The gate regenerates the Search API specification and compares it with the frozen artefact. The job fails when:

- An existing path, method, parameter, or response is removed or modified.
- A schema under `components/schemas` changes in an incompatible way.

If you intentionally introduce a breaking change, bump the major version, generate a new artefact (e.g. `openapi-v2.0.json`), and document the migration path.
