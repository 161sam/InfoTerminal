# Superset assets

This directory contains dataset, chart and dashboard exports for Superset.

Use `scripts/import.sh` to import them:

```bash
export SUPERTSET_TOKEN=... # API token
export SUPERTSET_URL=https://superset.example.com
./scripts/import.sh
```

The import script expects the Superset API to be reachable and uses the provided token.
