import pytest
import app

class DummySession:
    def run(self, *args, **kwargs):
        class DummyResult:
            def __iter__(self):
                return iter([])
        return DummyResult()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        pass

@pytest.mark.anyio
async def test_graph_neighbors(client, monkeypatch):
    class DummyDriver:
        def session(self):
            return DummySession()
    monkeypatch.setattr(app, "driver", DummyDriver())
    r = await client.get("/neighbors", params={"node_id": "demo:node:1"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)
