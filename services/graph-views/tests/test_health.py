import pytest
import app as app_module
import _shared.health as shared_health
from fastapi.testclient import TestClient


class DummyPool:
    def closeall(self):
        pass


def _make_client(monkeypatch, pool=DummyPool()):
    monkeypatch.setenv("INIT_DB_ON_STARTUP", "0")
    monkeypatch.setattr(app_module, "setup_pool", lambda: pool)
    return TestClient(app_module.app)


def test_healthz_shape(monkeypatch):
    with _make_client(monkeypatch) as c:
        r = c.get("/healthz")
        data = r.json()
        assert r.status_code == 200
        assert data["status"] == "ok"
        for key in ("service", "version", "time", "uptime_s"):
            assert key in data


def test_readyz_force_ready(monkeypatch):
    with _make_client(monkeypatch) as c:
        monkeypatch.setenv("IT_FORCE_READY", "1")
        r = c.get("/readyz")
        data = r.json()
        assert r.status_code == 200
        assert data["status"] == "ok"
        assert data["checks"] == {}


def test_readyz_ok_degraded_fail(monkeypatch):
    # ok
    monkeypatch.setattr(app_module, "probe_db", lambda fn, timeout_s=0.8: {"status": "ok", "latency_ms": 1.0, "error": None, "reason": None})
    with _make_client(monkeypatch) as c:
        r = c.get("/readyz")
        data = r.json()
        check = data["checks"]["postgres"]
        assert r.status_code == 200
        assert data["status"] == "ok"
        assert check["status"] == "ok"
        assert set(check) == {"status", "latency_ms", "error", "reason"}

    # degraded
    with _make_client(monkeypatch, pool=None) as c:
        r = c.get("/readyz")
        data = r.json()
        check = data["checks"]["postgres"]
        assert r.status_code == 200
        assert data["status"] == "degraded"
        assert check["status"] == "skipped"
        assert set(check) == {"status", "latency_ms", "error", "reason"}

    # fail
    monkeypatch.setattr(app_module, "probe_db", lambda fn, timeout_s=0.8: {"status": "fail", "latency_ms": None, "error": "boom", "reason": None})
    with _make_client(monkeypatch) as c:
        r = c.get("/readyz")
        data = r.json()
        check = data["checks"]["postgres"]
        assert r.status_code == 503
        assert data["status"] == "fail"
        assert check["status"] == "fail"
        assert set(check) == {"status", "latency_ms", "error", "reason"}
