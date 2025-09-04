import sys
from pathlib import Path
import asyncio
sys.path.append(Path(__file__).resolve().parents[1].as_posix())
import db as db_module  # noqa: E402
from app import app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


class DummyConn:
    async def fetchval(self, q):
        await asyncio.sleep(0.01)
        return 1


class FakeAcquire:
    def __init__(self, conn):
        self.conn = conn

    async def __aenter__(self):
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        pass


class FakePool:
    def __init__(self, conn):
        self.conn = conn

    def acquire(self):
        return FakeAcquire(self.conn)

    async def close(self):
        pass


def test_readyz_ok(monkeypatch):
    async def fake_create_pool(*a, **k):
        return FakePool(DummyConn())

    monkeypatch.setattr(db_module.asyncpg, "create_pool", fake_create_pool)

    with TestClient(app) as c:
        r = c.get("/readyz")
        assert r.status_code == 200
        data = r.json()["checks"]["postgres"]
        assert data["status"] == "ok"
        assert data["latency_ms"] is not None and data["latency_ms"] > 0
