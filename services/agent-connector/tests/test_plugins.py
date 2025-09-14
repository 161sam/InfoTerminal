import os
import sys
import shutil
import importlib.util
import importlib.machinery
from pathlib import Path
from fastapi.testclient import TestClient
import yaml
import pytest

try:
    import jsonschema  # type: ignore
except Exception:  # pragma: no cover
    jsonschema = None


def _client(tmp_plugins):
    service_dir = Path(__file__).resolve().parents[1]
    os.environ["IT_PLUGINS_DIR"] = str(tmp_plugins)
    pkg_name = "agent_connector"
    sys.modules.pop(f"{pkg_name}.app", None)
    sys.modules.pop(f"{pkg_name}.plugins.loader", None)
    pkg = importlib.util.module_from_spec(
        importlib.machinery.ModuleSpec(pkg_name, loader=None)
    )
    pkg.__path__ = [str(service_dir)]
    sys.modules[pkg_name] = pkg
    spec = importlib.util.spec_from_file_location(
        f"{pkg_name}.app", service_dir / "app.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)  # type: ignore
    loader = sys.modules[f"{pkg_name}.plugins.loader"]
    loader._cache = {"ts": 0.0, "items": []}
    return TestClient(module.app)


def test_tools_lists_manifests(tmp_path):
    src = Path(__file__).resolve().parents[3] / "plugins"
    shutil.copytree(src, tmp_path, dirs_exist_ok=True)
    client = _client(tmp_path)
    resp = client.get("/plugins/tools")
    data = resp.json()
    names = {t["plugin"] for t in data["tools"]}
    assert {"flowise", "openbb"} <= names


def test_api_version_mismatch(tmp_path):
    bad_dir = tmp_path / "bad"
    bad_dir.mkdir()
    (bad_dir / "plugin.yaml").write_text(
        yaml.dump(
            {
                "apiVersion": "v0",
                "name": "bad",
                "version": "0.0.1",
                "capabilities": {"tools": []},
            }
        )
    )
    client = _client(tmp_path)
    resp = client.get("/plugins/tools")
    assert resp.status_code == 422


@pytest.mark.skipif(jsonschema is None, reason="jsonschema not installed")
def test_args_schema_validation(tmp_path):
    plug = tmp_path / "openbb"
    plug.mkdir()
    manifest = {
        "apiVersion": "v1",
        "name": "openbb",
        "version": "0.1.0",
        "capabilities": {
            "tools": [
                {
                    "name": "finance.company_profile",
                    "argsSchema": {
                        "type": "object",
                        "properties": {"ticker": {"type": "string"}},
                        "required": ["ticker"],
                    },
                }
            ]
        },
        "endpoints": {"baseUrl": "http://localhost"},
    }
    (plug / "plugin.yaml").write_text(yaml.dump(manifest))
    client = _client(tmp_path)
    resp = client.post("/plugins/invoke/openbb/finance.company_profile", json={})
    assert resp.status_code == 400
