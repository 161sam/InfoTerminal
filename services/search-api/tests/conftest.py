import os
import sys
import pytest
from httpx import AsyncClient, ASGITransport

os.environ.setdefault("OTEL_SDK_DISABLED", "true")
os.environ.setdefault("IT_JSON_LOGS", "1")
os.environ.setdefault("IT_ENV", "test")
os.environ.setdefault("IT_LOG_SAMPLING", "")

# search-api uses a src layout; root conftest adds src to sys.path.
import search_api.app.main as app_main  # type: ignore
sys.modules.setdefault("app.main", app_main)
app = app_main.app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def test_settings():
    os.environ["ALLOW_TEST_MODE"] = "1"
    os.environ["IT_JSON_LOGS"] = "1"
    os.environ["IT_ENV"] = "test"
    os.environ["IT_LOG_SAMPLING"] = ""
    yield
    for k in ("ALLOW_TEST_MODE", "IT_JSON_LOGS", "IT_ENV", "IT_LOG_SAMPLING", "IT_OTEL"):
        os.environ.pop(k, None)


@pytest.fixture
async def client(test_settings):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
