import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

pytest.importorskip("httpx")
from httpx import ASGITransport, AsyncClient

os.environ.setdefault("OTEL_SDK_DISABLED", "true")
os.environ.setdefault("IT_JSON_LOGS", "1")
os.environ.setdefault("IT_ENV", "test")
os.environ.setdefault("IT_LOG_SAMPLING", "")

service_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(service_dir))
import app.main as app_main  # type: ignore  # noqa: E402

app = app_main.app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
