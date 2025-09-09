# Analytics frontend & Superset

## Superset assets

Assets live in `apps/superset/assets`. Import them via:

```bash
cd apps/superset/assets
SUPERTSET_URL=https://superset.example.com \
SUPERTSET_TOKEN=token ./scripts/import.sh
```

## Deep links

Charts generate links of form:
`https://INFOTERMINAL_BASE_URL/asset/{asset_id}?from=YYYY-MM-DD&to=YYYY-MM-DD&tab=chart`

## Frontend pages

- `/asset/[id]` – tabs: Kurs (chart & OHLC), Graph, News
- `/person/[id]` – tabs: Graph, News

Query parameters `from`, `to`, `tab` pre-select ranges and tabs.

## Tests

Run unit tests and e2e:

```bash
pnpm -w test
pnpm -w e2e
```
