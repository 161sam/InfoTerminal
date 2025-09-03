import os, pathlib, pytest, importlib.util
from httpx import AsyncClient, ASGITransport

os.environ.setdefault("OTEL_SDK_DISABLED", "true")
MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "app.py"
spec = importlib.util.spec_from_file_location("er_app", MODULE_PATH)
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)
app = app_module.app

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
