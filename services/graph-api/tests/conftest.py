import os, pathlib, sys, pytest
from httpx import AsyncClient, ASGITransport

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from app import app

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
