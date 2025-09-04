import os, sys, types
from pathlib import Path

sys.path.append(Path(__file__).resolve().parents[1].as_posix())
sys.modules.setdefault(
    "opentelemetry.instrumentation.fastapi",
    types.SimpleNamespace(
        FastAPIInstrumentor=type(
            "FastAPIInstrumentor", (), {"instrument_app": lambda self, app: app}
        )
    ),
)
# provide minimal stubs so other tests importing OTEL modules succeed
sys.modules.setdefault(
    "opentelemetry.sdk.trace.sampling",
    types.SimpleNamespace(
        ParentBased=lambda *a, **k: None, TraceIdRatioBased=lambda *a, **k: None
    ),
)
import app as app_module
from app import app
from fastapi.testclient import TestClient


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
    monkeypatch.setenv("INIT_DB_ON_STARTUP", "0")


def test_cors_allowed_origin(monkeypatch):
    _patch_pool(monkeypatch)
    with TestClient(app) as c:
        r = c.get("/healthz", headers={"Origin": "http://localhost:3411"})
        assert r.headers.get("access-control-allow-origin") == "http://localhost:3411"

        r = c.options(
            "/readyz",
            headers={
                "Origin": "http://localhost:3411",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Authorization,Content-Type",
            },
        )
        assert r.status_code in (200, 204)
        h = r.headers
        assert h.get("access-control-allow-origin") == "http://localhost:3411"
        assert "GET" in h.get("access-control-allow-methods", "")
        assert "Authorization" in h.get("access-control-allow-headers", "")
        assert "Content-Type" in h.get("access-control-allow-headers", "")


def test_cors_disallowed_origin(monkeypatch):
    _patch_pool(monkeypatch)
    with TestClient(app) as c:
        r = c.get("/healthz", headers={"Origin": "http://evil.local:9999"})
        assert "access-control-allow-origin" not in r.headers
