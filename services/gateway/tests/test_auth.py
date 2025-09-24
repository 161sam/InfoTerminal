import importlib
import sys
import time
from pathlib import Path

import pytest
from fastapi import Request
from jose import jwt

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


@pytest.mark.asyncio
async def test_validate_bearer_expiry(monkeypatch, rsa_keys):
    priv, jwks = rsa_keys
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

    valid_token = jwt.encode(
        {
            "sub": "user",
            "aud": "test",
            "iss": "test-issuer",
            "exp": int(time.time()) + 30,
        },
        priv,
        algorithm="RS256",
        headers={"kid": "test"},
    )
    claims = await auth_module.validate_bearer(valid_token)
    assert claims and claims.get("sub") == "user"

    expired_token = jwt.encode(
        {
            "sub": "user",
            "aud": "test",
            "iss": "test-issuer",
            "exp": int(time.time()) - 120,
        },
        priv,
        algorithm="RS256",
        headers={"kid": "test"},
    )
    assert await auth_module.validate_bearer(expired_token) is None


@pytest.mark.asyncio
async def test_fetch_jwks_cache(monkeypatch):
    monkeypatch.setenv("IT_OIDC_JWKS_URL", "https://example/jwks")
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from app import auth as auth_module

    auth_module = importlib.reload(auth_module)

    class DummyResponse:
        def __init__(self):
            self._json = {"keys": [{"kid": "test"}]}

        def json(self):
            return self._json

        def raise_for_status(self):
            return None

    class DummyClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url):
            return DummyResponse()

    monkeypatch.setattr(auth_module.httpx, "AsyncClient", DummyClient)
    auth_module._JWKS_CACHE = {"keys": [], "ts": 0}
    first = await auth_module._fetch_jwks()
    second = await auth_module._fetch_jwks()
    assert first["keys"] == [{"kid": "test"}]
    assert second["keys"] == [{"kid": "test"}]
