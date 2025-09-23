# RSS Feed Connector Quickstart (Iteration 04b)

This guide explains how to run the minimal RSS feed ingestion MVP delivered in
Wave 4 Iteration 04b.

## Prerequisites

- Python environment for `services/feed-ingestor`.
- Prometheus/Grafana stack (optional) for the new feed metrics.
- Environment flags:
  - `FEEDS_ENABLED=1`
  - `RSS_ENABLED=1`
  - Optional: `RSS_FEED_URL` (defaults to `https://example.com/rss.xml`),
    `RSS_FETCH_INTERVAL` (seconds, default `300`),
    `RSS_DRY_RUN` (`1` to skip ingestion during periodic runs).

Example `.env` snippet:

```bash
export FEEDS_ENABLED=1
export RSS_ENABLED=1
export RSS_FEED_URL="file://$(pwd)/examples/rss/mock.xml"
export RSS_FETCH_INTERVAL=0
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
- `/metrics` — exposes `feed_items_fetched_total{source="rss"}`,
  `feed_items_ingested_total{target="search"}` and
  `feed_dedup_skipped_total{source="rss"}`.
- `/healthz`, `/readyz` — feature flag aware probes.

Manual ingest example (using the bundled tests’ RSS snippet):

```bash
curl -s -X POST "http://localhost:8626/feeds/rss/run" \
  -H 'Content-Type: application/json' \
  -d '{"dry_run": false, "feed_url": "https://example.com/rss"}' | jq '.items[0]'

curl -s http://localhost:8626/feeds/rss/items | jq '.[] | {id,title,url}'
```

## Periodic job

When `RSS_FETCH_INTERVAL>0` the service launches a background scheduler on
startup. It fetches the configured feed on the given interval. Failures trigger
an exponential backoff (1s, 2s, 4s, … up to 5 minutes) before the next attempt.
Set `RSS_DRY_RUN=1` to validate fetch/normalise without mutating the store.

## Metrics & dashboard

The Grafana `Infra Overview` dashboard now includes three tiles for the feed
connector counters. Look for:

- **Feed Items Fetched** — total items retrieved from the RSS source.
- **Feed Items Ingested** — items written into the mock search index.
- **Feed Dedup Skipped** — duplicates skipped because the `id` or `url`
  already existed.

## Offline smoke demo

1. Launch the service with the environment variables shown above (using a local
   RSS file or the sample from tests).
2. Trigger a manual run via `curl` and observe the response.
3. Call `GET /feeds/rss/items` to verify the normalised entries are present.
4. Check `/metrics` to ensure the counters increment; the Grafana dashboard
   shows live values for the three new panels.
5. Re-run the `POST /feeds/rss/run` call — the second invocation increments
   `feed_dedup_skipped_total` because of de-duplication.

## Tests

```bash
cd services/feed-ingestor
pytest
```

The suite covers normalisation, deduplication, backoff logic, feature flag
checks, REST endpoints, and scheduler behaviour.
