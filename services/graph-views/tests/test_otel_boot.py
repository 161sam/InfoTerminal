import os, sys, importlib, types
import os
import sys
import importlib
import types
from pathlib import Path

sys.path.append(Path(__file__).resolve().parents[1].as_posix())


def test_otel_disabled(monkeypatch):
    monkeypatch.setenv("OTEL_SDK_DISABLED", "1")
    importlib.reload(importlib.import_module("obs.otel_boot"))


def test_otel_enabled(monkeypatch):
    monkeypatch.delenv("OTEL_SDK_DISABLED", raising=False)
    trace_mod = types.SimpleNamespace(set_tracer_provider=lambda tp: setattr(trace_mod, "tp", tp))
    metrics_mod = types.SimpleNamespace(set_meter_provider=lambda mp: setattr(metrics_mod, "mp", mp))
    otel_pkg = types.ModuleType("opentelemetry")
    otel_pkg.trace = trace_mod
    otel_pkg.metrics = metrics_mod
    sys.modules["opentelemetry"] = otel_pkg
    sys.modules["opentelemetry.trace"] = trace_mod
    sys.modules["opentelemetry.metrics"] = metrics_mod

    class Resource:
        @classmethod
        def create(cls, attrs):
            return types.SimpleNamespace(attrs=attrs)

    sys.modules["opentelemetry.sdk.resources"] = types.SimpleNamespace(Resource=Resource)

    class TracerProvider:
        def __init__(self, resource=None):
            self.resource = resource
        def add_span_processor(self, proc):
            self.proc = proc

    sys.modules["opentelemetry.sdk.trace"] = types.SimpleNamespace(TracerProvider=TracerProvider)

    class MeterProvider:
        def __init__(self, resource=None):
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

    sys.modules["opentelemetry.exporter.otlp.proto.grpc.trace_exporter"] = types.SimpleNamespace(
        OTLPSpanExporter=OTLPSpanExporter
    )

    class OTLPMetricExporter:
        def __init__(self, endpoint, insecure):
            self.endpoint = endpoint
            self.insecure = insecure

    sys.modules["opentelemetry.exporter.otlp.proto.grpc.metric_exporter"] = types.SimpleNamespace(
        OTLPMetricExporter=OTLPMetricExporter
    )

    importlib.reload(importlib.import_module("obs.otel_boot"))
    assert isinstance(trace_mod.tp, TracerProvider)
    assert isinstance(metrics_mod.mp, MeterProvider)
