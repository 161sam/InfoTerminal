import os
from datetime import datetime
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from .auth import auth_context

AUTH_REQUIRED = os.getenv("IT_AUTH_REQUIRED", "0") == "1"
TENANCY_MODE = os.getenv("IT_TENANCY_MODE", "single")
TENANT_CLAIM = os.getenv("IT_TENANT_CLAIM", "tenant")
LEGACY_PREFIXES = ["/nlp-service", "/api/nlp-service"]
CUTOFF = os.getenv("IT_DEPRECATION_CUTOFF_DATE", "")

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
    resp = await call_next(request)
    resp.headers["X-API-Version"] = "v1"
    resp.headers["X-Tenant-Id"] = request.state.tenant_id
    if ctx:
        resp.headers["X-User-Id"] = request.state.user_id
        resp.headers["X-Scopes"] = " ".join(request.state.scopes)
    return resp


@app.get("/healthz")
async def healthz():
    return {"ok": True}


@app.get("/readyz")
async def readyz():
    return {"ok": True}
