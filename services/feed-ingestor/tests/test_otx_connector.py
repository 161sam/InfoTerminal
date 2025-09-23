import asyncio

import pytest

from app import main as feed_main

from app.main import (
    OTXNormalizer,
    OTXPipeline,
    OTXStore,
    otx_backoff,
    otx_scheduler_loop,
    feed_dedup_skipped_total,
    feed_items_fetched_total,
    feed_items_ingested_total,
)

OTX_SAMPLE = {
    "results": [
        {
            "name": "Pulse Alpha",
            "tags": ["apt", "phishing"],
            "created": "2024-05-10T12:00:00",
            "indicators": [
                {
                    "indicator": "1.2.3.4",
                    "type": "IPv4",
                    "first_seen": "2024-05-01T00:00:00Z",
                    "tags": ["ipv4", "alpha"],
                }
            ],
        }
    ]
}


def read_counter(counter, **labels):
    if labels:
        key = tuple(labels[name] for name in counter._labelnames)  # type: ignore[attr-defined]
        metric = counter._metrics.get(key)  # type: ignore[attr-defined]
        if metric is None:
            return 0.0
        return metric._value.get()  # type: ignore[attr-defined]
    return counter._value.get()  # type: ignore[attr-defined]


@pytest.mark.anyio
async def test_otx_normalizer_extracts_fields():
    normalizer = OTXNormalizer()
    items = normalizer.normalize(OTX_SAMPLE)
    assert len(items) == 1
    item = items[0]
    assert item.indicator == "1.2.3.4"
    assert item.type == "IPv4"
    assert item.first_seen.startswith("2024-05-01")
    assert item.source == "Pulse Alpha"
    assert item.tags == ["apt", "phishing", "ipv4", "alpha"]


@pytest.mark.anyio
async def test_otx_pipeline_deduplicates(monkeypatch):
    store = OTXStore()
    captured = {"payloads": []}

    class FakeGraphClient:
        async def ingest_threat_indicators(self, payload):
            captured["payloads"].append(payload)
            return {"status": "ok", "ingested": len(payload["items"])}

        async def close(self):
            return None

    pipeline = OTXPipeline(store, ingest_client=FakeGraphClient())

    async def fake_fetch(url: str):  # noqa: ARG001
        return OTX_SAMPLE

    monkeypatch.setattr(pipeline.client, "fetch", fake_fetch)

    fetched_before = read_counter(feed_items_fetched_total, source="otx")
    dedup_before = read_counter(feed_dedup_skipped_total, source="otx")
    ingested_before = read_counter(
        feed_items_ingested_total, source="otx", target="graph"
    )

    first = await pipeline.run("https://example.com", dry_run=False)
    assert first.fetched == 1
    assert first.deduped == 0
    assert len(first.items) == 1
    assert store.seen(first.items[0])
    assert first.ingested == 1
    assert captured["payloads"]

    second = await pipeline.run("https://example.com", dry_run=False)
    assert second.deduped == 1
    assert len(second.items) == 0
    assert second.ingested == 0
    assert len(captured["payloads"]) == 1

    fetched_after = read_counter(feed_items_fetched_total, source="otx")
    dedup_after = read_counter(feed_dedup_skipped_total, source="otx")
    ingested_after = read_counter(
        feed_items_ingested_total, source="otx", target="graph"
    )

    assert fetched_after == pytest.approx(fetched_before + 2)
    assert dedup_after == pytest.approx(dedup_before + 1)
    assert ingested_after == pytest.approx(ingested_before + 1)

    await pipeline.close()


@pytest.mark.anyio
async def test_otx_run_endpoint(monkeypatch, client):
    async def fake_fetch(url: str):  # noqa: ARG001
        return OTX_SAMPLE

    monkeypatch.setattr("app.main.otx_pipeline.client.fetch", fake_fetch)
    response = await client.post("/feeds/otx/run", json={"dry_run": False})
    assert response.status_code == 200
    body = response.json()
    assert body["fetched"] == 1
    assert body["deduped"] == 0
    assert body["ingested"] == 1
    assert body["dry_run"] is False
    assert body["items"][0]["indicator"] == "1.2.3.4"

    clear = await client.delete("/feeds/otx/cache")
    assert clear.status_code == 200


@pytest.mark.anyio
async def test_otx_scheduler_loop_backoff(monkeypatch):
    call_count = {"value": 0}
    inner_pipeline = OTXPipeline(OTXStore())

    async def fake_fetch(url: str):  # noqa: ARG001
        return OTX_SAMPLE

    monkeypatch.setattr(inner_pipeline.client, "fetch", fake_fetch)

    async def fake_run(url: str, dry_run: bool):  # noqa: ARG001
        call_count["value"] += 1
        if call_count["value"] == 1:
            raise RuntimeError("boom")
        return await inner_pipeline.run(url, dry_run)

    async def fake_sleep(delay: float):  # noqa: ARG001
        raise asyncio.CancelledError

    monkeypatch.setattr(feed_main.otx_pipeline, "run", fake_run)
    monkeypatch.setattr("app.main.asyncio.sleep", fake_sleep)
    monkeypatch.setattr("app.main.otx_backoff.next_delay", lambda: 0.1)

    with pytest.raises(asyncio.CancelledError):
        await otx_scheduler_loop()

    await inner_pipeline.close()
    otx_backoff.reset()
