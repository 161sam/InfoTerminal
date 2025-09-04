import importlib
import sys
import types


def test_otel_boot_disabled(monkeypatch):
    monkeypatch.setenv("OTEL_SDK_DISABLED", "1")
    sys.modules.pop("obs.otel_boot", None)
    m = importlib.import_module("obs.otel_boot")
    assert not hasattr(m, "trace")


def test_otel_boot_enabled(monkeypatch):
    monkeypatch.delenv("OTEL_SDK_DISABLED", raising=False)
    trace_called = {}
    metrics_called = {}

    def set_tracer_provider(tp):
        trace_called["tp"] = tp
    def set_meter_provider(mp):
        metrics_called["mp"] = mp
    dummy_trace = types.SimpleNamespace(set_tracer_provider=set_tracer_provider)
    dummy_metrics = types.SimpleNamespace(set_meter_provider=set_meter_provider)
    sys.modules["opentelemetry"] = types.SimpleNamespace(trace=dummy_trace, metrics=dummy_metrics)
    sys.modules["opentelemetry.trace"] = dummy_trace
    sys.modules["opentelemetry.metrics"] = dummy_metrics

    class Resource:
        @staticmethod
        def create(d):
            return d
    sys.modules["opentelemetry.sdk.resources"] = types.SimpleNamespace(Resource=Resource)

    class TracerProvider:
        def __init__(self, resource):
            self.resource = resource
        def add_span_processor(self, proc):
            self.proc = proc
    sys.modules["opentelemetry.sdk.trace"] = types.SimpleNamespace(TracerProvider=TracerProvider)

    class MeterProvider:
        def __init__(self, resource):
            self.resource = resource
    sys.modules["opentelemetry.sdk.metrics"] = types.SimpleNamespace(MeterProvider=MeterProvider)

    class BatchSpanProcessor:
        def __init__(self, exporter):
            self.exporter = exporter
    sys.modules["opentelemetry.sdk.trace.export"] = types.SimpleNamespace(BatchSpanProcessor=BatchSpanProcessor)

    class OTLPSpanExporter:
        def __init__(self, endpoint, insecure):
            self.endpoint = endpoint
            self.insecure = insecure
    sys.modules["opentelemetry.exporter.otlp.proto.grpc.trace_exporter"] = types.SimpleNamespace(OTLPSpanExporter=OTLPSpanExporter)

    class OTLPMetricExporter:
        def __init__(self, endpoint, insecure):
            self.endpoint = endpoint
            self.insecure = insecure
    sys.modules["opentelemetry.exporter.otlp.proto.grpc.metric_exporter"] = types.SimpleNamespace(OTLPMetricExporter=OTLPMetricExporter)

    sys.modules.pop("obs.otel_boot", None)
    m = importlib.import_module("obs.otel_boot")
    assert trace_called["tp"].resource["service.name"] == "search-api"
    assert metrics_called["mp"].resource["service.name"] == "search-api"
