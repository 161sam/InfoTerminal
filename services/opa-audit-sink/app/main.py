import os, time
from fastapi import FastAPI, Request
from typing import Any, Dict

app = FastAPI(title="OPA Audit Sink", version="0.1.0")

@app.get("/healthz")
def healthz():
    return {"ok": True, "ts": int(time.time())}

@app.post("/audit")
async def audit(req: Request):
    payload: Dict[str, Any] = await req.json()
    # Hier könntest du in eine DB/Queue schreiben; wir loggen zur Konsole
    print("[AUDIT]", payload)
    return {"ok": True}
