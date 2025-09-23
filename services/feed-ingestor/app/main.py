"""RSS feed connector MVP for Iteration 04b (I1).

This FastAPI service fetches an RSS/Atom feed, normalises entries, performs
idempotent ingestion into an in-memory search index, and exposes Prometheus
counters plus a periodic scheduler with exponential backoff.
"""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree as ET

import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from prometheus_client import Counter
from starlette.middleware.cors import CORSMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics

logger = logging.getLogger("feed-ingestor")
logging.basicConfig(level=logging.INFO)

RSS_SOURCE = os.getenv("RSS_FEED_URL", "https://example.com/rss.xml")
FETCH_INTERVAL_SECONDS = int(os.getenv("RSS_FETCH_INTERVAL", "300"))
RSS_DRY_RUN_DEFAULT = os.getenv("RSS_DRY_RUN", "1") == "1"


# ---------------------------------------------------------------------------
# Feature flags
# ---------------------------------------------------------------------------


def feeds_enabled() -> bool:
    return os.getenv("FEEDS_ENABLED", "0") == "1"


def rss_enabled() -> bool:
    return os.getenv("RSS_ENABLED", "0") == "1"


def require_feeds_enabled() -> None:
    if not feeds_enabled():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Feeds module disabled. Set FEEDS_ENABLED=1 to activate.",
        )


def require_rss_enabled() -> None:
    if not rss_enabled():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RSS connector disabled. Set RSS_ENABLED=1 to activate.",
        )


# ---------------------------------------------------------------------------
# Models & storage
# ---------------------------------------------------------------------------


class FeedItem(BaseModel):
    id: str
    title: str
    url: str
    published_at: str
    summary: Optional[str] = None


class RunRequest(BaseModel):
    dry_run: Optional[bool] = Field(
        default=None,
        description="Skip ingestion when true (defaults to RSS_DRY_RUN env flag).",
    )
    feed_url: Optional[str] = Field(
        default=None,
        description="Override feed URL for this run.",
    )


class RunResponse(BaseModel):
    fetched: int
    ingested: int
    deduped: int
    dry_run: bool
    items: List[FeedItem]


class FeedStore:
    """In-memory search index representation for the MVP."""

    def __init__(self) -> None:
        self._items: Dict[str, FeedItem] = {}

    def upsert(self, item: FeedItem) -> None:
        self._items[item.id] = item

    def exists(self, item: FeedItem) -> bool:
        return item.id in self._items or any(existing.url == item.url for existing in self._items.values())

    def list_items(self) -> List[FeedItem]:
        return sorted(self._items.values(), key=lambda entry: entry.published_at, reverse=True)

    def clear(self) -> None:
        self._items.clear()


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

feed_items_fetched_total = Counter(
    "feed_items_fetched_total",
    "Total items fetched from external feeds.",
    labelnames=("source",),
)
feed_items_ingested_total = Counter(
    "feed_items_ingested_total",
    "Total items ingested into downstream targets.",
    labelnames=("target",),
)
feed_dedup_skipped_total = Counter(
    "feed_dedup_skipped_total",
    "Items skipped because they were already ingested.",
    labelnames=("source",),
)


# ---------------------------------------------------------------------------
# RSS parsing helpers
# ---------------------------------------------------------------------------


@dataclass
class FetchResult:
    items: List[FeedItem]
    fetched: int
    deduped: int
    ingested: int


class RSSParser:
    @staticmethod
    def parse_date(value: Optional[str]) -> str:
        if not value:
            return datetime.utcnow().isoformat() + "Z"
        try:
            parsed = parsedate_to_datetime(value)
            if parsed is None:
                raise ValueError
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=datetime.utcnow().astimezone().tzinfo)
            return parsed.isoformat()
        except Exception:
            return datetime.utcnow().isoformat() + "Z"

    def normalize(self, xml: str) -> List[FeedItem]:
        root = ET.fromstring(xml)
        items: List[FeedItem] = []
        rss_nodes = root.findall('.//item')
        atom_nodes = root.findall('.//{http://www.w3.org/2005/Atom}entry')
        for node in rss_nodes + atom_nodes:
            guid = node.findtext('guid') or node.findtext('id') or node.findtext('link')
            link = node.findtext('link') or node.findtext('{http://www.w3.org/2005/Atom}link')
            if isinstance(link, str) and not link.startswith('http'):
                href = node.find('{http://www.w3.org/2005/Atom}link')
                if href is not None:
                    link = href.attrib.get('href', link)
            title = node.findtext('title') or node.findtext('{http://www.w3.org/2005/Atom}title') or 'Untitled item'
            summary = node.findtext('description') or node.findtext('{http://www.w3.org/2005/Atom}summary')
            published = (
                node.findtext('pubDate')
                or node.findtext('{http://www.w3.org/2005/Atom}updated')
                or node.findtext('{http://www.w3.org/2005/Atom}published')
            )
            normalized = FeedItem(
                id=(guid or link or title),
                title=title.strip(),
                url=(link or guid or ""),
                published_at=self.parse_date(published),
                summary=summary.strip() if summary else None,
            )
            items.append(normalized)
        return items


class RSSClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=10.0)

    async def fetch(self, url: str) -> str:
        response = await self._client.get(url)
        response.raise_for_status()
        return response.text

    async def aclose(self) -> None:
        await self._client.aclose()


class FeedPipeline:
    def __init__(self, store: FeedStore) -> None:
        self.store = store
        self.parser = RSSParser()
        self.client = RSSClient()

    async def run(self, feed_url: str, dry_run: bool) -> FetchResult:
        xml = await self.client.fetch(feed_url)
        items = self.parser.normalize(xml)
        feed_items_fetched_total.labels(source="rss").inc(len(items))

        ingested = 0
        deduped = 0
        stored: List[FeedItem] = []
        for item in items:
            if self.store.exists(item):
                deduped += 1
                feed_dedup_skipped_total.labels(source="rss").inc()
                continue
            if not dry_run:
                self.store.upsert(item)
                feed_items_ingested_total.labels(target="search").inc()
                ingested += 1
            stored.append(item)
        return FetchResult(items=stored, fetched=len(items), deduped=deduped, ingested=ingested)

    async def close(self) -> None:
        await self.client.aclose()


class ExponentialBackoff:
    def __init__(self, base: float = 1.0, factor: float = 2.0, max_interval: float = 300.0) -> None:
        self.base = base
        self.factor = factor
        self.max_interval = max_interval
        self.attempt = 0

    def next_delay(self) -> float:
        delay = min(self.base * (self.factor ** self.attempt), self.max_interval)
        self.attempt += 1
        return delay

    def reset(self) -> None:
        self.attempt = 0


store = FeedStore()
pipeline = FeedPipeline(store)
backoff = ExponentialBackoff()

app = FastAPI(title="RSS Feed Connector", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(PrometheusMiddleware, app_name="feed-ingestor")
app.add_route("/metrics", handle_metrics)

scheduler_task: Optional[asyncio.Task] = None


async def scheduler_loop() -> None:
    logger.info("Starting RSS scheduler", extra={"interval": FETCH_INTERVAL_SECONDS})
    while True:
        delay = FETCH_INTERVAL_SECONDS
        try:
            result = await pipeline.run(RSS_SOURCE, dry_run=RSS_DRY_RUN_DEFAULT)
            backoff.reset()
            logger.info(
                "rss_run",
                extra={
                    "fetched": result.fetched,
                    "ingested": result.ingested,
                    "deduped": result.deduped,
                    "dry_run": RSS_DRY_RUN_DEFAULT,
                },
            )
        except Exception as exc:  # pragma: no cover - tested via backoff logic
            delay = backoff.next_delay()
            logger.error("rss_run_failed", exc_info=exc, extra={"delay": delay})
        await asyncio.sleep(delay)


@app.on_event("startup")
async def startup() -> None:
    global scheduler_task
    if feeds_enabled() and rss_enabled() and FETCH_INTERVAL_SECONDS > 0:
        scheduler_task = asyncio.create_task(scheduler_loop())


@app.on_event("shutdown")
async def shutdown() -> None:
    global scheduler_task
    if scheduler_task:
        scheduler_task.cancel()
        try:
            await scheduler_task
        except asyncio.CancelledError:
            pass
    await pipeline.close()


@app.get("/healthz")
def healthz() -> Dict[str, Any]:
    return {
        "status": "ok",
        "feeds_enabled": feeds_enabled(),
        "rss_enabled": rss_enabled(),
    }


@app.get("/readyz")
def readyz() -> Dict[str, Any]:
    return {
        "status": "ready" if feeds_enabled() else "disabled",
        "feeds_enabled": feeds_enabled(),
        "rss_enabled": rss_enabled(),
        "interval_seconds": FETCH_INTERVAL_SECONDS,
        "dry_run": RSS_DRY_RUN_DEFAULT,
    }


@app.post("/feeds/rss/run", response_model=RunResponse)
async def run_feed(request: RunRequest, _: None = Depends(require_feeds_enabled), __: None = Depends(require_rss_enabled)) -> RunResponse:
    dry_run = RSS_DRY_RUN_DEFAULT if request.dry_run is None else request.dry_run
    feed_url = request.feed_url or RSS_SOURCE
    result = await pipeline.run(feed_url, dry_run)
    return RunResponse(
        fetched=result.fetched,
        ingested=result.ingested,
        deduped=result.deduped,
        dry_run=dry_run,
        items=result.items,
    )


@app.get("/feeds/rss/items", response_model=List[FeedItem])
async def list_items(_: None = Depends(require_feeds_enabled)) -> List[FeedItem]:
    return store.list_items()


@app.delete("/feeds/rss/items")
async def clear_items(_: None = Depends(require_feeds_enabled)) -> Dict[str, Any]:
    store.clear()
    return {"status": "cleared"}


__all__ = [
    "app",
    "RSSParser",
    "FeedStore",
    "FeedPipeline",
    "ExponentialBackoff",
    "feed_items_fetched_total",
    "feed_items_ingested_total",
    "feed_dedup_skipped_total",
]
