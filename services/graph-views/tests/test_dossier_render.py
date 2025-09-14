from fastapi.testclient import TestClient


def test_dossier_markdown(app_client: TestClient):
    payload = {
        "title": "Sample",
        "items": {"docs": ["d1"], "nodes": ["n1"], "edges": ["e1"]},
        "options": {"summary": False},
    }
    r = app_client.post("/dossier", json=payload)
    assert r.status_code == 200
    j = r.json()
    assert "markdown" in j and "# Sample" in j["markdown"]
