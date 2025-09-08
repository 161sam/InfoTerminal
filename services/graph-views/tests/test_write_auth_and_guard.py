import app as app_module
import app as app_module
from .conftest import basic_auth_header


def test_writes_disabled(app_client, monkeypatch):
    monkeypatch.setattr(app_module, "GV_ALLOW_WRITES", False)
    r = app_client.post("/graphs/load/csv?write=1", json={"rows": []})
    assert r.status_code == 200
    assert r.json().get("ok") is False


def test_requires_auth(app_client, monkeypatch):
    monkeypatch.setattr(app_module, "GV_ALLOW_WRITES", True)
    monkeypatch.setenv("GV_BASIC_USER", "u")
    monkeypatch.setenv("GV_BASIC_PASS", "p")
    r = app_client.post("/graphs/load/csv?write=1", json={"rows": []})
    assert r.status_code == 401
    assert "WWW-Authenticate" in r.headers


def test_basic_auth_ok(app_client, mock_driver, monkeypatch):
    monkeypatch.setattr(app_module, "GV_ALLOW_WRITES", True)
    monkeypatch.setenv("GV_BASIC_USER", "u")
    monkeypatch.setenv("GV_BASIC_PASS", "p")
    r = app_client.post(
        "/graphs/load/csv?write=1",
        json={"rows": []},
        headers=basic_auth_header("u", "p"),
    )
    assert r.status_code == 200
    assert r.json().get("ok") is True
    assert mock_driver.runs == []
