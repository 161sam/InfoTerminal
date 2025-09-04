import pytest


@pytest.mark.anyio
async def test_health(client):
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
    assert "checks" in data
