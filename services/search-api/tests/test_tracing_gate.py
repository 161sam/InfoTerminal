import importlib.util
import os
import pathlib
import sys
import types

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "src/search_api/app/main.py"


def _load_app(monkeypatch, enable: bool):
    sys.modules.pop("search_api._shared.obs.otel_boot", None)
    if enable:
        monkeypatch.setenv("IT_OTEL", "1")
    else:
        monkeypatch.delenv("IT_OTEL", raising=False)
    calls = {"fastapi": 0, "requests": 0, "httpx": 0}

    class DummyFastAPIInstrumentor:
        def instrument_app(self, app):
            calls["fastapi"] += 1

    class DummyRequestsInstrumentor:
        def instrument(self):
            calls["requests"] += 1

    class DummyHTTPXClientInstrumentor:
        def instrument(self):
            calls["httpx"] += 1

    class DummyResource:
        @classmethod
        def create(cls, attrs):
            return cls()

    class DummyTracerProvider:
        def __init__(self, *a, **k):
            pass

        def add_span_processor(self, proc):
            pass

    class DummyBatchSpanProcessor:
        def __init__(self, exporter):
            pass

    class DummyOTLPSpanExporter:
        def __init__(self, *a, **k):
            pass

    class DummyTraceIdRatioBased:
        def __init__(self, *a, **k):
            pass

    class DummyParentBased:
        def __init__(self, *a, **k):
            pass

    class DummyTrace:
        def set_tracer_provider(self, provider):
            pass

    monkeypatch.setitem(sys.modules, "opentelemetry", types.SimpleNamespace(trace=DummyTrace()))
    monkeypatch.setitem(sys.modules, "opentelemetry.trace", DummyTrace())
    monkeypatch.setitem(
        sys.modules,
        "opentelemetry.sdk.resources",
        types.SimpleNamespace(Resource=DummyResource),
    )
    monkeypatch.setitem(
        sys.modules,
        "opentelemetry.sdk.trace",
        types.SimpleNamespace(TracerProvider=DummyTracerProvider),
    )
    monkeypatch.setitem(
        sys.modules,
        "opentelemetry.sdk.trace.export",
        types.SimpleNamespace(BatchSpanProcessor=DummyBatchSpanProcessor),
    )
    monkeypatch.setitem(
        sys.modules,
        "opentelemetry.exporter.otlp.proto.http.trace_exporter",
        types.SimpleNamespace(OTLPSpanExporter=DummyOTLPSpanExporter),
    )
    monkeypatch.setitem(
        sys.modules,
        "opentelemetry.sdk.trace.sampling",
        types.SimpleNamespace(TraceIdRatioBased=DummyTraceIdRatioBased, ParentBased=DummyParentBased),
    )
    monkeypatch.setitem(
        sys.modules,
        "opentelemetry.instrumentation.fastapi",
        types.SimpleNamespace(FastAPIInstrumentor=DummyFastAPIInstrumentor),
    )
    monkeypatch.setitem(
        sys.modules,
        "opentelemetry.instrumentation.requests",
        types.SimpleNamespace(RequestsInstrumentor=DummyRequestsInstrumentor),
    )
    monkeypatch.setitem(
        sys.modules,
        "opentelemetry.instrumentation.httpx",
        types.SimpleNamespace(HTTPXClientInstrumentor=DummyHTTPXClientInstrumentor),
    )

    spec = importlib.util.spec_from_file_location("search_api.app.main", MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod.app, calls


def test_tracing_disabled(monkeypatch):
    _, calls = _load_app(monkeypatch, False)
    assert calls == {"fastapi": 0, "requests": 0, "httpx": 0}


def test_tracing_enabled(monkeypatch):
    _, calls = _load_app(monkeypatch, True)
    assert calls == {"fastapi": 1, "requests": 1, "httpx": 1}
