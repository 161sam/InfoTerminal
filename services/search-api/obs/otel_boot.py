import os
import uuid
import logging
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware

INSTRUMENTATION_ENABLED = False
logger = logging.getLogger(__name__)

def setup_otel(app, service_name: str = "search-api") -> None:
    """Initialize OTEL tracing if IT_OTEL=1."""
    global INSTRUMENTATION_ENABLED
    if os.getenv("IT_OTEL") != "1":
        return
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.requests import RequestsInstrumentor
    except Exception as e:  # pragma: no cover - optional dependency
        logger.warning("OTEL init skipped: %s", e)
        return

    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://tempo:4318")
    attrs = {"service.name": os.getenv("OTEL_SERVICE_NAME", service_name)}
    for item in os.getenv("OTEL_RESOURCE_ATTRIBUTES", "deployment.environment=dev").split(","):
        if "=" in item:
            k, v = item.split("=", 1)
            attrs[k] = v
    ratio = float(os.getenv("OTEL_TRACES_SAMPLER_ARG", "0.1"))
    sampler = ParentBased(TraceIdRatioBased(ratio))
    try:
        exporter = OTLPSpanExporter(endpoint=endpoint)
    except Exception as e:  # pragma: no cover - exporter misconfig
        logger.warning("OTEL exporter disabled: %s", e)
        return
    provider = TracerProvider(resource=Resource.create(attrs), sampler=sampler)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    RequestsInstrumentor().instrument()

    class RequestIdMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next: Callable):
            req_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
            request.state.request_id = req_id
            span = trace.get_current_span()
            if span:
                span.set_attribute("http.request_id", req_id)
            response = await call_next(request)
            response.headers["X-Request-Id"] = req_id
            return response

    app.add_middleware(RequestIdMiddleware)
    INSTRUMENTATION_ENABLED = True
