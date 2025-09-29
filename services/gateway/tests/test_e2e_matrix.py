import importlib
import sys
import types
from pathlib import Path

import prometheus_client.registry as registry
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[3]
SERVICE_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = Path(__file__).resolve().parents[2]

for path in (REPO_ROOT, SERVICE_ROOT, PACKAGE_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


def _load_app(monkeypatch):
    registry.REGISTRY = registry.CollectorRegistry()
    for name in ("app", "app.app", "services.gateway.app.app"):
        sys.modules.pop(name, None)

    dummy_boot = types.ModuleType("_shared.obs.otel_boot")
    dummy_boot.setup_otel = lambda *_a, **_k: None  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "_shared.obs.otel_boot", dummy_boot)

    from app import app as app_module

    return importlib.reload(app_module)


def test_e2e_matrix_endpoints(monkeypatch):
    app_module = _load_app(monkeypatch)
    client = TestClient(app_module.app)

    listing = client.get("/healthz/e2e")
    assert listing.status_code == 200
    flows = listing.json()["flows"]
    assert any(flow["id"] == "search-graph-dossier" for flow in flows)

    detail = client.get("/healthz/e2e/search-graph-dossier")
    assert detail.status_code == 200
    payload = detail.json()
    assert payload["id"] == "search-graph-dossier"
    assert payload["status"] == "ok"
    assert payload["tests"].endswith("test_search_graph_dossier.py")

    missing = client.get("/healthz/e2e/unknown-flow")
    assert missing.status_code == 404
