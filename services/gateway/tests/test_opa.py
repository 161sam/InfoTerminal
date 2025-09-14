import importlib
import sys
from pathlib import Path

import pytest
from fastapi import Request
from httpx import AsyncClient, ASGITransport


@pytest.mark.asyncio
async def test_opa_allow_deny(monkeypatch, rsa_keys, valid_token):
    priv, jwks = rsa_keys
    monkeypatch.setenv("IT_AUTH_REQUIRED", "1")
    monkeypatch.setenv("IT_OIDC_AUDIENCE", "test")
    monkeypatch.setenv("IT_OIDC_ISSUER", "test-issuer")
    monkeypatch.setenv("IT_OIDC_JWKS_URL", "https://example/jwks")
    monkeypatch.setenv("OPA_URL", "http://opa")

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

    @app.get("/plugins/invoke/x")
    async def handler(request: Request):
        return {"ok": True}

    async def allow(_):
        return True

    async def deny(_):
        return False

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        monkeypatch.setattr(app_module, "opa_check", allow)
        r = await ac.get(
            "/plugins/invoke/x", headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert r.status_code == 200

        monkeypatch.setattr(app_module, "opa_check", deny)
        r = await ac.get(
            "/plugins/invoke/x", headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert r.status_code == 403
