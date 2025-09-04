import importlib
import os
from fastapi.testclient import TestClient
from prometheus_client import REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR


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
    import app.main as main

    importlib.reload(main)
    return main.app


def test_metrics_disabled():
    app = _load_app(False)
    client = TestClient(app)
    assert client.get("/metrics").status_code == 404


def test_metrics_enabled():
    app = _load_app(True)
    client = TestClient(app)
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "process_start_time_seconds" in r.text
