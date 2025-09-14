# Plugin System

Plugins reside under the directory specified by `IT_PLUGINS_DIR` and expose a `plugin.yaml` manifest.
The agent connector discovers these manifests, caches them for quick access, and exposes
`/plugins/tools` and `/plugins/invoke/{plugin}/{tool}` endpoints.
Enable the system via `IT_PLUGINS_ENABLE=1` and control cache TTL with `IT_PLUGINS_CACHE_TTL_SEC`.
