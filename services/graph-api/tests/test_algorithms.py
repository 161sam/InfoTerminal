import pytest
import types
import app.routes.alg as alg

class FakeSession:
    def run(self, *args, **kwargs):
        q = args[0].lower()
        if "coalesce" in q:
            return types.SimpleNamespace(data=lambda: [{"id": 1, "degree": 2}])
        return types.SimpleNamespace(data=lambda: [])
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        pass

class FakeDriver:
    def session(self):
        return FakeSession()

@pytest.mark.anyio
async def test_degree_without_gds(client, monkeypatch):
    monkeypatch.setattr(alg, "driver", FakeDriver())
    monkeypatch.setattr(alg, "USE_GDS", False)
    r = await client.post("/alg/degree", json={})
    assert r.status_code == 200
    data = r.json()
    assert data["items"][0]["degree"] == 2
    assert len(data["items"]) == 1

@pytest.mark.anyio
async def test_other_algorithms_require_gds(client, monkeypatch):
    monkeypatch.setattr(alg, "driver", FakeDriver())
    monkeypatch.setattr(alg, "USE_GDS", False)
    r1 = await client.post("/alg/betweenness", json={})
    r2 = await client.post("/alg/louvain", json={})
    assert r1.status_code == 501
    assert r2.status_code == 501
