import types
import pytest
import search_api.auth as auth


def test_get_jwks_caches(monkeypatch):
    auth._jwks_cache.clear()
    calls = []

    class DummyResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return {"keys": ["k"]}
    class DummyClient:
        def __init__(self, timeout):
            pass
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass
        def get(self, url):
            calls.append(url)
            return DummyResponse()
    monkeypatch.setattr(auth.httpx, "Client", DummyClient)
    data1 = auth._get_jwks()
    data2 = auth._get_jwks()
    assert calls == [auth.JWKS_URL]
    assert data1 == data2 == {"keys": ["k"]}


def test_verify_token_valid(monkeypatch):
    monkeypatch.setattr(auth, "_get_jwks", lambda: {"keys": []})
    monkeypatch.setattr(
        auth.jwt,
        "decode",
        lambda token, jwks, algorithms, audience, issuer, options: {
            "sub": "123",
            "preferred_username": "u",
            "roles": ["r"],
        },
    )
    claims = auth.verify_token("tok")
    assert claims["sub"] == "123"
    user = auth.user_from_token("tok")
    assert user == {"sub": "123", "preferred_username": "u", "roles": ["r"]}


def test_verify_token_invalid(monkeypatch):
    monkeypatch.setattr(auth, "_get_jwks", lambda: {"keys": []})
    def bad_decode(*args, **kwargs):
        raise Exception("bad")
    monkeypatch.setattr(auth.jwt, "decode", bad_decode)
    with pytest.raises(ValueError):
        auth.verify_token("tok")
