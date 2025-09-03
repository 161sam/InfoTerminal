import os, pathlib, pytest, sys, importlib
from httpx import AsyncClient, ASGITransport

os.environ.setdefault("OTEL_SDK_DISABLED", "true")
SERVICE_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVICE_DIR))
import app.main as app_main  # type: ignore
sys.modules.setdefault("app.main", app_main)
app = app_main.app

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
