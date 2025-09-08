from fastapi.testclient import TestClient


def test_export_dossier_basic(app_client: TestClient):
    r = app_client.get("/graphs/export/dossier", params=dict(label="Person", key="id", value="alice", depth=2))
    assert r.status_code == 200
    j = r.json()
    assert j["ok"] is True and j["error"] is None
    assert "nodes" in j["data"] and "edges" in j["data"]
