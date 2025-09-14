import os
from fastapi import FastAPI, Request, Response
from .auth import auth_context

AUTH_REQUIRED = os.getenv("IT_AUTH_REQUIRED", "0") == "1"
TENANCY_MODE = os.getenv("IT_TENANCY_MODE", "single")
TENANT_CLAIM = os.getenv("IT_TENANT_CLAIM", "tenant")

app = FastAPI(title="gateway")


@app.middleware("http")
async def oidc_middleware(request: Request, call_next):
    path = request.url.path
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
