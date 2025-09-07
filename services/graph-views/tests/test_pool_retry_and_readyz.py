import asyncio
import time

import db as db_module
from app import app
from fastapi.testclient import TestClient


class DummyConn:
    def __init__(self, value=1, delay: float = 0.0):
        self.value = value
        self.delay = delay

    async def fetchval(self, q):
        if self.delay:
            await asyncio.sleep(self.delay)
        if isinstance(self.value, Exception):
            raise self.value
        return self.value


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

    async def close(self):  # pragma: no cover
        pass


def test_delayed_start(monkeypatch):
    attempts = {"n": 0}

    async def fake_create_pool(*a, **k):
        attempts["n"] += 1
        if attempts["n"] <= 2:
            raise ConnectionRefusedError("no")
        return FakePool(DummyConn())

    monkeypatch.setattr(db_module.asyncpg, "create_pool", fake_create_pool)
    monkeypatch.setattr(db_module.random, "randint", lambda a, b: 0)
    monkeypatch.setenv("GV_PG_INIT_BACKOFF_BASE_MS", "10")
    monkeypatch.setenv("GV_PG_INIT_BACKOFF_MAX_MS", "20")

    with TestClient(app) as c:
        r1 = c.get("/readyz")
        assert r1.status_code == 503
        time.sleep(0.1)
        r2 = c.get("/readyz")
        assert r2.status_code == 200
        assert r2.json()["checks"]["postgres"]["status"] == "ok"


def test_pool_unavailable(monkeypatch):
    async def always_fail(*a, **k):
        raise ConnectionRefusedError("no")

    monkeypatch.setattr(db_module.asyncpg, "create_pool", always_fail)
    monkeypatch.setattr(db_module.random, "randint", lambda a, b: 0)
    monkeypatch.setenv("GV_PG_INIT_BACKOFF_BASE_MS", "10")
    monkeypatch.setenv("GV_PG_INIT_BACKOFF_MAX_MS", "20")
    monkeypatch.setenv("GV_PG_INIT_MAX_RETRIES", "2")

    with TestClient(app) as c:
        time.sleep(0.1)
        r = c.get("/readyz")
        assert r.status_code == 503
        assert r.json()["checks"]["postgres"]["error"] == "pool_unavailable"


def test_query_timeout(monkeypatch):
    async def fake_create_pool(*a, **k):
        return FakePool(DummyConn(delay=0.2))

    monkeypatch.setattr(db_module.asyncpg, "create_pool", fake_create_pool)
    monkeypatch.setenv("GV_PG_QUERY_TIMEOUT_S", "0.05")

    with TestClient(app) as c:
        time.sleep(0.05)
        r = c.get("/readyz")
        assert r.status_code == 503
        assert r.json()["checks"]["postgres"]["error"] == "timeout"
