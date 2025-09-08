from fastapi.testclient import TestClient
from response import ok


def test_ego_envelope(app_client: TestClient):
    r = app_client.get("/graphs/view/ego", params=dict(label="Person", key="id", value="alice", depth=1, limit=10))
    j = r.json()
    assert r.status_code == 200
    assert set(j.keys()) == {"ok", "data", "counts", "error"}
    assert j["ok"] is True
    assert "nodes" in j["data"] and "relationships" in j["data"]
    assert "nodes" in j["counts"] and "relationships" in j["counts"]


def test_cypher_read_envelope(app_client: TestClient):
    r = app_client.post("/graphs/cypher", json={"query": "RETURN 1 AS x", "params": {}})
    j = r.json()
    assert r.status_code == 200 and j["ok"] is True and j["error"] is None


def test_write_disabled_returns_error(app_client: TestClient, monkeypatch):
    monkeypatch.setenv("GV_ALLOW_WRITES", "0")
    r = app_client.post("/graphs/load/csv?write=1", json={"rows": []})
    j = r.json()
    assert r.status_code in (200, 403)
    assert j["ok"] is False
    assert j["error"]["code"] in ("writes_disabled", "unauthorized", "bad_request")


def test_ego_returns_json_ct(app_client: TestClient):
    r = app_client.get("/graphs/view/ego", params=dict(label="Person", key="id", value="alice", depth=1, limit=5))
    assert r.headers.get("content-type","" ).startswith("application/json")
