import pytest
from fastapi import HTTPException
import app.main as main
from app import rerank as rr


@pytest.mark.anyio
async def test_startup_exposes(monkeypatch):
    called = {}

    def expose(app, include_in_schema=False, should_gzip=True):
        called["hit"] = True

    monkeypatch.setattr(main.instrumentator, "expose", expose)
    await main._startup()
    assert called.get("hit")


def test_oidc_user_requires_token(monkeypatch):
    monkeypatch.setenv("REQUIRE_AUTH", "1")
    monkeypatch.setattr(main, "settings", main.Settings())
    with pytest.raises(HTTPException):
        main.oidc_user(None)


def test_oidc_user_valid(monkeypatch):
    monkeypatch.setenv("REQUIRE_AUTH", "1")
    monkeypatch.setattr(main, "settings", main.Settings())
    monkeypatch.setattr(main, "user_from_token", lambda tok: {"sub": "x"})
    assert main.oidc_user("Bearer t") == {"sub": "x"}


def test_filters_query(monkeypatch):
    q = main._filters_query(["person"])
    assert q["bool"]["must"][0]["nested"]["query"]["terms"] == {"entities.type": ["person"]}


@pytest.mark.anyio
async def test_search_forbidden(client, monkeypatch):
    monkeypatch.setattr(main, "allow", lambda u, a, r: False)
    r = await client.get("/search", params={"q": "a"})
    assert r.status_code == 403


@pytest.mark.anyio
async def test_search_error(client, monkeypatch):
    monkeypatch.setattr(main, "allow", lambda u, a, r: True)

    def bad_search(index, body):
        raise RuntimeError("boom")

    monkeypatch.setattr(main.client, "search", bad_search)
    r = await client.get("/search", params={"q": "a"})
    assert r.status_code == 500


@pytest.mark.anyio
async def test_rerank_exception(client, monkeypatch):
    monkeypatch.setenv("RERANK_ENABLED", "1")
    monkeypatch.setattr(main, "settings", main.Settings())
    monkeypatch.setattr(rr, "settings", main.Settings())

    def fake_search(index, body):
        return {
            "hits": {
                "hits": [
                    {"_id": "1", "_score": 1.0, "_source": {"title": "a", "snippet": "a"}},
                    {"_id": "2", "_score": 0.9, "_source": {"title": "b", "snippet": "b"}},
                ]
            },
            "aggregations": {},
        }

    def bad_embed(*args, **kwargs):
        raise RuntimeError("bad")

    monkeypatch.setattr(main.client, "search", fake_search)
    monkeypatch.setattr(rr, "get_query_embedding", bad_embed)

    r = await client.get("/search", params={"q": "foo", "rerank": 1})
    assert r.status_code == 200
    assert len(r.json()["results"]) == 2

