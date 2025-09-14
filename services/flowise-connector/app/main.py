import logging
import os
import time
from typing import Any, Dict, Optional

import httpx
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette_exporter import PrometheusMiddleware, handle_metrics

try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
except Exception:  # pragma: no cover - optional dependency
    FastAPIInstrumentor = None

from .errors import AgentUpstreamError, WorkflowTriggerError
from .http_client import request as http_request
from .it_logging import setup_logging

AGENT_BASE_URL = os.getenv("AGENT_BASE_URL", "")
FLOWISE_API_KEY = os.getenv("FLOWISE_API_KEY", "")
N8N_BASE = os.getenv("N8N_BASE_URL")
N8N_KEY = os.getenv("N8N_API_KEY")
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK_URL")

logger = logging.getLogger("flowise-connector")

app = FastAPI(title="Flowise Connector", version="0.1.0")
setup_logging(app, "flowise-connector")
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


@app.exception_handler(AgentUpstreamError)
async def handle_agent_error(request: Request, exc: AgentUpstreamError):
    logger.error(
        "agent_error",
        extra={
            "req_id": getattr(request.state, "req_id", None),
            "status": exc.status,
            "upstream": exc.upstream,
        },
    )
    return JSONResponse(
        status_code=exc.status,
        content={"status": exc.status, "detail": exc.detail, "upstream": exc.upstream},
    )


@app.exception_handler(WorkflowTriggerError)
async def handle_workflow_error(request: Request, exc: WorkflowTriggerError):
    logger.error(
        "workflow_error",
        extra={
            "req_id": getattr(request.state, "req_id", None),
            "status": exc.status,
            "upstream": exc.upstream,
        },
    )
    return JSONResponse(
        status_code=exc.status,
        content={"status": exc.status, "detail": exc.detail, "upstream": exc.upstream},
    )


@app.get("/tools")
def tools():
    return {
        "tools": [
            {"name": "search.query", "args": {"q": "string"}},
            {
                "name": "graph.neighbors",
                "args": {"nodeId": "string", "depth": "number"},
            },
            {"name": "docs.ner", "args": {"text": "string", "lang": "string"}},
            {"name": "dossier.build", "args": {"payload": "object"}},
        ]
    }


@app.post("/playbooks/run")
async def run_playbook(pb: Dict[str, Any]):
    name = pb.get("name")
    params = pb.get("params", {})
    search_url = f"http://localhost:{os.getenv('IT_PORT_SEARCH_API','8611')}"
    if name == "InvestigatePerson":
        q = params.get("q", "")
        s = await http_request("GET", f"{search_url}/search", params={"q": q})
        results = s.json()
        return {"name": name, "results": results}
    if name == "FinancialRiskAssistant":
        if N8N_WEBHOOK:
            await http_request("POST", N8N_WEBHOOK, json=params)
            return {"name": name, "status": "triggered", "n8n": "webhook"}
        if N8N_BASE and N8N_KEY:
            r = await http_request(
                "POST",
                f"{N8N_BASE}/rest/workflows/run",
                headers={"X-N8N-API-KEY": N8N_KEY},
                json={"params": params},
            )
            data = r.json() if r.content else {}
            return {
                "name": name,
                "status": "triggered",
                "n8n": "rest",
                "response": data,
            }
        return {"name": name, "status": "configured=false"}
    raise HTTPException(404, "unknown playbook")


@app.post("/chat")
async def chat(body: Dict[str, Any], authorization: Optional[str] = Header(None)):
    if not AGENT_BASE_URL:
        return {
            "reply": "(stub) Agent not configured; using local tools only.",
            "steps": [],
        }

    headers = {"Content-Type": "application/json"}
    if FLOWISE_API_KEY:
        headers["Authorization"] = f"Bearer {FLOWISE_API_KEY}"
    if authorization:
        headers["X-Caller-Authorization"] = authorization

    url = f"{AGENT_BASE_URL}/api/v1/prediction"
    try:
        r = await http_request("POST", url, json=body, headers=headers)
        return r.json()
    except httpx.TimeoutException:
        raise AgentUpstreamError(408, "request timeout", url)
    except httpx.HTTPStatusError as e:
        detail = (e.response.text if e.response else "") or str(e)
        status = e.response.status_code if e.response else 502
        raise AgentUpstreamError(status, detail, url)
    except httpx.HTTPError as e:
        raise AgentUpstreamError(502, str(e), url)


@app.post("/workflows/trigger")
async def trigger_workflow(body: Dict[str, Any]):
    name = body.get("name")
    params = body.get("params", {})
    if N8N_WEBHOOK:
        url = N8N_WEBHOOK
        try:
            await http_request("POST", url, json={"name": name, "params": params})
            return {"status": "triggered", "n8n": "webhook"}
        except httpx.TimeoutException:
            raise WorkflowTriggerError(408, "request timeout", url)
        except httpx.HTTPStatusError as e:
            detail = (e.response.text if e.response else "") or str(e)
            raise WorkflowTriggerError(
                e.response.status_code if e.response else 502, detail, url
            )
        except httpx.HTTPError as e:
            raise WorkflowTriggerError(502, str(e), url)
    if N8N_BASE and N8N_KEY:
        url = f"{N8N_BASE}/rest/workflows/run"
        try:
            r = await http_request(
                "POST",
                url,
                headers={"X-N8N-API-KEY": N8N_KEY},
                json={"name": name, "params": params},
            )
            data = r.json() if r.content else {}
            return {"status": "triggered", "n8n": "rest", "response": data}
        except httpx.TimeoutException:
            raise WorkflowTriggerError(408, "request timeout", url)
        except httpx.HTTPStatusError as e:
            detail = (e.response.text if e.response else "") or str(e)
            raise WorkflowTriggerError(
                e.response.status_code if e.response else 502, detail, url
            )
        except httpx.HTTPError as e:
            raise WorkflowTriggerError(502, str(e), url)
    raise WorkflowTriggerError(500, "n8n not configured", "n8n")
