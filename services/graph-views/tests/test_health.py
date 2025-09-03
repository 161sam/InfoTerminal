import os, sys
from pathlib import Path
os.environ.setdefault("INIT_DB_ON_STARTUP", "0")  # vermeidet echten PG-Connect
os.environ.setdefault("OTEL_SDK_DISABLED", "1")
sys.path.append(Path(__file__).resolve().parents[1].as_posix())
from fastapi.testclient import TestClient
from app import app


def test_healthz_ok():
  with TestClient(app) as c:
    r = c.get("/healthz")
    assert r.status_code == 200
    assert r.json().get("status") in ("ok", "OK", "healthy", None)  # tolerant
