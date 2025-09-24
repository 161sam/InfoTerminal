import importlib
import sys
import types

from pathlib import Path

from fastapi.testclient import TestClient
import prometheus_client.registry as registry


REPO_ROOT = Path(__file__).resolve().parents[3]
SERVICE_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = Path(__file__).resolve().parents[2]

for path in (REPO_ROOT, SERVICE_ROOT, PACKAGE_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


def test_traceparent_header_forwarded(monkeypatch):
    monkeypatch.setenv("IT_OPS_ENABLE", "1")
    monkeypatch.delenv("IT_OTEL", raising=False)

    registry.REGISTRY = registry.CollectorRegistry()
    sys.modules.pop("app", None)
    sys.modules.pop("app.app", None)
    sys.modules.pop("services.gateway.app.app", None)

    dummy_boot = types.ModuleType("_shared.obs.otel_boot")

    def _setup_otel(*_args, **_kwargs):  # pragma: no cover - invoked in import
        return None

    dummy_boot.setup_otel = _setup_otel  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "_shared.obs.otel_boot", dummy_boot)

    from app import app as app_module

    app_module = importlib.reload(app_module)

    captured: dict[str, str] = {}

    class DummyResponse:
        def __init__(self):
            self.status_code = 200
            self.content = b"{}"
            self.headers = {"content-type": "application/json"}

    class DummyAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # pragma: no cover - cleanup
            return False

        async def request(self, method, url, headers=None, **kwargs):
            captured.update(headers or {})
            return DummyResponse()

    monkeypatch.setattr(app_module.httpx, "AsyncClient", DummyAsyncClient)

    client = TestClient(app_module.app)
    traceparent = "00-11111111111111111111111111111111-2222222222222222-01"
    response = client.get("/ops/demo", headers={"traceparent": traceparent})

    assert response.status_code == 200
    assert captured.get("traceparent") == traceparent

