import importlib.util
import os
import pathlib
from fastapi.testclient import TestClient
from prometheus_client import PLATFORM_COLLECTOR, PROCESS_COLLECTOR, REGISTRY

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "app.py"


def _load_app(enable: bool):
    for collector in list(REGISTRY._collector_to_names):
        try:
            REGISTRY.unregister(collector)
        except Exception:
            pass
    REGISTRY.register(PROCESS_COLLECTOR)
    REGISTRY.register(PLATFORM_COLLECTOR)
    if enable:
        os.environ["IT_ENABLE_METRICS"] = "1"
    else:
        os.environ.pop("IT_ENABLE_METRICS", None)
        os.environ.pop("IT_OBSERVABILITY", None)
    spec = importlib.util.spec_from_file_location("graph_api", MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod.app


def test_metrics_disabled():
    app = _load_app(False)
    client = TestClient(app)
    assert client.get("/metrics").status_code == 404


def test_metrics_enabled():
    app = _load_app(True)
    client = TestClient(app)
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "process_start_time_seconds" in resp.text
