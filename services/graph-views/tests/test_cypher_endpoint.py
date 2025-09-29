import app as app_module

from .conftest import basic_auth_header


def test_read_cypher(app_client, mock_driver):
    r = app_client.post(
        "/graphs/cypher", json={"query": "MATCH (n) RETURN n", "params": {}}
    )
    j = r.json()
    assert r.status_code == 200 and j["ok"] is True
    data = j["data"]["records"]
    assert isinstance(data, list) and data[0]["n"]["__type"] == "node"


def test_write_requires_auth(app_client, monkeypatch):
    monkeypatch.setattr(app_module, "GV_ALLOW_WRITES", True)
    monkeypatch.setenv("GV_BASIC_USER", "u")
    monkeypatch.setenv("GV_BASIC_PASS", "p")
    r = app_client.post(
        "/graphs/cypher?write=1", json={"query": "CREATE (n)", "params": {}}
    )
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "unauthorized"


def test_write_cypher_ok(app_client, mock_driver, monkeypatch):
    monkeypatch.setattr(app_module, "GV_ALLOW_WRITES", True)
    monkeypatch.setenv("GV_BASIC_USER", "u")
    monkeypatch.setenv("GV_BASIC_PASS", "p")
    r = app_client.post(
        "/graphs/cypher?write=1",
        json={"query": "CREATE (:X) RETURN 1", "params": {"x": 1}},
        headers=basic_auth_header("u", "p"),
    )
    assert r.status_code == 200
    assert r.json()["ok"] is True
    stmt, params = mock_driver.runs[-1]
    assert "create" in stmt.lower()
    assert params == {"x": 1}
