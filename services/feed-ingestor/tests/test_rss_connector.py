import asyncio

import pytest

from app import main as feed_main
from types import SimpleNamespace

from app.main import (
    ExponentialBackoff,
    FeedPipeline,
    FeedStore,
    RSSParser,
    RSSClient,
    rss_scheduler_loop,
    feed_dedup_skipped_total,
    feed_items_fetched_total,
    feed_items_ingested_total,
)

RSS_SAMPLE = """
<rss version="2.0">
  <channel>
    <title>Example Feed</title>
    <item>
      <title>Item One</title>
      <link>https://example.com/1</link>
      <guid>item-1</guid>
      <pubDate>Wed, 24 Sep 2025 12:00:00 GMT</pubDate>
      <description>Summary 1</description>
    </item>
  </channel>
</rss>
"""


def get_counter(counter, **labels):
    if labels:
        metric = counter._metrics.get(tuple(labels.values()))  # type: ignore[attr-defined]
        if metric is None:
            return 0.0
        return metric._value.get()  # type: ignore[attr-defined]
    return counter._value.get()  # type: ignore[attr-defined]


def test_normalizer_extracts_core_fields():
    parser = RSSParser()
    items = parser.normalize(RSS_SAMPLE)
    assert len(items) == 1
    item = items[0]
    assert item.id == "item-1"
    assert item.title == "Item One"
    assert item.url == "https://example.com/1"
    assert item.summary == "Summary 1"
    from datetime import datetime

    parsed = datetime.fromisoformat(item.published_at.replace("Z", "+00:00"))
    assert parsed.year == 2025


def test_parse_date_handles_invalid_and_naive():
    parser = RSSParser()
    iso = parser.parse_date("Wed, 24 Sep 2025 12:00:00")
    assert "2025" in iso
    fallback = parser.parse_date("not-a-date")
    assert isinstance(fallback, str)
    assert len(fallback) > 10


@pytest.mark.anyio
async def test_pipeline_deduplicates_and_counts(monkeypatch):
    store = FeedStore()
    pipeline = FeedPipeline(store)

    async def fake_fetch(url: str) -> str:  # noqa: ARG001
        return RSS_SAMPLE

    monkeypatch.setattr(pipeline.client, "fetch", fake_fetch)

    fetched_before = get_counter(feed_items_fetched_total, source="rss")
    ingested_before = get_counter(feed_items_ingested_total, target="search")
    dedup_before = get_counter(feed_dedup_skipped_total, source="rss")

    result_first = await pipeline.run("https://example.com/rss", dry_run=False)
    assert result_first.ingested == 1

    result_second = await pipeline.run("https://example.com/rss", dry_run=False)
    assert result_second.ingested == 0
    assert result_second.deduped == 1

    fetched_after = get_counter(feed_items_fetched_total, source="rss")
    ingested_after = get_counter(feed_items_ingested_total, target="search")
    dedup_after = get_counter(feed_dedup_skipped_total, source="rss")

    assert fetched_after == pytest.approx(fetched_before + 2)
    assert ingested_after == pytest.approx(ingested_before + 1)
    assert dedup_after == pytest.approx(dedup_before + 1)


def test_backoff_sequence():
    backoff = ExponentialBackoff(base=1, factor=2, max_interval=10)
    assert backoff.next_delay() == 1
    assert backoff.next_delay() == 2
    assert backoff.next_delay() == 4
    backoff.reset()
    assert backoff.next_delay() == 1


@pytest.mark.anyio
async def test_run_endpoint_uses_pipeline(monkeypatch, client):
    async def fake_fetch(url: str) -> str:  # noqa: ARG001
        return RSS_SAMPLE

    monkeypatch.setattr("app.main.rss_pipeline.client.fetch", fake_fetch)
    response = await client.post("/feeds/rss/run", json={"dry_run": False})
    assert response.status_code == 200
    body = response.json()
    assert body["fetched"] == 1
    assert body["ingested"] == 1
    items = await client.get("/feeds/rss/items")
    assert items.status_code == 200
    assert len(items.json()) == 1


@pytest.mark.anyio
async def test_clear_items_endpoint(client):
    response = await client.delete("/feeds/rss/items")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_feature_flags_block(monkeypatch, client):
    monkeypatch.setenv("FEEDS_ENABLED", "0")
    response = await client.get("/feeds/rss/items")
    assert response.status_code == 503

    monkeypatch.setenv("FEEDS_ENABLED", "1")
    monkeypatch.setenv("RSS_ENABLED", "0")
    response = await client.post("/feeds/rss/run")
    assert response.status_code == 503

    monkeypatch.setenv("RSS_ENABLED", "1")
    monkeypatch.setenv("FEED_OTX_ENABLED", "0")
    response = await client.post("/feeds/otx/run")
    assert response.status_code == 503


@pytest.mark.anyio
async def test_startup_scheduler(monkeypatch):
    async def fake_run(url: str, dry_run: bool):  # noqa: ARG001
        from app.main import FetchResult, FeedItem

        return FetchResult(
            items=[FeedItem(id="x", title="X", url="http://x", published_at="2025-09-24T00:00:00Z")],
            fetched=1,
            deduped=0,
            ingested=0,
        )

    monkeypatch.setenv("FEEDS_ENABLED", "1")
    monkeypatch.setenv("RSS_ENABLED", "1")
    feed_main.FETCH_INTERVAL_SECONDS = 1
    monkeypatch.setattr(feed_main.rss_pipeline, "run", fake_run)

    await feed_main.startup()  # type: ignore[attr-defined]
    assert feed_main.rss_scheduler_task is not None
    feed_main.rss_scheduler_task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await feed_main.rss_scheduler_task
    await feed_main.rss_pipeline.close()
    feed_main.rss_scheduler_task = None
    feed_main.FETCH_INTERVAL_SECONDS = 0


@pytest.mark.anyio
async def test_rss_client_fetch(monkeypatch):
    client = RSSClient()

    async def fake_get(url: str):  # noqa: ARG001
        return SimpleNamespace(text="<rss></rss>", raise_for_status=lambda: None)

    monkeypatch.setattr(client._client, "get", fake_get)
    text = await client.fetch("https://example.com")
    assert text == "<rss></rss>"
    await client.aclose()


@pytest.mark.anyio
async def test_scheduler_loop_handles_error(monkeypatch):
    from app.main import FetchResult, FeedItem

    call_count = {"value": 0}

    async def fake_run(url: str, dry_run: bool):  # noqa: ARG001
        call_count["value"] += 1
        if call_count["value"] == 1:
            raise RuntimeError("boom")
        return FetchResult(
            items=[FeedItem(id="y", title="Y", url="http://y", published_at="2025-09-24T00:00:00Z")],
            fetched=1,
            deduped=0,
            ingested=0,
        )

    async def fake_sleep(delay: float):  # noqa: ARG001
        raise asyncio.CancelledError

    monkeypatch.setattr(feed_main.rss_pipeline, "run", fake_run)
    monkeypatch.setenv("FEEDS_ENABLED", "1")
    monkeypatch.setenv("RSS_ENABLED", "1")
    feed_main.RSS_DRY_RUN_DEFAULT = False
    monkeypatch.setattr("app.main.asyncio.sleep", fake_sleep)

    with pytest.raises(asyncio.CancelledError):
        await rss_scheduler_loop()
    feed_main.RSS_DRY_RUN_DEFAULT = True

