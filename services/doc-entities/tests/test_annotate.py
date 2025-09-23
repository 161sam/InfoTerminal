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
        payload = {
            "text": "Alice meets Bob",
            "language": "en",
            "extract_entities": True,
            "extract_relations": False,
            "generate_summary": True,
        }
        r = c.post("/v1/documents/annotate", json=payload)
        assert r.status_code == 200
        body = r.json()
        ent = body["entities"][0]
        assert "context" in ent and "Alice" in ent["context"]
        assert "<span" in body["html_content"]
        assert body["summary"]
        doc_id = body["doc_id"]
        r2 = c.get(f"/v1/documents/{doc_id}")
        assert r2.status_code == 200
        ent2 = r2.json()["entities"][0]
        assert ent2["context"] == ent["context"]
