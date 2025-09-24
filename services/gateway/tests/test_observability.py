import importlib
import sys
import types
from pathlib import Path

import pytest
import httpx
from fastapi.testclient import TestClient
from starlette.requests import Request
import prometheus_client.registry as registry
from datetime import datetime, timedelta


REPO_ROOT = Path(__file__).resolve().parents[3]
SERVICE_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = Path(__file__).resolve().parents[2]

for path in (REPO_ROOT, SERVICE_ROOT, PACKAGE_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


def _load_app(monkeypatch):
    registry.REGISTRY = registry.CollectorRegistry()
    sys.modules.pop("app", None)
    sys.modules.pop("app.app", None)
    sys.modules.pop("services.gateway.app.app", None)

    dummy_boot = types.ModuleType("_shared.obs.otel_boot")
    dummy_boot.setup_otel = lambda *_a, **_k: None  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "_shared.obs.otel_boot", dummy_boot)

    from app import app as app_module

    return importlib.reload(app_module)


def test_trace_helpers(monkeypatch):
    app_module = _load_app(monkeypatch)

    class DummySpanContext:
        trace_id = 0x1
        span_id = 0x2

    class DummySpan:
        def get_span_context(self):
            return DummySpanContext()

    class DummyTrace:
        def get_current_span(self):  # pragma: no cover - simple return
            return DummySpan()

    monkeypatch.setitem(sys.modules, "opentelemetry.trace", DummyTrace())

    trace_id, span_id = app_module._current_trace_ids()
    assert trace_id == "00000000000000000000000000000001"
    assert span_id == "0000000000000002"

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [
            (b"traceparent", b"00-1234567890abcdef1234567890abcdef-1234567890abcdef-01"),
            (b"tracestate", b"congo=t61rcWkgMzE"),
        ],
        "query_string": b"",
        "server": ("test", 80),
    }
    request = Request(scope)
    headers = app_module._w3c_propagation_headers(request)
    assert headers["traceparent"].startswith("00-1234")
    parsed_trace, parsed_span = app_module._parse_traceparent(headers["traceparent"])
    assert parsed_trace == "1234567890abcdef1234567890abcdef"
    assert parsed_span == "1234567890abcdef"
    assert app_module._parse_traceparent("bad") == (None, None)
    monkeypatch.setattr(app_module.prom_registry, "REGISTRY", None)
    app_module._unregister_metric("nonexistent")


def test_demo_trace_smoke(monkeypatch):
    app_module = _load_app(monkeypatch)

    client = TestClient(app_module.app)
    response = client.get(
        "/demo/trace",
        headers={
            "traceparent": "00-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-bbbbbbbbbbbbbbbb-01",
            "tracestate": "test=1",
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert client.get("/readyz").status_code == 200
    assert client.get("/metrics").status_code == 200


def test_opa_check_path(monkeypatch):
    app_module = _load_app(monkeypatch)
    app_module.OPA_URL = "http://opa"

    captured: dict[str, str] = {}

    class DummyResponse:
        status_code = 200

        def __init__(self):
            self._json = {"result": True}

        def json(self):
            return self._json

        def raise_for_status(self):
            return None

    class DummyClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # pragma: no cover - cleanup
            return False

        async def post(self, url, json=None, headers=None):
            captured.update(headers or {})
            return DummyResponse()

    monkeypatch.setattr(app_module.httpx, "AsyncClient", DummyClient)

    @app_module.app.get("/plugins/invoke/demo")
    async def _demo_handler():  # pragma: no cover - simple handler
        return {"ok": True}

    client = TestClient(app_module.app)
    traceparent = "00-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-cccccccccccccccc-01"
    response = client.get(
        "/plugins/invoke/demo",
        headers={"traceparent": traceparent},
    )
    assert response.status_code == 200
    assert captured.get("traceparent") == traceparent
    assert response.headers["X-Trace-Id"].startswith("aaaaaaaa")


@pytest.mark.asyncio
async def test_opa_check_no_url(monkeypatch):
    app_module = _load_app(monkeypatch)
    app_module.OPA_URL = ""

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/any",
        "headers": [],
        "query_string": b"",
        "server": ("test", 80),
    }
    request = Request(scope)
    request.state.request_id = "req"
    request.state.trace_headers = {}
    assert await app_module.opa_check(request) is True


def test_legacy_redirect(monkeypatch):
    app_module = _load_app(monkeypatch)
    future = datetime.utcnow() + timedelta(days=1)
    app_module.CUTOFF = future.isoformat()

    client = TestClient(app_module.app)
    response = client.get("/nlp-service/ner", allow_redirects=False)
    assert response.status_code == 308
    assert response.headers["location"].startswith("/doc-entities")


@pytest.mark.asyncio
async def test_opa_check_failure(monkeypatch):
    app_module = _load_app(monkeypatch)
    app_module.OPA_URL = "http://opa"

    class FailingClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def post(self, url, json=None, headers=None):
            raise httpx.HTTPError("boom")

    monkeypatch.setattr(app_module.httpx, "AsyncClient", FailingClient)

    scope = {
        "type": "http",
        "method": "POST",
        "path": "/plugins/invoke/demo",
        "headers": [],
        "query_string": b"",
        "server": ("test", 80),
    }
    request = Request(scope)
    request.state.request_id = "req"
    request.state.trace_headers = {}
    request.state.user_id = "user"
    request.state.tenant_id = "tenant"

    allowed = await app_module.opa_check(request)
    assert allowed is False
