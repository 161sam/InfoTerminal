import pytest

@pytest.mark.anyio
async def test_health(client):
    r = await client.get("/healthz")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
