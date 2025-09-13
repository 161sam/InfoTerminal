import os
import sys
from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport
from prometheus_client import REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR

os.environ.setdefault("OTEL_SDK_DISABLED", "true")
os.environ.setdefault("IT_JSON_LOGS", "1")
os.environ.setdefault("IT_ENV", "test")
os.environ.setdefault("IT_LOG_SAMPLING", "")

# make service root importable so we can import the app package
SERVICE_ROOT = Path(__file__).resolve().parents[1]
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

import app as app_module  # type: ignore
sys.modules.setdefault("app", app_module)
app = app_module.app

for collector in list(REGISTRY._collector_to_names):
    try:
        REGISTRY.unregister(collector)
    except Exception:
        pass
REGISTRY.register(PROCESS_COLLECTOR)
REGISTRY.register(PLATFORM_COLLECTOR)

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
