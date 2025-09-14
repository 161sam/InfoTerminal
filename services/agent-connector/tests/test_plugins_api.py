import os, sys, shutil, json, importlib.util, importlib.machinery
from pathlib import Path
from fastapi.testclient import TestClient
import httpx
import pytest


import os, sys, shutil, json, importlib.util, importlib.machinery
from pathlib import Path
from fastapi.testclient import TestClient
import httpx
import pytest


def _client(tmp_plugins: Path, tmp_state: Path) -> TestClient:
    service_dir = Path(__file__).resolve().parents[1]
    os.environ["IT_PLUGINS_DIR"] = str(tmp_plugins)
    os.environ["IT_PLUGINS_STATE_DIR"] = str(tmp_state)
    pkg_name = "agent_connector"
    for mod in [
        f"{pkg_name}.app",
        f"{pkg_name}.plugins.loader",
        f"{pkg_name}.plugins.api",
        f"{pkg_name}.plugins.state",
        f"{pkg_name}.auth",
    ]:
        sys.modules.pop(mod, None)
    pkg = importlib.util.module_from_spec(importlib.machinery.ModuleSpec(pkg_name, loader=None))
    pkg.__path__ = [str(service_dir)]
    sys.modules[pkg_name] = pkg
    spec = importlib.util.spec_from_file_location(f"{pkg_name}.app", service_dir / "app.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)  # type: ignore
    loader = sys.modules[f"{pkg_name}.plugins.loader"]
    loader._cache = {"ts": 0.0, "items": []}
    api = sys.modules[f"{pkg_name}.plugins.api"]
    api._CACHE = {"ts": 0, "registry": []}
    return TestClient(module.app)


def _setup(tmp_path: Path):
    src = Path(__file__).resolve().parents[3] / "plugins" / "openbb"
    shutil.copytree(src, tmp_path / "openbb")


def test_registry_returns_items(tmp_path):
    _setup(tmp_path)
    client = _client(tmp_path, tmp_path / "state")
    resp = client.get("/plugins/registry", headers={"Authorization": "Bearer alice"})
    assert resp.status_code == 200
    data = resp.json()
    assert any(p["name"] == "openbb" for p in data["items"])


def test_state_merge_user_overrides(tmp_path):
    _setup(tmp_path)
    state_dir = tmp_path / "state"
    (state_dir / "users").mkdir(parents=True, exist_ok=True)
    (state_dir / "global.json").write_text(json.dumps({"openbb": {"enabled": False}}))
    (state_dir / "users" / "alice.json").write_text(json.dumps({"openbb": {"enabled": True}}))
    client = _client(tmp_path, state_dir)
    resp = client.get("/plugins/state", headers={"Authorization": "Bearer alice"})
    item = next(p for p in resp.json()["items"] if p["name"] == "openbb")
    assert item["enabled"] is True


def test_enable_rbac(tmp_path):
    _setup(tmp_path)
    client = _client(tmp_path, tmp_path / "state")
    # user scope
    r = client.post("/plugins/openbb/enable", json={"enabled": False}, headers={"Authorization": "Bearer alice"})
    assert r.status_code == 200
    # global without admin
    r = client.post("/plugins/openbb/enable", json={"enabled": True, "scope": "global"}, headers={"Authorization": "Bearer alice"})
    assert r.status_code == 403
    # global with admin
    r = client.post("/plugins/openbb/enable", json={"enabled": True, "scope": "global"}, headers={"Authorization": "Bearer admin"})
    assert r.status_code == 200


def test_config_rejects_secrets(tmp_path):
    _setup(tmp_path)
    client = _client(tmp_path, tmp_path / "state")
    r = client.post("/plugins/openbb/config", json={"config": {"token": "x"}}, headers={"Authorization": "Bearer alice"})
    assert r.status_code == 400


def test_health_up_down(tmp_path, monkeypatch):
    _setup(tmp_path)
    client = _client(tmp_path, tmp_path / "state")

    async def fake_ok(self, url, headers=None):
        return httpx.Response(200, request=httpx.Request("GET", url))

    async def fake_fail(self, url, headers=None):
        raise httpx.ConnectError("boom", request=httpx.Request("GET", url))

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_ok)
    r = client.get("/plugins/openbb/health", headers={"Authorization": "Bearer alice", "X-Request-Id": "1"})
    assert r.json()["status"] == "up"

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_fail)
    r = client.get("/plugins/openbb/health", headers={"Authorization": "Bearer alice", "X-Request-Id": "1"})
    assert r.json()["status"] == "down"
