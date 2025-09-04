import logging
import os
from typing import Optional

from fastapi import FastAPI


def setup_otel(app: FastAPI, service_name: str, version: Optional[str] = None) -> None:
    """Set up OpenTelemetry tracing if enabled via environment variables.

    Tracing is only initialised when ``IT_OTEL`` equals ``"1"``. Default
    environment variables for the OTLP exporter and sampler are provided if
    they are not already configured. The function is idempotent and will not
    re-instrument an application that was already initialised. Missing
    OpenTelemetry dependencies are handled gracefully with a logged warning.
    """

    if os.getenv("IT_OTEL") != "1" or getattr(app.state, "otel_enabled", False):
        return

    os.environ.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://tempo:4318")
    os.environ.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "http/protobuf")
    os.environ.setdefault("OTEL_TRACES_SAMPLER", "parentbased_traceidratio")
    os.environ.setdefault("OTEL_TRACES_SAMPLER_ARG", "0.1")
    os.environ.setdefault("OTEL_SERVICE_NAME", service_name)

    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
        from opentelemetry.instrumentation.requests import RequestsInstrumentor
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased
    except Exception as exc:  # pragma: no cover - optional dependency
        logging.getLogger(__name__).warning("opentelemetry not available: %s", exc)
        return

    attrs = {"service.name": service_name}
    if version:
        attrs["service.version"] = version
    if extra := os.getenv("OTEL_RESOURCE_ATTRIBUTES"):
        for part in extra.split(","):
            if "=" in part:
                k, v = part.split("=", 1)
                attrs[k.strip()] = v.strip()
    resource = Resource.create(attrs)

    ratio = float(os.getenv("OTEL_TRACES_SAMPLER_ARG", "0.1"))
    sampler = ParentBased(TraceIdRatioBased(ratio))
    provider = TracerProvider(resource=resource, sampler=sampler)
    exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"),
        protocol=os.getenv("OTEL_EXPORTER_OTLP_PROTOCOL", "http/protobuf"),
    )
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    FastAPIInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()

    app.state.otel_enabled = True
