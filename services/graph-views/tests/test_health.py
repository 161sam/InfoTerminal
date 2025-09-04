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
    def __init__(self, fail_execute: bool = False):
        self.fail_execute = fail_execute

    def execute(self, *a, **k):
        if self.fail_execute:
            raise RuntimeError("db error")

    def __enter__(self):
        return self

    def __exit__(self, *a):
        pass


class DummyConn:
    def __init__(self, fail_execute: bool = False):
        self.fail_execute = fail_execute

    def cursor(self):
        return DummyCur(self.fail_execute)


class DummyPool:
    def __init__(self, fail_getconn: bool = False, fail_execute: bool = False):
        self.fail_getconn = fail_getconn
        self.fail_execute = fail_execute

    def getconn(self):
        if self.fail_getconn:
            raise RuntimeError("no conn")
        return DummyConn(self.fail_execute)

    def putconn(self, conn):  # pragma: no cover - trivial
        pass

    def closeall(self):  # pragma: no cover - trivial
        pass


def _patch_pool(monkeypatch, fail_getconn: bool = False, fail_execute: bool = False):
    monkeypatch.setattr(app_module, "setup_pool", lambda: DummyPool(fail_getconn, fail_execute))


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


def test_ready_ok(monkeypatch):
    _patch_pool(monkeypatch)
    monkeypatch.delenv("IT_FORCE_READY", raising=False)
    with TestClient(app) as c:
        r = c.get("/readyz")
        data = r.json()
        assert r.status_code == 200
        assert data["status"] == "ok"
        assert data["checks"]["postgres"]["status"] == "ok"


def test_ready_fail(monkeypatch):
    _patch_pool(monkeypatch, fail_execute=True)
    with TestClient(app) as c:
        r = c.get("/readyz")
        data = r.json()
        assert r.status_code == 503
        assert data["status"] == "fail"
        assert data["checks"]["postgres"]["status"] == "fail"


def test_ready_fail_conn(monkeypatch):
    _patch_pool(monkeypatch, fail_getconn=True)
    with TestClient(app) as c:
        r = c.get("/readyz")
        data = r.json()
        assert r.status_code == 503
        assert data["status"] == "fail"
        assert data["checks"]["postgres"]["status"] == "fail"
