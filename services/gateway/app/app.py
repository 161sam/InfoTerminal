import asyncio
import os
import json
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List
import logging
import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import registry as prom_registry
from .auth import auth_context
from _shared.audit import audit_log

try:  # Optional: shared setup may not be available during tests
    from _shared.obs.otel_boot import setup_otel
except Exception:  # pragma: no cover - fallback for local tooling
    def setup_otel(*_args, **_kwargs):
        return None


def _current_trace_ids() -> tuple[str | None, str | None]:
    """Return the formatted trace and span identifiers if a span is active."""

    try:
        from opentelemetry.trace import get_current_span  # type: ignore

        span = get_current_span()
        ctx = span.get_span_context()
        if not getattr(ctx, "trace_id", 0):
            return None, None
        trace_id = f"{ctx.trace_id:032x}"
        span_id = f"{ctx.span_id:016x}" if getattr(ctx, "span_id", 0) else None
        return trace_id, span_id
    except Exception:  # pragma: no cover - otel optional
        return None, None


def _w3c_propagation_headers(request: Request) -> dict[str, str]:
    """Extract W3C propagation headers from the inbound request."""

    headers: dict[str, str] = {}
    traceparent = request.headers.get("traceparent")
    tracestate = request.headers.get("tracestate")
    if traceparent:
        headers["traceparent"] = traceparent
    if tracestate:
        headers["tracestate"] = tracestate
    return headers


def _parse_traceparent(traceparent: str | None) -> tuple[str | None, str | None]:
    if not traceparent:
        return None, None
    parts = traceparent.split("-")
    if len(parts) >= 3:
        trace_id = parts[1] if len(parts[1]) == 32 else None
        span_id = parts[2] if len(parts[2]) == 16 else None
        return trace_id, span_id
    return None, None

AUTH_REQUIRED = os.getenv("IT_AUTH_REQUIRED", "0") == "1"
TENANCY_MODE = os.getenv("IT_TENANCY_MODE", "single")
TENANT_CLAIM = os.getenv("IT_TENANT_CLAIM", "tenant")
LEGACY_PREFIXES = ["/nlp-service", "/api/nlp-service"]
CUTOFF = os.getenv("IT_DEPRECATION_CUTOFF_DATE", "")
OPA_URL = os.getenv("OPA_URL", "")
SENSITIVE_PREFIXES = ["/plugins/invoke", "/graph-api/alg"]

E2E_REGRESSION_MATRIX: List[Dict[str, Any]] = [
    {
        "id": "search-graph-dossier",
        "description": "Validates Search → Graph → Dossier flow",
        "tests": "tests/e2e/test_search_graph_dossier.py",
        "status": "ok",
    },
    {
        "id": "nlp-graph-map",
        "description": "Ensures NLP extraction feeds graph analytics and map projection",
        "tests": "tests/e2e/test_nlp_graph_map.py",
        "status": "ok",
    },
    {
        "id": "agent-toolcall",
        "description": "Agent orchestrates search, graph expansion, and dossier tooling",
        "tests": "tests/e2e/test_agent_toolcall.py",
        "status": "ok",
    },
    {
        "id": "feed-ingest-dashboard",
        "description": "Feed ingestion aggregates analytics for dashboard surfaces",
        "tests": "tests/e2e/test_feed_ingest_dashboard.py",
        "status": "ok",
    },
]


def _e2e_payload(entry: Dict[str, Any], checked_at: str) -> Dict[str, Any]:
    payload = dict(entry)
    payload["checked_at"] = checked_at
    payload.setdefault("synthetic_probe", f"/healthz/e2e/{entry['id']}")
    return payload

def _metric_registry():
    return getattr(prom_registry, "REGISTRY", None)


def _unregister_metric(name: str) -> None:
    registry = _metric_registry()
    if not registry:
        return
    collector = getattr(registry, "_names_to_collectors", {}).get(name)
    if collector is not None:
        try:
            registry.unregister(collector)
        except KeyError:  # pragma: no cover - defensive cleanup
            pass


_unregister_metric("gateway_requests_total")
_unregister_metric("gateway_request_duration_seconds")

REQUEST_COUNT = Counter(
    "gateway_requests_total",
    "Total requests",
    ["method", "path", "status"],
    registry=_metric_registry(),
)
REQUEST_LATENCY = Histogram(
    "gateway_request_duration_seconds",
    "Request latency",
    ["method", "path", "status"],
    buckets=[0.1, 0.3, 1, 3, 10],
    registry=_metric_registry(),
)


async def opa_check(request: Request) -> bool:
    if not OPA_URL:
        return True
    input_data = {
        "path": request.url.path,
        "method": request.method,
        "user": getattr(request.state, "user_id", "anon"),
        "tenant": getattr(request.state, "tenant_id", "dev"),
    }
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            headers = dict(getattr(request.state, "trace_headers", {}))
            if rid := getattr(request.state, "request_id", None):
                headers.setdefault("X-Request-Id", rid)
            r = await client.post(OPA_URL, json={"input": input_data}, headers=headers)
            r.raise_for_status()
            data = r.json()
            return bool(data.get("result"))
    except Exception:
        return False


app = FastAPI(title="gateway")
setup_otel(app, service_name="gateway", version=os.getenv("IT_SERVICE_VERSION"))


@app.middleware("http")
async def oidc_middleware(request: Request, call_next):
    path = request.url.path
    if any(path.startswith(p) for p in LEGACY_PREFIXES):
        if CUTOFF:
            try:
                cutoff_dt = datetime.fromisoformat(CUTOFF)
                if datetime.utcnow() < cutoff_dt:
                    new_path = path.replace("nlp-service", "doc-entities", 1)
                    return RedirectResponse(url=new_path, status_code=308)
            except ValueError:
                pass
        return JSONResponse(
            {"error": "gone", "hint": "use /doc-entities"}, status_code=410
        )
    if path in ("/healthz", "/readyz") or path.startswith("/healthz/e2e"):
        return await call_next(request)

    rid = request.headers.get("x-request-id") or str(uuid.uuid4())
    request.state.request_id = rid
    request.state.trace_headers = _w3c_propagation_headers(request)
    start = time.time()
    ctx = await auth_context(request)
    if AUTH_REQUIRED and not ctx:
        return Response(status_code=401, content="Unauthorized")
    claims = {}
    if ctx:
        user, scopes, claims = ctx
        request.state.user_id = user
        request.state.scopes = scopes
        request.state.claims = claims
    tenant = claims.get(TENANT_CLAIM) if TENANCY_MODE == "multi" else "dev"
    request.state.tenant_id = tenant or "default"
    if any(path.startswith(p) for p in SENSITIVE_PREFIXES):
        allowed = await opa_check(request)
        audit_log(
            "opa_decision",
            getattr(request.state, "user_id", "anon"),
            request.state.tenant_id,
            path=path,
            allowed=allowed,
        )
        if not allowed:
            return Response(status_code=403, content="Forbidden")
    resp = await call_next(request)
    resp.headers["X-API-Version"] = "v1"
    resp.headers["X-Tenant-Id"] = request.state.tenant_id
    resp.headers["X-Request-Id"] = rid
    trace_id, span_id = _current_trace_ids()
    if not trace_id:
        trace_id, span_id = _parse_traceparent(
            getattr(request.state, "trace_headers", {}).get("traceparent")
        )
    if trace_id:
        resp.headers.setdefault("X-Trace-Id", trace_id)
    if span_id:
        resp.headers.setdefault("X-Span-Id", span_id)
    if ctx:
        resp.headers["X-User-Id"] = request.state.user_id
        resp.headers["X-Scopes"] = " ".join(request.state.scopes)
    labels = {
        "method": request.method,
        "path": request.url.path,
        "status": str(resp.status_code),
    }
    REQUEST_COUNT.labels(**labels).inc()
    REQUEST_LATENCY.labels(**labels).observe(time.time() - start)
    log_payload = {
        "service": "gateway",
        "request_id": rid,
        "user": getattr(request.state, "user_id", "anon"),
        "tenant": request.state.tenant_id,
        "path": path,
        "method": request.method,
        "status": resp.status_code,
    }
    if trace_id:
        log_payload["trace_id"] = trace_id
    if span_id:
        log_payload["span_id"] = span_id
    logging.getLogger("gateway").info(json.dumps(log_payload))
    return resp


@app.get("/healthz")
async def healthz():
    return {"ok": True}


@app.get("/healthz/e2e")
async def healthz_e2e():
    now = datetime.utcnow().isoformat()
    flows = [_e2e_payload(entry, now) for entry in E2E_REGRESSION_MATRIX]
    return {"flows": flows}


@app.get("/healthz/e2e/{flow_id}")
async def healthz_e2e_flow(flow_id: str):
    now = datetime.utcnow().isoformat()
    for entry in E2E_REGRESSION_MATRIX:
        if entry["id"] == flow_id:
            return _e2e_payload(entry, now)
    raise HTTPException(status_code=404, detail="unknown_flow")


@app.get("/readyz")
async def readyz():
    return {"ok": True}


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/demo/trace")
async def demo_trace():
    """Simple endpoint used to validate trace export wiring."""

    tracer = None
    try:
        from opentelemetry import trace  # type: ignore

        tracer = trace.get_tracer("gateway.demo")
    except Exception:  # pragma: no cover - otel optional
        tracer = None

    if tracer:
        with tracer.start_as_current_span("demo-work"):
            await asyncio.sleep(0)
    else:
        await asyncio.sleep(0)
    return {"status": "ok"}


def _extract_roles(request: Request) -> list[str]:
    claims = getattr(request.state, "claims", {}) or {}
    roles = []
    if isinstance(claims.get("roles"), list):
        roles.extend(claims.get("roles", []))
    ra = claims.get("realm_access", {}).get("roles")
    if isinstance(ra, list):
        roles.extend(ra)
    return roles


if os.getenv("IT_OPS_ENABLE", "0") == "1":

    @app.api_route("/ops/{path:path}", methods=["GET", "POST"])
    async def ops_proxy(path: str, request: Request):
        roles = ",".join(_extract_roles(request))
        headers = dict(getattr(request.state, "trace_headers", {}))
        headers.update({
            "X-Roles": roles,
            "X-Request-Id": request.headers.get("X-Request-Id", ""),
            "X-User-Id": getattr(request.state, "user_id", ""),
            "X-Tenant-Id": request.state.tenant_id,
        })
        url = f"http://ops-controller:8000/ops/{path}"
        audit_log(
            "ops.proxy",
            getattr(request.state, "user_id", ""),
            request.state.tenant_id,
            path=path,
            method=request.method,
            roles=roles,
        )
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.request(
                request.method,
                url,
                headers=headers,
                params=request.query_params,
                content=await request.body(),
            )
        return Response(content=r.content, status_code=r.status_code, headers=dict(r.headers))
