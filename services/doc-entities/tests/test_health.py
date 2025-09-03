import os, sys
from pathlib import Path
# SQLite in-memory statt PG, damit Import/Metadata.create_all() nicht fehlschlägt
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("OTEL_SDK_DISABLED", "1")
sys.path.append(Path(__file__).resolve().parents[1].as_posix())
from fastapi.testclient import TestClient
from app import app


def test_healthz_ok():
  with TestClient(app) as c:
    r = c.get("/healthz")
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, dict)
