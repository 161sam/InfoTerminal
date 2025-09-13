import os, time
from typing import Optional, Dict, Any
import httpx
from fastapi import FastAPI, HTTPException, Header
from starlette_exporter import PrometheusMiddleware, handle_metrics
try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
except Exception:
    FastAPIInstrumentor = None

AGENT_BASE_URL = os.getenv("AGENT_BASE_URL", "")
FLOWISE_API_KEY = os.getenv("FLOWISE_API_KEY", "")
TIMEOUT = float(os.getenv("FLOWISE_TIMEOUT_S", "30"))

app = FastAPI(title="Flowise Connector", version="0.1.0")
if os.getenv("IT_ENABLE_METRICS") == "1":
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", handle_metrics)

if FastAPIInstrumentor:
    try:
        FastAPIInstrumentor.instrument_app(app)
    except Exception:
        pass

@app.get("/healthz")
def healthz():
    return {"ok": True, "ts": int(time.time())}


@app.get("/readyz")
def readyz():
    return {"ok": True}

@app.get("/tools")
def tools():
    return {
        "tools": [
            {"name": "search.query"},
            {"name": "graph.neighbors"},
            {"name": "docs.ner"},
        ]
    }


@app.post("/playbooks/run")
async def run_playbook(pb: Dict[str, Any]):
    name = pb.get("name")
    if name == "InvestigatePerson":
        # Placeholder steps; real implementation would call search-api, graph-api and doc-entities
        return {"steps": ["search", "graph.neighbors", "docs.ner"], "result": {}}
    raise HTTPException(404, "unknown playbook")


@app.post("/chat")
async def chat(body: Dict[str, Any], authorization: Optional[str] = Header(None)):
    if not AGENT_BASE_URL:
        last = (body.get("messages") or [{}])[-1].get("content", "")
        return {"reply": f"stub: {last}"}

    headers = {"Content-Type": "application/json"}
    if FLOWISE_API_KEY:
        headers["Authorization"] = f"Bearer {FLOWISE_API_KEY}"
    if authorization:
        headers["X-Caller-Authorization"] = authorization

    url = f"{AGENT_BASE_URL}/api/v1/prediction"
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.post(url, json=body, headers=headers)
        r.raise_for_status()
        return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=str(e))
