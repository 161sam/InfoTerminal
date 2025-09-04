import os, sys
from pathlib import Path
os.environ.setdefault("INIT_DB_ON_STARTUP", "0")  # vermeidet echten PG-Connect
os.environ.setdefault("OTEL_SDK_DISABLED", "1")
sys.path.append(Path(__file__).resolve().parents[1].as_posix())
from fastapi.testclient import TestClient
import app as app_module
from app import app, socket
from contextlib import contextmanager


@contextmanager
def _dummy_conn():
  class DummyCur:
    def execute(self, *a, **k):
      pass
    def __enter__(self): return self
    def __exit__(self, *a): pass
  class DummyConn:
    def cursor(self): return DummyCur()
  yield DummyConn()


def test_healthz_ok(monkeypatch):
  class DummySock:
    def __enter__(self): return self
    def __exit__(self, *a): pass

  monkeypatch.setattr(app_module, "pool", object())
  monkeypatch.setattr(app_module, "conn", lambda: _dummy_conn())
  monkeypatch.setattr(socket, "create_connection", lambda *a, **k: DummySock())
  with TestClient(app) as c:
    r = c.get("/healthz")
    assert r.status_code == 200
    assert r.json().get("ok") is True
