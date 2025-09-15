import os
import importlib.util
from pathlib import Path
from fastapi.testclient import TestClient

service_path = Path(__file__).resolve().parents[1] / "services" / "nlp-service" / "app.py"
spec = importlib.util.spec_from_file_location("nlp_service_app", service_path)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)
os.environ["ALLOW_TEST_MODE"] = "1"
client = TestClient(module.app)

def test_ner_returns_entity():
    resp = client.post("/ner", json={"text": "Barack Obama was born in Hawaii."})
    data = resp.json()
    assert "entities" in data
    assert len(data["entities"]) >= 1

def test_summarize_returns_string():
    resp = client.post("/summarize", json={"text": "This is a test text for summarization."})
    data = resp.json()
    assert isinstance(data.get("summary"), str)
    assert data["summary"]
