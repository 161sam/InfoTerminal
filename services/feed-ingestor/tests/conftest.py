import os
import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.environ.setdefault("FEEDS_ENABLED", "1")
os.environ.setdefault("RSS_ENABLED", "1")
os.environ.setdefault("FEED_OTX_ENABLED", "1")
os.environ.setdefault("RSS_FETCH_INTERVAL", "0")
os.environ.setdefault("RSS_DRY_RUN", "0")
os.environ.setdefault("OTX_FETCH_INTERVAL", "0")
os.environ.setdefault("OTX_DRY_RUN", "0")

service_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(service_dir))

import app.main as app_main  # type: ignore  # noqa: E402
from app.main import (  # type: ignore  # noqa: E402
    otx_backoff,
    otx_store,
    rss_backoff,
    rss_pipeline,
    rss_store,
)

app = app_main.app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
def reset_store():
    rss_store.clear()
    otx_store.clear()
    rss_backoff.reset()
    otx_backoff.reset()
