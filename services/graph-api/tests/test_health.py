import pytest


@pytest.mark.anyio
async def test_healthz(client):
    r = await client.get("/healthz")
    data = r.json()
    assert r.status_code == 200
    assert data["status"] == "ok"
    for key in ("service", "version", "time", "uptime_s"):
        assert key in data


@pytest.mark.anyio
async def test_ready_force(client, monkeypatch):
    monkeypatch.setenv("IT_FORCE_READY", "1")
    r = await client.get("/readyz")
    data = r.json()
    assert r.status_code == 200
    assert data["status"] == "ok"
    assert data["checks"]["neo4j"]["status"] == "skipped"


@pytest.mark.anyio
async def test_ready_skipped(client, monkeypatch):
    monkeypatch.delenv("IT_FORCE_READY", raising=False)
    r = await client.get("/readyz")
    data = r.json()
    assert r.status_code == 200
    assert data["status"] == "ok"
    assert data["checks"]["neo4j"]["status"] == "skipped"
