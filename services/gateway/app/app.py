import os
import json
import time
import uuid
from datetime import datetime
import logging
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from .auth import auth_context
from _shared.audit import audit_log

AUTH_REQUIRED = os.getenv("IT_AUTH_REQUIRED", "0") == "1"
TENANCY_MODE = os.getenv("IT_TENANCY_MODE", "single")
TENANT_CLAIM = os.getenv("IT_TENANT_CLAIM", "tenant")
LEGACY_PREFIXES = ["/nlp-service", "/api/nlp-service"]
CUTOFF = os.getenv("IT_DEPRECATION_CUTOFF_DATE", "")
OPA_URL = os.getenv("OPA_URL", "")
SENSITIVE_PREFIXES = ["/plugins/invoke", "/graph-api/alg"]

REQUEST_COUNT = Counter(
    "gateway_requests_total",
    "Total requests",
    ["method", "path", "status"],
)
REQUEST_LATENCY = Histogram(
    "gateway_request_duration_seconds",
    "Request latency",
    ["method", "path", "status"],
    buckets=[0.1, 0.3, 1, 3, 10],
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
            r = await client.post(OPA_URL, json={"input": input_data})
            r.raise_for_status()
            data = r.json()
            return bool(data.get("result"))
    except Exception:
        return False


app = FastAPI(title="gateway")


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
    if path in ("/healthz", "/readyz"):
        return await call_next(request)

    rid = request.headers.get("x-request-id") or str(uuid.uuid4())
    request.state.request_id = rid
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
    logging.getLogger("gateway").info(
        json.dumps(
            {
                "service": "gateway",
                "request_id": rid,
                "user": getattr(request.state, "user_id", "anon"),
                "tenant": request.state.tenant_id,
                "path": path,
                "method": request.method,
                "status": resp.status_code,
            }
        )
    )
    return resp


@app.get("/healthz")
async def healthz():
    return {"ok": True}


@app.get("/readyz")
async def readyz():
    return {"ok": True}


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
