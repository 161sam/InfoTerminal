# Feed Connector Quickstart (RSS + OTX)

This guide explains how to run the RSS feed MVP and the new AlienVault OTX
threat-intel connector. Both connectors share the same FastAPI service and
expose feature-flag aware endpoints plus Prometheus counters for observability.

## Prerequisites

- Python environment for `services/feed-ingestor`.
- Prometheus/Grafana stack (optional) for the new feed metrics.
- Environment flags:
  - `FEEDS_ENABLED=1`
  - `RSS_ENABLED=1`
  - `FEED_OTX_ENABLED=1`
  - Optional RSS overrides: `RSS_FEED_URL` (defaults to
    `https://example.com/rss.xml`), `RSS_FETCH_INTERVAL` (seconds, default
    `300`), `RSS_DRY_RUN` (`1` to skip ingestion during periodic runs).
  - Optional OTX overrides: `OTX_API_URL`
    (defaults to `https://otx.alienvault.com/api/v1/pulses/subscribed`),
    `OTX_FETCH_INTERVAL` (seconds, default `900`), `OTX_DRY_RUN` (`1` to keep
    the seen-cache untouched during scheduled runs).

Example `.env` snippet:

```bash
export FEEDS_ENABLED=1
export RSS_ENABLED=1
export FEED_OTX_ENABLED=1
export RSS_FEED_URL="file://$(pwd)/examples/rss/mock.xml"
export RSS_FETCH_INTERVAL=0
export OTX_API_URL="file://$(pwd)/examples/feeds/otx/mock.json"
export OTX_FETCH_INTERVAL=0
```

## Start the service

```bash
cd services/feed-ingestor
uvicorn app.main:app --reload --port 8626
```

Endpoints:

- `POST /feeds/rss/run` — fetch + normalise + ingest once. Accepts JSON body
  `{ "dry_run": false, "feed_url": "https://..." }`.
- `GET /feeds/rss/items` — list items stored in the in-memory search index.
- `DELETE /feeds/rss/items` — clear the index.
- `POST /feeds/otx/run` — fetch + normalise indicators from OTX. Accepts JSON
  `{ "dry_run": false, "api_url": "https://..." }` and returns the
  de-duplicated indicator list.
- `DELETE /feeds/otx/cache` — reset the OTX de-dup cache.
- `/metrics` — exposes `feed_items_fetched_total{source="rss"}`,
  `feed_items_fetched_total{source="otx"}`,
  `feed_items_ingested_total{source="rss",target="search"}`,
  `feed_items_ingested_total{source="otx",target="graph"}` and
  `feed_dedup_skipped_total{source="rss"|"otx"}`.
- `/healthz`, `/readyz` — feature flag aware probes with connector metadata.

Manual ingest example (using the bundled tests’ RSS snippet):

```bash
curl -s -X POST "http://localhost:8626/feeds/rss/run" \
  -H 'Content-Type: application/json' \
  -d '{"dry_run": false, "feed_url": "https://example.com/rss"}' | jq '.items[0]'

curl -s http://localhost:8626/feeds/rss/items | jq '.[] | {id,title,url}'
```

Manual OTX fetch using the bundled mock pulse:

```bash
curl -s -X POST "http://localhost:8626/feeds/otx/run" \
  -H 'Content-Type: application/json' \
  -d '{"dry_run": false, "api_url": "file://'"$(pwd)"'/examples/feeds/otx/mock.json"}' \
  | jq '.items[] | {indicator,type,first_seen}'
```

## Periodic job

When `RSS_FETCH_INTERVAL>0` the service launches a background scheduler on
startup. It fetches the configured feed on the given interval. Failures trigger
an exponential backoff (1s, 2s, 4s, … up to 5 minutes) before the next attempt.
Set `RSS_DRY_RUN=1` to validate fetch/normalise without mutating the store.

Similarly, when `OTX_FETCH_INTERVAL>0` the OTX connector runs on the configured
interval. Every non-dry-run invocation now forwards the normalised indicators to
the graph ingestion endpoint and only then marks them as seen. Repeated runs
with `dry_run=false` skip already-observed indicators using the
`source:indicator` key while keeping the graph payload idempotent.

## Metrics & dashboard

The Grafana `Infra Overview` dashboard now includes dedicated tiles for the feed
connector counters. Look for:

- **Feed Items Fetched (rss)** — total items retrieved from the RSS source.
- **Feed Items Ingested** — items written into the mock search index.
- **OTX → Graph Items Ingested** — threat indicators successfully upserted into
  the graph target.
- **Feed Dedup Skipped (rss)** — duplicates skipped because the `id` or `url`
  already existed.
- **Feed Items Fetched (otx)** — total indicators retrieved from the OTX API or
  mock file.
- **Feed Dedup Skipped (otx)** — indicators skipped due to the seen-cache.

## Offline smoke demo

1. Launch the service with the environment variables shown above (using the
   bundled RSS and OTX mock files).
2. Trigger a manual RSS run via `curl` and observe the response.
3. Trigger a manual OTX run using the mock pulse; the response should list two
   indicators and report `ingested=2` on the first run.
4. Re-run both commands with `dry_run=false` — the second invocation increments
   `feed_dedup_skipped_total{source="rss"}` and
   `feed_dedup_skipped_total{source="otx"}` due to de-duplication.
5. Check `/metrics` to ensure the counters increment;
   `feed_items_ingested_total{source="otx",target="graph"}` should rise with
   the first OTX ingest. The Grafana dashboard now shows six panels across RSS
   and OTX sources including the dedicated OTX ingest tile.

## Tests

```bash
cd services/feed-ingestor
pytest
```

The suite covers normalisation, deduplication, backoff logic, feature flag
checks, REST endpoints, and scheduler behaviour for both connectors.
