import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient

MODULE_PATH = Path(__file__).resolve().parents[1] / "app" / "main.py"
spec = importlib.util.spec_from_file_location("collab_app", MODULE_PATH)
collab_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collab_main)
app = collab_main.app


client = TestClient(app)


def test_dossier_export_markdown(tmp_path):
    payload = {
        "case_id": "demo-case",
        "source": "graph",
        "format": "markdown",
        "template": "standard",
        "analysts": ["Analyst Demo"],
        "notes": ["Sample note"],
    }

    response = client.post("/dossier/export", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == "demo-case"
    assert data["format"] == "markdown"
    assert "markdown" in data


def test_dossier_export_pdf(tmp_path):
    payload = {
        "case_id": "demo-case",
        "source": "search",
        "format": "pdf",
        "template": "brief",
    }

    response = client.post("/dossier/export", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")


def test_dossier_templates_catalog():
    response = client.get("/dossier/templates")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    templates = {tpl["id"] for tpl in data["items"]}
    assert {"standard", "brief"}.issubset(templates)
    sample = next(tpl for tpl in data["items"] if tpl["id"] == "standard")
    assert sample["settings"]["includeSummary"] is True


def test_notes_feature_flag(monkeypatch):
    note_payload = {
        "case_id": "case-1",
        "author": "tester",
        "body": "Initial note",
    }

    # Disabled by default
    resp = client.post("/collab/notes", json=note_payload)
    assert resp.status_code == 503

    monkeypatch.setenv("IT_ENABLE_COLLAB_NOTES", "1")
    created = client.post("/collab/notes", json=note_payload)
    assert created.status_code == 200
    note_id = created.json()["id"]
    assert note_id

    listed = client.get("/collab/notes/case-1")
    assert listed.status_code == 200
    assert any(item["id"] == note_id for item in listed.json()["items"])

    monkeypatch.delenv("IT_ENABLE_COLLAB_NOTES", raising=False)
