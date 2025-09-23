import os
import sys
from pathlib import Path
import importlib.util

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

pytest.importorskip("httpx")
from httpx import AsyncClient, ASGITransport
from prometheus_client import REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR

os.environ.setdefault("OTEL_SDK_DISABLED", "true")
os.environ.setdefault("IT_JSON_LOGS", "1")
os.environ.setdefault("IT_ENV", "test")
os.environ.setdefault("IT_LOG_SAMPLING", "")

# make service root importable so we can import the app package
SERVICE_ROOT = Path(__file__).resolve().parents[1]
for path in list(sys.path):
    if path.endswith("services/graph-views"):
        sys.path.remove(path)
if str(SERVICE_ROOT) in sys.path:
    sys.path.remove(str(SERVICE_ROOT))
sys.path.insert(0, str(SERVICE_ROOT))

APP_DIR = SERVICE_ROOT / "app"
for alias in ("app", "graph_api_app"):
    sys.modules.pop(alias, None)
sys.modules.pop("metrics", None)
spec = importlib.util.spec_from_file_location(
    "graph_api_app",
    APP_DIR / "__init__.py",
    submodule_search_locations=[str(APP_DIR)],
)
if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load graph-api app module for tests")
app_module = importlib.util.module_from_spec(spec)
sys.modules["graph_api_app"] = app_module
spec.loader.exec_module(app_module)
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
