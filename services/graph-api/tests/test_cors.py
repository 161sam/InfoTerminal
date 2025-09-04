import pytest


@pytest.mark.anyio
async def test_cors_allowed_origin(client):
    r = await client.get("/healthz", headers={"Origin": "http://localhost:3411"})
    assert r.headers.get("access-control-allow-origin") == "http://localhost:3411"

    r = await client.options(
        "/readyz",
        headers={
            "Origin": "http://localhost:3411",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Authorization,Content-Type",
        },
    )
    assert r.status_code in (200, 204)
    h = r.headers
    assert h.get("access-control-allow-origin") == "http://localhost:3411"
    assert "GET" in h.get("access-control-allow-methods", "")
    assert "Authorization" in h.get("access-control-allow-headers", "")
    assert "Content-Type" in h.get("access-control-allow-headers", "")


@pytest.mark.anyio
async def test_cors_disallowed_origin(client):
    r = await client.get("/healthz", headers={"Origin": "http://evil.local:9999"})
    assert "access-control-allow-origin" not in r.headers
