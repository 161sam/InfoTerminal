import json
import logging
import logging.config
import os
import time
import uuid
from datetime import datetime
from typing import Set

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, service_name: str, env: str):
        super().__init__(app)
        self.logger = logging.getLogger(service_name)
        sample = os.getenv("IT_LOG_SAMPLING", "/healthz,/metrics")
        self.skip_paths: Set[str] = {p for p in sample.split(",") if p}

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        req_id = request.headers.get("X-Request-Id") or getattr(request.state, "request_id", None) or str(uuid.uuid4())
        request.state.req_id = req_id
        start = time.time()
        trace_id = span_id = None
        if os.getenv("IT_OTEL") == "1":
            try:
                from opentelemetry.trace import get_current_span  # type: ignore

                span = get_current_span()
                ctx = span.get_span_context()
                trace_id = f"{getattr(ctx, 'trace_id', 0):032x}" if getattr(ctx, "trace_id", 0) else None
                span_id = f"{getattr(ctx, 'span_id', 0):016x}" if getattr(ctx, "span_id", 0) else None
            except Exception:
                trace_id = span_id = None
        status = 500
        response: Response | None = None
        try:
            response = await call_next(request)
            status = response.status_code
            return response
        finally:
            duration = (time.time() - start) * 1000
            path = request.url.path
            if response is not None:
                response.headers.setdefault("X-Request-Id", req_id)
            if path not in self.skip_paths or status >= 400:
                extra = {
                    "req_id": req_id,
                    "method": request.method,
                    "path": path,
                    "status": status,
                    "dur_ms": round(duration, 3),
                }
                if request.client:
                    extra["client_ip"] = request.client.host
                if trace_id:
                    extra["trace_id"] = trace_id
                if span_id:
                    extra["span_id"] = span_id
                self.logger.info("request", extra=extra)


def setup_logging(app, service_name: str):
    if os.getenv("IT_JSON_LOGS", "1") != "1":
        return
    log_level = os.getenv("IT_LOG_LEVEL", "INFO").upper()
    env = os.getenv("IT_ENV", "dev")

    class JsonFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:  # pragma: no cover - simple
            ts = datetime.utcnow().isoformat(timespec="milliseconds") + "Z"
            data = {
                "ts": ts,
                "level": record.levelname.lower(),
                "service": service_name,
                "env": env,
            }
            for key in (
                "req_id",
                "trace_id",
                "span_id",
                "client_ip",
                "method",
                "path",
                "status",
                "dur_ms",
            ):
                val = getattr(record, key, None)
                if val is not None:
                    data[key] = val
            data["msg"] = record.getMessage()
            return json.dumps(data, separators=(",", ":"))

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"json": {"()": JsonFormatter}},
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": "json",
                "stream": "ext://sys.stdout",
            },
            "null": {"class": "logging.NullHandler"},
        },
        "root": {"handlers": ["default"], "level": log_level},
        "loggers": {
            "uvicorn": {"handlers": ["default"], "level": log_level, "propagate": False},
            "uvicorn.error": {"handlers": ["default"], "level": log_level, "propagate": False},
            "uvicorn.access": {"handlers": ["null"], "level": log_level, "propagate": False},
        },
    }
    logging.config.dictConfig(logging_config)
    app.add_middleware(RequestLogMiddleware, service_name=service_name, env=env)
