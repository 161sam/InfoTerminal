from starlette.testclient import TestClient
import importlib.util, pathlib

try:
    from app import app
except Exception:
    module_path = pathlib.Path(__file__).resolve().parents[1] / "app.py"
    spec = importlib.util.spec_from_file_location("er_app", module_path)
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    app = app_module.app  # type: ignore

def test_healthz_ok():
    with TestClient(app) as c:
        r = c.get("/healthz")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}
