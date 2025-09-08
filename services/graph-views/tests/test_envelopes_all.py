from fastapi.testclient import TestClient


def _is_envelope(j):
    return set(j.keys()) == {"ok","data","counts","error"}


def test_cypher_read_envelope(app_client: TestClient):
    r = app_client.post("/graphs/cypher", json={"stmt": "RETURN 1 AS x", "params": {}})
    j = r.json()
    assert r.status_code == 200 and _is_envelope(j) and j["ok"] is True
    assert "records" in j["data"]


def test_shortest_path_envelope(app_client: TestClient):
    r = app_client.get("/graphs/view/shortest-path", params=dict(
        srcLabel="Person", srcKey="id", srcValue="alice",
        dstLabel="Person", dstKey="id", dstValue="bob", maxLen=3
    ))
    j = r.json()
    assert r.status_code == 200 and _is_envelope(j) and j["ok"] is True
    assert "nodes" in j["data"] and "relationships" in j["data"]


def test_load_csv_writes_disabled(app_client: TestClient, monkeypatch):
    monkeypatch.setenv("GV_ALLOW_WRITES","0")
    r = app_client.post("/graphs/load/csv?write=1", json={"rows":[]})
    j = r.json()
    assert r.status_code in (200,403)
    assert _is_envelope(j) and j["ok"] is False
    assert j["error"]["code"] in ("writes_disabled","unauthorized")


def test_cypher_write_unauthorized(app_client: TestClient):
    r = app_client.post("/graphs/cypher?write=1", json={"stmt":"RETURN 1","params":{}})
    j = r.json()
    assert r.status_code in (401,403)
    assert _is_envelope(j) and j["ok"] is False
