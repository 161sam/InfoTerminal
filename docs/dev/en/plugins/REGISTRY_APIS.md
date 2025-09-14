# Plugin Registry APIs

The agent-connector exposes endpoints for discovering and configuring external plugins.

## Endpoints

- `GET /plugins/registry` – list plugin manifests discovered under `IT_PLUGINS_DIR`.
- `GET /plugins/state` – merge registry data with global and user specific state files.
- `POST /plugins/{name}/enable` – toggle a plugin on or off. Defaults to user scope; use `{ "scope": "global" }` and admin credentials for global settings.
- `GET /plugins/{name}/config` – read merged configuration.
- `POST /plugins/{name}/config` – persist non-secret configuration values. Keys containing `secret`, `token`, `password` or `apiKey` are rejected.
- `GET /plugins/{name}/health` – proxy a health check against the plugin's `endpoints.health` URL. Results are cached for `IT_PLUGINS_CACHE_TTL_SEC` seconds.

## RBAC

User scoped operations require authentication. Global scoped mutations require an admin role (`roles` claim contains `admin`).

## State Storage

State is stored as JSON files beneath `IT_PLUGINS_STATE_DIR`:

- `global.json` – global defaults.
- `users/<userId>.json` – per user overrides.

## Caching

Registry and health responses are cached for `IT_PLUGINS_CACHE_TTL_SEC` seconds to reduce filesystem and network load.
