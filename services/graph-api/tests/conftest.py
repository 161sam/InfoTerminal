import os, pathlib, pytest, importlib.util, sys
from httpx import AsyncClient, ASGITransport
from prometheus_client import REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR

os.environ.setdefault("OTEL_SDK_DISABLED", "true")
MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "app.py"
for collector in list(REGISTRY._collector_to_names):
    try:
        REGISTRY.unregister(collector)
    except Exception:
        pass
REGISTRY.register(PROCESS_COLLECTOR)
REGISTRY.register(PLATFORM_COLLECTOR)
spec = importlib.util.spec_from_file_location("graph_api_app", MODULE_PATH)
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)
sys.modules.setdefault("app", app_module)
app = app_module.app

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
def test_settings():
    os.environ["ALLOW_TEST_MODE"] = "1"
    yield
    os.environ.pop("ALLOW_TEST_MODE", None)

@pytest.fixture
async def client(test_settings):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
