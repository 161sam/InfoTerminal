import pytest
import app

class DummySession:
    def run(self, *args, **kwargs):
        class DummyResult:
            def consume(self):
                return None
        return DummyResult()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        pass

@pytest.mark.anyio
async def test_health(client, monkeypatch):
    class DummyDriver:
        def session(self):
            return DummySession()
    monkeypatch.setattr(app, "driver", DummyDriver())
    r = await client.get("/healthz")
    assert r.status_code == 200
    assert r.json().get("status") in ("ok", "healthy")
