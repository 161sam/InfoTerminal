import importlib
import sys
from pathlib import Path

from httpx import AsyncClient, ASGITransport


async def test_legacy_nlp_redirect(monkeypatch):
    monkeypatch.setenv("IT_DEPRECATION_CUTOFF_DATE", "2999-01-01")
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from app import app as app_module

    app_module = importlib.reload(app_module)
    app = app_module.app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/nlp-service/ner")
        assert r.status_code == 308
        assert r.headers["location"] == "/doc-entities/ner"


async def test_legacy_nlp_gone(monkeypatch):
    monkeypatch.setenv("IT_DEPRECATION_CUTOFF_DATE", "2000-01-01")
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from app import app as app_module

    app_module = importlib.reload(app_module)
    app = app_module.app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/nlp-service/ner")
        assert r.status_code == 410
        assert r.json()["hint"] == "use /doc-entities"
