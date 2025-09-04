import os, sys
from pathlib import Path

os.environ.setdefault("INIT_DB_ON_STARTUP", "0")
os.environ.setdefault("OTEL_SDK_DISABLED", "1")

sys.path.append(Path(__file__).resolve().parents[1].as_posix())
import types
sys.modules.setdefault(
    "opentelemetry.instrumentation.fastapi",
    types.SimpleNamespace(
        FastAPIInstrumentor=type("FastAPIInstrumentor", (), {"instrument_app": lambda self, app: app})
    ),
)
import app as app_module  # noqa: E402
from app import app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


class DummyCur:
    def execute(self, *a, **k):
        pass
    def __enter__(self):
        return self
    def __exit__(self, *a):
        pass


class DummyConn:
    def cursor(self):
        return DummyCur()


class DummyPool:
    def getconn(self):
        return DummyConn()
    def putconn(self, conn):  # pragma: no cover - trivial
        pass
    def closeall(self):  # pragma: no cover - trivial
        pass


def _patch_pool(monkeypatch):
    monkeypatch.setattr(app_module, "setup_pool", lambda: DummyPool())


def test_healthz(monkeypatch):
    _patch_pool(monkeypatch)
    with TestClient(app) as c:
        r = c.get("/healthz")
        data = r.json()
        assert r.status_code == 200
        assert data["status"] == "ok"
        for key in ("service", "version", "time", "uptime_s"):
            assert key in data


def test_ready_force(monkeypatch):
    _patch_pool(monkeypatch)
    monkeypatch.setenv("IT_FORCE_READY", "1")
    with TestClient(app) as c:
        r = c.get("/readyz")
        data = r.json()
        assert r.status_code == 200
        assert data["status"] == "ok"
        assert data["checks"]["postgres"]["status"] == "skipped"


def test_ready_skipped(monkeypatch):
    monkeypatch.setattr(app_module, "setup_pool", lambda: None)
    monkeypatch.delenv("IT_FORCE_READY", raising=False)
    with TestClient(app) as c:
        r = c.get("/readyz")
        data = r.json()
        assert r.status_code == 200
        assert data["status"] == "ok"
        assert data["checks"]["postgres"]["status"] == "skipped"
