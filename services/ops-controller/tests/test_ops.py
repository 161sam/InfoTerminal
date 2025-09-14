import importlib.util
from pathlib import Path
import sys
import subprocess
import types
from fastapi.testclient import TestClient

def load_app(monkeypatch):
    monkeypatch.setenv("IT_OPS_ENABLE", "1")
    services_dir = Path(__file__).resolve().parents[2]
    sys.path.append(str(services_dir))
    path = services_dir / "ops-controller" / "app.py"
    spec = importlib.util.spec_from_file_location("ops_controller", path)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(module)  # type: ignore
    return module.APP

def test_list_and_status(monkeypatch, tmp_path):
    yaml_path = tmp_path / "stacks.yaml"
    yaml_path.write_text('version:1\nstacks:\n  core:\n    title: Core\n    files: ["docker-compose.yml"]')
    monkeypatch.setenv("IT_OPS_STACKS_FILE", str(yaml_path))

    def mock_run(cmd, stdout, stderr, timeout, env):
        return subprocess.CompletedProcess(cmd, 0, b'{}\n', b'')
    monkeypatch.setattr(subprocess, "run", mock_run)
    app = load_app(monkeypatch)
    client = TestClient(app)
    r = client.get("/ops/stacks", headers={"X-Roles": "ops"})
    assert r.status_code == 200
    r = client.get("/ops/stacks/core/status", headers={"X-Roles": "ops"})
    assert r.status_code == 200

def test_up_down(monkeypatch, tmp_path):
    yaml_path = tmp_path / "stacks.yaml"
    yaml_path.write_text('version:1\nstacks:\n  core:\n    title: Core\n    files: ["docker-compose.yml"]')
    monkeypatch.setenv("IT_OPS_STACKS_FILE", str(yaml_path))
    monkeypatch.setenv("IT_OPS_ENABLE", "1")

    def mock_run(cmd, stdout, stderr, timeout, env):
        return subprocess.CompletedProcess(cmd, 0, b'', b'')
    monkeypatch.setattr(subprocess, "run", mock_run)
    app = load_app(monkeypatch)
    client = TestClient(app)
    for action in ["up", "down", "restart"]:
        r = client.post(f"/ops/stacks/core/{action}", headers={"X-Roles": "ops"})
        assert r.status_code == 200

def test_scale_range(monkeypatch, tmp_path):
    yaml_path = tmp_path / "stacks.yaml"
    yaml_path.write_text('version:1\nstacks:\n  core:\n    title: Core\n    files: ["docker-compose.yml"]')
    monkeypatch.setenv("IT_OPS_STACKS_FILE", str(yaml_path))
    monkeypatch.setenv("IT_OPS_ENABLE", "1")
    app = load_app(monkeypatch)
    client = TestClient(app)
    r = client.post("/ops/stacks/core/scale?service=web&replicas=11", headers={"X-Roles": "ops"})
    assert r.status_code == 400

def test_logs(monkeypatch, tmp_path):
    yaml_path = tmp_path / "stacks.yaml"
    yaml_path.write_text('version:1\nstacks:\n  core:\n    title: Core\n    files: ["docker-compose.yml"]')
    monkeypatch.setenv("IT_OPS_STACKS_FILE", str(yaml_path))
    monkeypatch.setenv("IT_OPS_ENABLE", "1")

    class DummyProc:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass
        def terminate(self):
            pass
        stdout = types.SimpleNamespace(readline=lambda: b'line\n')

    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: DummyProc())
    app = load_app(monkeypatch)
    client = TestClient(app)
    r = client.get("/ops/stacks/core/logs", headers={"X-Roles": "ops"})
    assert r.status_code == 200
