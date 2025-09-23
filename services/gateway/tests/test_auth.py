import importlib
import sys
from pathlib import Path

import pytest
from fastapi import Request

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

pytest.importorskip("httpx")
from httpx import AsyncClient, ASGITransport


@pytest.mark.asyncio
async def test_health_and_protected(monkeypatch, rsa_keys, valid_token, expired_token):
    priv, jwks = rsa_keys
    monkeypatch.setenv("IT_AUTH_REQUIRED", "1")
    monkeypatch.setenv("IT_OIDC_AUDIENCE", "test")
    monkeypatch.setenv("IT_OIDC_ISSUER", "test-issuer")
    monkeypatch.setenv("IT_OIDC_JWKS_URL", "https://example/jwks")

    sys.path.append(str(Path(__file__).resolve().parents[1]))
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from app import auth as auth_module

    auth_module = importlib.reload(auth_module)

    async def fake_fetch():
        return jwks

    monkeypatch.setattr(auth_module, "_fetch_jwks", fake_fetch)

    import prometheus_client.registry as registry

    registry.REGISTRY = registry.CollectorRegistry()
    from app import app as app_module

    app_module = importlib.reload(app_module)
    app = app_module.app

    @app.get("/protected")
    async def protected(request: Request):
        return {"user": request.state.user_id}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/healthz")
        assert r.status_code == 200

        r = await ac.get("/protected")
        assert r.status_code == 401

        r = await ac.get("/protected", headers={"Authorization": "Bearer invalid"})
        assert r.status_code == 401

        r = await ac.get(
            "/protected", headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert r.status_code == 200
        assert r.headers["X-User-Id"] == "user"

        r = await ac.get(
            "/protected", headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert r.status_code == 401
