import pytest
import types
import app.routes.export as export

class FakeNode:
    def __init__(self, id):
        self.id = id
        self.labels = []
        self._props = {}
    def __iter__(self):
        return iter(self._props.items())
    def items(self):
        return self._props.items()

class FakeRel:
    def __init__(self, id, start, end):
        self.id = id
        self.type = "KNOWS"
        self.start_node = start
        self.end_node = end
        self._props = {}
    def __iter__(self):
        return iter(self._props.items())
    def items(self):
        return self._props.items()

class FakeGraph:
    def __init__(self):
        n = FakeNode(1)
        self.nodes = [n]
        self.relationships = [FakeRel(2, n, n)]

class FakeSession:
    def run(self, *args, **kwargs):
        return types.SimpleNamespace(graph=lambda: FakeGraph())
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        pass

class FakeDriver:
    def session(self):
        return FakeSession()

@pytest.mark.anyio
async def test_export_roundtrip(client, monkeypatch):
    monkeypatch.setattr(export, "driver", FakeDriver())
    r = await client.get("/export/json")
    assert r.status_code == 200
    assert r.json()["nodes"][0]["id"] == 1
    r = await client.get("/export/graphml")
    assert r.status_code == 200
    assert "<graphml" in r.text
    assert 'node id="1"' in r.text
