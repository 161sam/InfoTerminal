import os
from typing import Optional


def setup_otel(app, service_name: Optional[str] = None, service_version: Optional[str] = None, **_ignored) -> None:
    """
    Aktiviert OpenTelemetry für FastAPI, wenn OTEL_ENABLED/ENABLE_OTEL truthy ist.
    Akzeptiert optionale service_name/service_version; ignoriert weitere kwargs.
    Fällt still zurück, wenn OTel nicht installiert ist.
    """
    enabled = str(os.getenv("OTEL_ENABLED", os.getenv("ENABLE_OTEL", "0"))).lower() in ("1", "true", "yes")
    if not enabled:
        return
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor

        name = service_name or os.getenv("OTEL_SERVICE_NAME", "graph-views")
        version = service_version or os.getenv("OTEL_SERVICE_VERSION")

        attrs = {"service.name": name}
        if version:
            attrs["service.version"] = version
        resource = Resource.create(attrs)

        endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4318")
        headers_env = os.getenv("OTEL_EXPORTER_OTLP_HEADERS", "")
        headers = {}
        for pair in headers_env.split(","):
            if "=" in pair:
                k, v = pair.split("=", 1)
                headers[k.strip()] = v.strip()

        provider = TracerProvider(resource=resource)
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, headers=headers or None)))
        trace.set_tracer_provider(provider)

        FastAPIInstrumentor.instrument_app(app)
    except Exception:
        # Kein Hard-Fail in Minimal-Container
        return
