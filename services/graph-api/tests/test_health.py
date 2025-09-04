import pytest
import app as app_module
import _shared.health as shared_health


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
    # ok
    monkeypatch.setenv("NEO4J_URI", "bolt://")
    monkeypatch.setenv("NEO4J_USER", "u")
    monkeypatch.setenv("NEO4J_PASS", "p")
    app_module.app.state.driver = object()
    monkeypatch.setattr(app_module, "probe_db", lambda fn, timeout_s=0.8: {"status": "ok", "latency_ms": 1.0, "error": None, "reason": None})
    r = await client.get("/readyz")
    data = r.json()
    check = data["checks"]["neo4j"]
    assert r.status_code == 200
    assert data["status"] == "ok"
    assert check["status"] == "ok"
    assert set(check) == {"status", "latency_ms", "error", "reason"}

    # degraded
    monkeypatch.delenv("NEO4J_URI", raising=False)
    monkeypatch.delenv("NEO4J_USER", raising=False)
    monkeypatch.delenv("NEO4J_PASS", raising=False)
    app_module.app.state.driver = None
    r = await client.get("/readyz")
    data = r.json()
    check = data["checks"]["neo4j"]
    assert r.status_code == 200
    assert data["status"] == "degraded"
    assert check["status"] == "skipped"
    assert set(check) == {"status", "latency_ms", "error", "reason"}

    # fail
    monkeypatch.setenv("NEO4J_URI", "bolt://")
    monkeypatch.setenv("NEO4J_USER", "u")
    monkeypatch.setenv("NEO4J_PASS", "p")
    app_module.app.state.driver = object()
    monkeypatch.setattr(app_module, "probe_db", lambda fn, timeout_s=0.8: {"status": "fail", "latency_ms": None, "error": "boom", "reason": None})
    r = await client.get("/readyz")
    data = r.json()
    check = data["checks"]["neo4j"]
    assert r.status_code == 503
    assert data["status"] == "fail"
    assert check["status"] == "fail"
    assert set(check) == {"status", "latency_ms", "error", "reason"}
