import json
import types
import pytest
from starlette.requests import Request
import app.health as health


@pytest.mark.anyio
async def test_health(client):
    r = await client.get("/healthz")
    data = r.json()
    assert r.status_code == 200
    assert data["status"] == "ok"
    for key in ("service", "version", "time", "uptime_s"):
        assert key in data


def _dummy_request():
    app = types.SimpleNamespace(state=types.SimpleNamespace(service_name="s", start_time=0, version="dev"))
    return Request({"type": "http", "app": app})


def _json(resp):
    return json.loads(resp.body)


def test_ready_force(monkeypatch):
    monkeypatch.setenv("IT_FORCE_READY", "1")
    resp = health.readyz(_dummy_request())
    data = _json(resp)
    assert resp.status_code == 200
    assert data["checks"]["opensearch"]["status"] == "skipped"


def test_ready_opensearch_success(monkeypatch):
    monkeypatch.setenv("OPENSEARCH_URL", "http://os")

    class Resp:
        def __init__(self, code):
            self.code = code

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

        def getcode(self):
            return self.code

    monkeypatch.setattr(health.urlrequest, "urlopen", lambda url, timeout=0: Resp(200))
    resp = health.readyz(_dummy_request())
    data = _json(resp)
    assert resp.status_code == 200
    assert data["checks"]["opensearch"]["status"] == "ok"


def test_ready_opensearch_fail(monkeypatch):
    monkeypatch.setenv("OPENSEARCH_URL", "http://os")

    class Resp:
        def __init__(self, code):
            self.code = code

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

        def getcode(self):
            return self.code

    monkeypatch.setattr(health.urlrequest, "urlopen", lambda url, timeout=0: Resp(500))
    resp = health.readyz(_dummy_request())
    data = _json(resp)
    assert resp.status_code == 503
    assert data["checks"]["opensearch"]["status"] == "fail"


def test_ready_opensearch_missing(monkeypatch):
    monkeypatch.delenv("OPENSEARCH_URL", raising=False)
    resp = health.readyz(_dummy_request())
    data = _json(resp)
    assert data["checks"]["opensearch"]["status"] == "skipped"
