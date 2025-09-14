from fastapi import FastAPI
from services.common.tenancy import tenant_context_middleware
from .plugins.loader import router as plugins_loader_router

app = FastAPI(title="agent-connector")

app.middleware("http")(tenant_context_middleware)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/readyz")
async def readyz():
    return {"status": "ok"}


app.include_router(plugins_loader_router)
