import os
import sys
import importlib.util
from pathlib import Path
from fastapi.testclient import TestClient

service_path = Path(__file__).resolve().parents[1] / "services" / "doc-entities" / "app.py"
service_dir = service_path.parent
sys.path.insert(0, str(service_dir))
spec = importlib.util.spec_from_file_location("doc_entities_app", service_path)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
os.environ["ALLOW_TEST_MODE"] = "1"
spec.loader.exec_module(module)  # type: ignore
sys.path.pop(0)
sys.modules.pop("db", None)
client = TestClient(module.app)

def test_annotate_returns_aleph_id():
    payload = {"text": "Hello world", "meta": {"aleph_id": "A1"}}
    resp = client.post("/annotate", json=payload)
    data = resp.json()
    assert data["aleph_id"] == "A1"
    assert "doc_id" in data
    assert isinstance(data["entities"], list)
    assert data["entities"][0]["resolution"]["status"] == "pending"
    assert "context" in data["entities"][0]
    doc_id = data["doc_id"]
    resp2 = client.get(f"/docs/{doc_id}")
    data2 = resp2.json()
    assert data2["aleph_id"] == "A1"
    assert data2["entities"][0]["resolution"]["status"] == "pending"
    assert "context" in data2["entities"][0]


def test_resolve_placeholder():
    resp = client.post("/resolve/some-doc")
    assert resp.status_code == 501
