try:
    from obs.otel_boot import *  # noqa
except Exception:
    pass

import os, json, datetime, httpx
from typing import Any, Dict, List
from fastapi import FastAPI, Request
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentation
from prometheus_client import make_asgi_app

CH = os.getenv("CH_URL","http://clickhouse.clickhouse.svc.cluster.local:8123")
CH_DB = os.getenv("CH_DB","logs")
CH_TABLE = os.getenv("CH_TABLE","opa_decisions")

app = FastAPI(title="OPA Audit Sink", version="0.1.0")
FastAPIInstrumentation().instrument_app(app)
app.mount("/metrics", make_asgi_app())

@app.get("/healthz")
def health(): return {"ok": True}

def _row(e: Dict[str,Any]) -> Dict[str,Any]:
    # OPA decision log schema: https://www.openpolicyagent.org/docs/latest/management-decision-logs/
    ts = e.get("timestamp") or datetime.datetime.utcnow().isoformat()
    path = e.get("path","")
    decision_id = e.get("decision_id","")
    inp = e.get("input",{}) or {}
    user = ((inp.get("user") or {}).get("username")) or ""
    roles = (inp.get("user") or {}).get("roles") or []
    tenant = (inp.get("user") or {}).get("tenant") or ""
    cls = (inp.get("resource") or {}).get("classification") or ""
    action = inp.get("action") or ""
    res = e.get("result", False)
    return {
        "ts": ts, "path": path, "decision_id": decision_id, "user": user,
        "roles": roles, "tenant": tenant, "classification": cls, "action": action,
        "allowed": 1 if bool(res) else 0,
        "policy_version": e.get("bundles",{}).get("main",{}).get("revision",""),
        "raw": json.dumps(e, separators=(",",":"))
    }

@app.post("/logs")
async def logs(request: Request):
    payload = await request.json()
    events: List[Dict[str,Any]] = payload if isinstance(payload, list) else [payload]
    rows = [_row(e) for e in events]
    # insert via JSONEachRow (ClickHouse HTTP)
    data = "\n".join(json.dumps(r) for r in rows)
    q = f"INSERT INTO {CH_DB}.{CH_TABLE} FORMAT JSONEachRow"
    async with httpx.AsyncClient(timeout=10.0) as c:
        r = await c.post(f"{CH}/?query={q}", content=data, headers={"Content-Type":"application/json"})
        r.raise_for_status()
    return {"ingested": len(rows)}
