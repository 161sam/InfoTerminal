import os, sys
from pathlib import Path

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("ALLOW_TEST_MODE", "1")
os.environ.setdefault("OTEL_SDK_DISABLED", "1")
sys.path.append(Path(__file__).resolve().parents[1].as_posix())

from fastapi.testclient import TestClient  # noqa
from app import app  # noqa

def test_annotation_includes_context():
    with TestClient(app) as c:
        r = c.post("/annotate", json={"text": "Alice meets Bob", "do_summary": True})
        body = r.json()
        ent = body["entities"][0]
        assert "context" in ent and "Alice" in ent["context"]
        assert "<span" in body["html"]
        assert body["summary"]
        doc_id = body["doc_id"]
        r2 = c.get(f"/docs/{doc_id}")
        ent2 = r2.json()["entities"][0]
        assert ent2["context"] == ent["context"]
