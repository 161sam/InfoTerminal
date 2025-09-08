import base64
from fastapi.testclient import TestClient

import app as app_module
from app import app


def test_writes_disabled(monkeypatch):
    app_module.GV_ALLOW_WRITES = False
    client = TestClient(app)
    r = client.post("/graphs/load/csv?write=1", json={"rows": []})
    assert r.status_code == 200
    assert r.json().get("ok") is False


def test_requires_auth(monkeypatch):
    app_module.GV_ALLOW_WRITES = True
    monkeypatch.setenv("GV_BASIC_USER", "u")
    monkeypatch.setenv("GV_BASIC_PASS", "p")
    client = TestClient(app)
    r = client.post("/graphs/load/csv?write=1", json={"rows": []})
    assert r.status_code == 401


def test_basic_auth_ok(monkeypatch):
    app_module.GV_ALLOW_WRITES = True
    monkeypatch.setenv("GV_BASIC_USER", "u")
    monkeypatch.setenv("GV_BASIC_PASS", "p")
    client = TestClient(app)
    token = base64.b64encode(b"u:p").decode()
    r = client.post(
        "/graphs/load/csv?write=1",
        json={"rows": []},
        headers={"Authorization": f"Basic {token}"},
    )
    assert r.status_code == 200
    assert r.json().get("ok") is True
