import os, time
from typing import Optional, Dict, Any
import httpx
from fastapi import FastAPI, HTTPException, Header, Depends
try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
except Exception:
    FastAPIInstrumentor = None

FLOWISE_URL = os.getenv("FLOWISE_URL", "http://flowise:3000")
FLOWISE_API_KEY = os.getenv("FLOWISE_API_KEY", "")
TIMEOUT = float(os.getenv("FLOWISE_TIMEOUT_S", "30"))

app = FastAPI(title="Flowise Connector", version="0.1.0")

if FastAPIInstrumentor:
    try:
        FastAPIInstrumentor.instrument_app(app)
    except Exception:
        pass

@app.get("/healthz")
def healthz():
    return {"ok": True, "ts": int(time.time())}

@app.post("/chat/{agent_id}")
async def chat(agent_id: str, body: Dict[str, Any], authorization: Optional[str] = Header(None)):
    headers = {"Content-Type": "application/json"}
    if FLOWISE_API_KEY:
        headers["Authorization"] = f"Bearer {FLOWISE_API_KEY}"
    # Optional: forward caller auth (keycloak) if needed
    if authorization:
        headers["X-Caller-Authorization"] = authorization

    url = f"{FLOWISE_URL}/api/v1/prediction/{agent_id}"
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.post(url, json=body, headers=headers)
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=str(e))
