import time
import numpy as np
import pytest

import app.main as app
from app.config import Settings as AppSettings
from app import rerank as rr


@pytest.fixture
def rerank_env(monkeypatch):
    monkeypatch.setenv("RERANK_ENABLED", "1")
    app.settings = AppSettings()
    rr.settings = AppSettings()
    rr.query_cache.clear(); rr.doc_cache.clear()
    yield
    monkeypatch.delenv("RERANK_ENABLED", raising=False)


@pytest.fixture
def rerank_env_timeout(monkeypatch):
    monkeypatch.setenv("RERANK_ENABLED", "1")
    monkeypatch.setenv("RERANK_TIMEOUT_MS", "10")
    app.settings = AppSettings()
    rr.settings = AppSettings()
    rr.query_cache.clear(); rr.doc_cache.clear()
    yield
    monkeypatch.delenv("RERANK_ENABLED", raising=False)
    monkeypatch.delenv("RERANK_TIMEOUT_MS", raising=False)


def test_cosine_rank_basic():
    q = np.array([1.0, 0.0])
    docs = np.array([[1.0, 0.0], [0.0, 1.0]])
    ranks = rr.cosine_rank(q, docs)
    assert ranks[0][0] == 0
    assert ranks[0][1] > ranks[1][1]


def test_cache_ttl(monkeypatch):
    provider = rr.EmbeddingProvider("dummy")
    calls = {"n": 0}

    def fake_embed(self, texts):
        calls["n"] += 1
        return np.array([[float(calls["n"])]] * len(texts))

    monkeypatch.setattr(rr.EmbeddingProvider, "embed", fake_embed, raising=False)
    monkeypatch.setattr(rr, "query_cache", rr.TTLCache(maxsize=10, ttl=1))

    rr.get_query_embedding(provider, "hello")
    rr.get_query_embedding(provider, "hello")
    assert calls["n"] == 1
    time.sleep(1.1)
    rr.get_query_embedding(provider, "hello")
    assert calls["n"] == 2


@pytest.mark.anyio
async def test_rerank_integration(rerank_env, client, monkeypatch):
    def fake_search(index, body):
        return {
            "hits": {
                "hits": [
                    {"_id": "1", "_score": 1.0, "_source": {"title": "doc1", "snippet": "foo"}},
                    {"_id": "2", "_score": 0.9, "_source": {"title": "doc2", "snippet": "alpha"}},
                    {"_id": "3", "_score": 0.8, "_source": {"title": "doc3", "snippet": "bar"}},
                ]
            },
            "aggregations": {},
        }

    monkeypatch.setattr(app.client, "search", fake_search)

    def fake_embed(self, texts):
        mapping = {"alpha": [1.0, 0.0], "foo": [0.0, 1.0], "bar": [0.0, 0.5]}
        return np.asarray([mapping.get(t, [0.0, 0.0]) for t in texts])

    monkeypatch.setattr(rr.EmbeddingProvider, "embed", fake_embed, raising=False)

    r = await client.get("/search", params={"q": "alpha", "rerank": 1})
    assert r.status_code == 200
    items = r.json()["results"]
    assert items[0]["id"] == "2"
    assert items[0]["meta"]["rerank"]["cosine"] >= items[1]["meta"]["rerank"]["cosine"]


@pytest.mark.anyio
async def test_rerank_timeout(rerank_env_timeout, client, monkeypatch):
    def fake_search(index, body):
        return {
            "hits": {
                "hits": [
                    {"_id": "1", "_score": 1.0, "_source": {"title": "doc1", "snippet": "foo"}},
                    {"_id": "2", "_score": 0.9, "_source": {"title": "doc2", "snippet": "alpha"}},
                ]
            },
            "aggregations": {},
        }

    monkeypatch.setattr(app.client, "search", fake_search)

    def slow_embed(self, texts):
        time.sleep(0.05)
        return np.asarray([[0.0, 0.0] for _ in texts])

    monkeypatch.setattr(rr.EmbeddingProvider, "embed", slow_embed, raising=False)

    r = await client.get("/search", params={"q": "alpha", "rerank": 1})
    assert r.status_code == 200
    items = r.json()["results"]
    assert items[0]["id"] == "1"
    assert r.headers.get("X-Reranked") is None
