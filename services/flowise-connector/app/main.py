import os, time, uuid
from typing import Optional, Dict, Any
import httpx
from fastapi import FastAPI, HTTPException, Header
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics
try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
except Exception:
    FastAPIInstrumentor = None

AGENT_BASE_URL = os.getenv("AGENT_BASE_URL", "")
AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT_MS", "120000"))
FLOWISE_API_KEY = os.getenv("FLOWISE_API_KEY", "")
N8N_BASE = os.getenv("N8N_BASE_URL")
N8N_KEY = os.getenv("N8N_API_KEY")
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK_URL")

REQ_ID_HEADER = os.getenv("IT_REQUEST_ID_HEADER", "X-Request-Id")

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get(REQ_ID_HEADER) or str(uuid.uuid4())
        request.state.request_id = req_id
        response = await call_next(request)
        response.headers[REQ_ID_HEADER] = req_id
        return response

app = FastAPI(title="Flowise Connector", version="0.1.0")
app.add_middleware(RequestIdMiddleware)
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
            {"name": "search.query", "args": {"q": "string"}},
            {"name": "graph.neighbors", "args": {"nodeId": "string", "depth": "number"}},
            {"name": "docs.ner", "args": {"text": "string", "lang": "string"}},
            {"name": "dossier.build", "args": {"payload": "object"}},
        ]
    }


@app.post("/playbooks/run")
async def run_playbook(pb: Dict[str, Any]):
    name = pb.get("name")
    params = pb.get("params", {})
    search_url = f"http://localhost:{os.getenv('IT_PORT_SEARCH_API','8611')}"
    graph_url = f"http://localhost:{os.getenv('IT_PORT_GRAPH_API','8612')}"
    nlp_url = f"http://localhost:{os.getenv('IT_PORT_DOC_ENTITIES','8613')}"
    async with httpx.AsyncClient(timeout=30) as client:
        if name == "InvestigatePerson":
            q = params.get("q", "")
            s = await client.get(f"{search_url}/search", params={"q": q})
            s.raise_for_status()
            results = s.json()
            return {"name": name, "results": results}
        if name == "FinancialRiskAssistant":
            if N8N_WEBHOOK:
                r = await client.post(N8N_WEBHOOK, json=params)
                r.raise_for_status()
                return {"name": name, "status": "triggered", "n8n": "webhook"}
            if N8N_BASE and N8N_KEY:
                r = await client.post(
                    f"{N8N_BASE}/rest/workflows/run",
                    headers={"X-N8N-API-KEY": N8N_KEY},
                    json={"params": params},
                )
                r.raise_for_status()
                data = r.json() if r.content else {}
                return {"name": name, "status": "triggered", "n8n": "rest", "response": data}
            return {"name": name, "status": "configured=false"}
    raise HTTPException(404, "unknown playbook")


@app.post("/chat")
async def chat(body: Dict[str, Any], authorization: Optional[str] = Header(None)):
    if not AGENT_BASE_URL:
        last = (body.get("messages") or [{}])[-1].get("content", "")
        return {"reply": "(stub) Agent not configured; using local tools only.", "steps": []}

    headers = {"Content-Type": "application/json"}
    if FLOWISE_API_KEY:
        headers["Authorization"] = f"Bearer {FLOWISE_API_KEY}"
    if authorization:
        headers["X-Caller-Authorization"] = authorization

    url = f"{AGENT_BASE_URL}/api/v1/prediction"
    try:
        async with httpx.AsyncClient(timeout=AGENT_TIMEOUT/1000) as client:
            r = await client.post(url, json=body, headers=headers)
        r.raise_for_status()
        return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.post("/workflows/trigger")
async def trigger_workflow(body: Dict[str, Any]):
    name = body.get("name")
    params = body.get("params", {})
    async with httpx.AsyncClient(timeout=30) as client:
        if N8N_WEBHOOK:
            r = await client.post(N8N_WEBHOOK, json={"name": name, "params": params})
            r.raise_for_status()
            return {"status": "triggered", "n8n": "webhook"}
        if N8N_BASE and N8N_KEY:
            r = await client.post(
                f"{N8N_BASE}/rest/workflows/run",
                headers={"X-N8N-API-KEY": N8N_KEY},
                json={"name": name, "params": params},
            )
            r.raise_for_status()
            data = r.json() if r.content else {}
            return {"status": "triggered", "n8n": "rest", "response": data}
    raise HTTPException(500, "n8n not configured")
