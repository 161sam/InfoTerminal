"""Feed connector service (RSS + OTX) for Iteration 04b (I1).

This FastAPI application fetches RSS/Atom feeds and AlienVault OTX pulses,
normalises entries, performs idempotent operations (ingest for RSS, seen-cache
for OTX), and exposes Prometheus counters plus periodic schedulers with
exponential backoff.
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from xml.etree import ElementTree as ET

import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from prometheus_client import Counter
from starlette.middleware.cors import CORSMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics

SERVICE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_DIR.parent.parent.parent
shared_path = REPO_ROOT / "services"
if str(shared_path) not in sys.path:
    sys.path.insert(0, str(shared_path))

from _shared.clients.graph_ingest import GraphIngestClient

logger = logging.getLogger("feed-ingestor")
logging.basicConfig(level=logging.INFO)

RSS_SOURCE = os.getenv("RSS_FEED_URL", "https://example.com/rss.xml")
FETCH_INTERVAL_SECONDS = int(os.getenv("RSS_FETCH_INTERVAL", "300"))
RSS_DRY_RUN_DEFAULT = os.getenv("RSS_DRY_RUN", "1") == "1"

OTX_SOURCE = os.getenv(
    "OTX_API_URL", "https://otx.alienvault.com/api/v1/pulses/subscribed"
)
OTX_FETCH_INTERVAL_SECONDS = int(os.getenv("OTX_FETCH_INTERVAL", "900"))
OTX_DRY_RUN_DEFAULT = os.getenv("OTX_DRY_RUN", "1") == "1"


# ---------------------------------------------------------------------------
# Feature flags
# ---------------------------------------------------------------------------


def feeds_enabled() -> bool:
    return os.getenv("FEEDS_ENABLED", "0") == "1"


def rss_enabled() -> bool:
    return os.getenv("RSS_ENABLED", "0") == "1"


def otx_enabled() -> bool:
    return os.getenv("FEED_OTX_ENABLED", "0") == "1"


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


def require_otx_enabled() -> None:
    if not otx_enabled():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OTX connector disabled. Set FEED_OTX_ENABLED=1 to activate.",
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


class OTXIndicator(BaseModel):
    indicator: str
    type: str
    first_seen: Optional[str]
    source: str
    tags: Optional[List[str]] = None


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


class OTXRunRequest(BaseModel):
    dry_run: Optional[bool] = Field(
        default=None,
        description="Skip persisting seen indicators when true (defaults to OTX_DRY_RUN env flag).",
    )
    api_url: Optional[str] = Field(
        default=None,
        description="Override the OTX API URL for this run.",
    )


class OTXRunResponse(BaseModel):
    fetched: int
    deduped: int
    ingested: int
    dry_run: bool
    items: List[OTXIndicator]


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


class OTXStore:
    """Track indicators that were already observed to support de-duplication."""

    def __init__(self) -> None:
        self._seen: Set[str] = set()

    @staticmethod
    def _key(item: OTXIndicator) -> str:
        return f"{item.source}:{item.indicator}"

    def seen(self, item: OTXIndicator) -> bool:
        return self._key(item) in self._seen

    def mark(self, item: OTXIndicator) -> None:
        self._seen.add(self._key(item))

    def clear(self) -> None:
        self._seen.clear()


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
    labelnames=("source", "target"),
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


@dataclass
class OTXFetchResult:
    items: List[OTXIndicator]
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


class OTXNormalizer:
    @staticmethod
    def parse_datetime(value: Optional[str]) -> Optional[str]:
        if not value:
            return None
        try:
            cleaned = value.replace("Z", "+00:00")
            parsed = datetime.fromisoformat(cleaned)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.isoformat()
        except Exception:
            return None

    def normalize(self, payload: Dict[str, Any]) -> List[OTXIndicator]:
        pulses = payload.get("results") or []
        indicators: List[OTXIndicator] = []
        for pulse in pulses:
            source = str(pulse.get("name") or pulse.get("id") or "otx")
            pulse_tags = [tag for tag in pulse.get("tags", []) if isinstance(tag, str)]
            for indicator in pulse.get("indicators", []) or []:
                indicator_value = indicator.get("indicator") or indicator.get("value")
                if not indicator_value:
                    continue
                indicator_type = indicator.get("type") or indicator.get("indicator_type") or "unknown"
                first_seen = indicator.get("first_seen") or indicator.get("created") or pulse.get("created")
                normalised_first_seen = self.parse_datetime(first_seen)
                indicator_tags = [tag for tag in indicator.get("tags", []) if isinstance(tag, str)]
                combined_tags = pulse_tags + indicator_tags
                unique_tags = list(dict.fromkeys(combined_tags)) if combined_tags else None
                indicators.append(
                    OTXIndicator(
                        indicator=str(indicator_value),
                        type=str(indicator_type),
                        first_seen=normalised_first_seen,
                        source=source,
                        tags=unique_tags,
                    )
                )
        return indicators


class OTXClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=10.0)

    async def fetch(self, url: str) -> Dict[str, Any]:
        response = await self._client.get(url)
        response.raise_for_status()
        return response.json()

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
                feed_items_ingested_total.labels(
                    source="rss", target="search"
                ).inc()
                ingested += 1
            stored.append(item)
        return FetchResult(items=stored, fetched=len(items), deduped=deduped, ingested=ingested)

    async def close(self) -> None:
        await self.client.aclose()


class OTXPipeline:
    def __init__(
        self, store: OTXStore, ingest_client: Optional[GraphIngestClient] = None
    ) -> None:
        self.store = store
        self.normalizer = OTXNormalizer()
        self.client = OTXClient()
        self.ingest_client = ingest_client

    async def run(self, api_url: str, dry_run: bool) -> OTXFetchResult:
        payload = await self.client.fetch(api_url)
        items = self.normalizer.normalize(payload)
        feed_items_fetched_total.labels(source="otx").inc(len(items))

        deduped = 0
        delivered: List[OTXIndicator] = []
        for item in items:
            if self.store.seen(item):
                deduped += 1
                feed_dedup_skipped_total.labels(source="otx").inc()
                continue
            delivered.append(item)
        ingested = 0
        if not dry_run and delivered:
            if self.ingest_client is not None:
                try:
                    response = await self.ingest_client.ingest_threat_indicators(
                        {"items": [item.model_dump() for item in delivered]}
                    )
                    ingested = int(response.get("ingested", len(delivered)))
                    for item in delivered:
                        self.store.mark(item)
                    if ingested:
                        feed_items_ingested_total.labels(
                            source="otx", target="graph"
                        ).inc(ingested)
                except Exception as exc:  # pragma: no cover - network failure path
                    logger.warning("otx_graph_ingest_failed", exc_info=exc)
            else:
                for item in delivered:
                    self.store.mark(item)
                ingested = len(delivered)
        elif not dry_run:
            for item in delivered:
                self.store.mark(item)
        return OTXFetchResult(
            items=delivered, fetched=len(items), deduped=deduped, ingested=ingested
        )

    async def close(self) -> None:
        await self.client.aclose()
        if self.ingest_client is not None:
            await self.ingest_client.close()


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


rss_store = FeedStore()
rss_pipeline = FeedPipeline(rss_store)
rss_backoff = ExponentialBackoff()

otx_store = OTXStore()
graph_ingest_client = GraphIngestClient()
otx_pipeline = OTXPipeline(otx_store, ingest_client=graph_ingest_client)
otx_backoff = ExponentialBackoff()

app = FastAPI(title="Feed Connector Service", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(PrometheusMiddleware, app_name="feed-ingestor")
app.add_route("/metrics", handle_metrics)

rss_scheduler_task: Optional[asyncio.Task] = None
otx_scheduler_task: Optional[asyncio.Task] = None


async def rss_scheduler_loop() -> None:
    logger.info("Starting RSS scheduler", extra={"interval": FETCH_INTERVAL_SECONDS})
    while True:
        delay = FETCH_INTERVAL_SECONDS
        try:
            result = await rss_pipeline.run(RSS_SOURCE, dry_run=RSS_DRY_RUN_DEFAULT)
            rss_backoff.reset()
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
            delay = rss_backoff.next_delay()
            logger.error("rss_run_failed", exc_info=exc, extra={"delay": delay})
        await asyncio.sleep(delay)


async def otx_scheduler_loop() -> None:
    logger.info("Starting OTX scheduler", extra={"interval": OTX_FETCH_INTERVAL_SECONDS})
    while True:
        delay = OTX_FETCH_INTERVAL_SECONDS
        try:
            result = await otx_pipeline.run(OTX_SOURCE, dry_run=OTX_DRY_RUN_DEFAULT)
            otx_backoff.reset()
            logger.info(
                "otx_run",
                extra={
                    "fetched": result.fetched,
                    "deduped": result.deduped,
                    "ingested": result.ingested,
                    "dry_run": OTX_DRY_RUN_DEFAULT,
                },
            )
        except Exception as exc:  # pragma: no cover - tested via backoff logic
            delay = otx_backoff.next_delay()
            logger.error("otx_run_failed", exc_info=exc, extra={"delay": delay})
        await asyncio.sleep(delay)


@app.on_event("startup")
async def startup() -> None:
    global rss_scheduler_task, otx_scheduler_task
    if feeds_enabled() and rss_enabled() and FETCH_INTERVAL_SECONDS > 0:
        rss_scheduler_task = asyncio.create_task(rss_scheduler_loop())
    if feeds_enabled() and otx_enabled() and OTX_FETCH_INTERVAL_SECONDS > 0:
        otx_scheduler_task = asyncio.create_task(otx_scheduler_loop())


@app.on_event("shutdown")
async def shutdown() -> None:
    global rss_scheduler_task, otx_scheduler_task
    for task in (rss_scheduler_task, otx_scheduler_task):
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
    rss_scheduler_task = None
    otx_scheduler_task = None
    await rss_pipeline.close()
    await otx_pipeline.close()


@app.get("/healthz")
def healthz() -> Dict[str, Any]:
    return {
        "status": "ok",
        "feeds_enabled": feeds_enabled(),
        "rss_enabled": rss_enabled(),
        "otx_enabled": otx_enabled(),
    }


@app.get("/readyz")
def readyz() -> Dict[str, Any]:
    return {
        "status": "ready" if feeds_enabled() else "disabled",
        "feeds_enabled": feeds_enabled(),
        "rss_enabled": rss_enabled(),
        "otx_enabled": otx_enabled(),
        "rss_interval_seconds": FETCH_INTERVAL_SECONDS,
        "rss_dry_run": RSS_DRY_RUN_DEFAULT,
        "otx_interval_seconds": OTX_FETCH_INTERVAL_SECONDS,
        "otx_dry_run": OTX_DRY_RUN_DEFAULT,
    }


@app.post("/feeds/rss/run", response_model=RunResponse)
async def run_feed(request: RunRequest, _: None = Depends(require_feeds_enabled), __: None = Depends(require_rss_enabled)) -> RunResponse:
    dry_run = RSS_DRY_RUN_DEFAULT if request.dry_run is None else request.dry_run
    feed_url = request.feed_url or RSS_SOURCE
    result = await rss_pipeline.run(feed_url, dry_run)
    return RunResponse(
        fetched=result.fetched,
        ingested=result.ingested,
        deduped=result.deduped,
        dry_run=dry_run,
        items=result.items,
    )


@app.get("/feeds/rss/items", response_model=List[FeedItem])
async def list_items(_: None = Depends(require_feeds_enabled)) -> List[FeedItem]:
    return rss_store.list_items()


@app.delete("/feeds/rss/items")
async def clear_items(_: None = Depends(require_feeds_enabled)) -> Dict[str, Any]:
    rss_store.clear()
    return {"status": "cleared"}


@app.post("/feeds/otx/run", response_model=OTXRunResponse)
async def run_otx(
    request: OTXRunRequest,
    _: None = Depends(require_feeds_enabled),
    __: None = Depends(require_otx_enabled),
) -> OTXRunResponse:
    dry_run = OTX_DRY_RUN_DEFAULT if request.dry_run is None else request.dry_run
    api_url = request.api_url or OTX_SOURCE
    result = await otx_pipeline.run(api_url, dry_run)
    return OTXRunResponse(
        fetched=result.fetched,
        deduped=result.deduped,
        ingested=result.ingested,
        dry_run=dry_run,
        items=result.items,
    )


@app.delete("/feeds/otx/cache")
async def clear_otx_cache(
    _: None = Depends(require_feeds_enabled), __: None = Depends(require_otx_enabled)
) -> Dict[str, Any]:
    otx_store.clear()
    return {"status": "cleared"}


__all__ = [
    "app",
    "RSSParser",
    "FeedStore",
    "FeedPipeline",
    "OTXNormalizer",
    "OTXStore",
    "OTXPipeline",
    "OTXIndicator",
    "ExponentialBackoff",
    "feed_items_fetched_total",
    "feed_items_ingested_total",
    "feed_dedup_skipped_total",
    "rss_store",
    "rss_pipeline",
    "rss_backoff",
    "rss_scheduler_loop",
    "otx_store",
    "otx_pipeline",
    "otx_backoff",
    "otx_scheduler_loop",
]
