import pytest
import search_api._shared.health as shared_health


@pytest.mark.anyio
async def test_healthz_shape(client):
    r = await client.get("/healthz")
    data = r.json()
    assert r.status_code == 200
    assert data["status"] == "ok"
    for key in ("service", "version", "time", "uptime_s"):
        assert key in data


@pytest.mark.anyio
async def test_readyz_force_ready(client, monkeypatch):
    monkeypatch.setenv("IT_FORCE_READY", "1")
    r = await client.get("/readyz")
    data = r.json()
    assert r.status_code == 200
    assert data["status"] == "ok"
    assert data["checks"] == {}


@pytest.mark.anyio
async def test_readyz_ok_degraded_fail(client, monkeypatch):
    class Resp:
        def __enter__(self):
            return self
        def __exit__(self, *a):
            pass
        def getcode(self):
            return 200

    # ok
    monkeypatch.setenv("OPENSEARCH_URL", "http://os")
    monkeypatch.setattr(shared_health.urlrequest, "urlopen", lambda url, timeout=0.8: Resp())
    r = await client.get("/readyz")
    data = r.json()
    check = data["checks"]["opensearch"]
    assert r.status_code == 200
    assert data["status"] == "ok"
    assert check["status"] == "ok"
    assert set(check) == {"status", "latency_ms", "error", "reason"}

    # degraded
    monkeypatch.delenv("OPENSEARCH_URL", raising=False)
    r = await client.get("/readyz")
    data = r.json()
    check = data["checks"]["opensearch"]
    assert r.status_code == 200
    assert data["status"] == "degraded"
    assert check["status"] == "skipped"
    assert set(check) == {"status", "latency_ms", "error", "reason"}

    # fail
    monkeypatch.setenv("OPENSEARCH_URL", "http://os")
    def raise_err(url, timeout=0.8):
        raise RuntimeError("boom")
    monkeypatch.setattr(shared_health.urlrequest, "urlopen", raise_err)
    r = await client.get("/readyz")
    data = r.json()
    check = data["checks"]["opensearch"]
    assert r.status_code == 503
    assert data["status"] == "fail"
    assert check["status"] == "fail"
    assert set(check) == {"status", "latency_ms", "error", "reason"}
