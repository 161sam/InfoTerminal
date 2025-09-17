import hashlib
import json
import os
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from .crypto_utils import sign_message

LEDGER_PATH = os.getenv("FORENSICS_LEDGER", "/data/forensics_ledger.jsonl")
os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)

app = FastAPI(title="Forensics Service", version="0.1.0")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def append_ledger(entry: dict):
    prev = None
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, 'rb') as f:
            try:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b"\n":
                    f.seek(-2, os.SEEK_CUR)
                last = f.readline().decode().strip()
                if last:
                    prev = json.loads(last).get("record_hash")
            except Exception:
                prev = None
    entry["prev_hash"] = prev
    payload = json.dumps(entry, ensure_ascii=False)
    entry["record_hash"] = sha256_bytes(payload.encode())
    with open(LEDGER_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


class VerifyRequest(BaseModel):
    sha256: str


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    data = await file.read()
    digest = sha256_bytes(data)
    entry = {
        "ts": datetime.utcnow().isoformat(),
        "filename": file.filename,
        "size": len(data),
        "sha256": digest,
    }
    append_ledger(entry)
    return {"status": "ok", "sha256": digest}


@app.post("/verify")
def verify(req: VerifyRequest):
    if not os.path.exists(LEDGER_PATH):
        return {"present": False}
    with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                obj = json.loads(line)
                if obj.get("sha256") == req.sha256:
                    return {"present": True, "entry": obj}
            except Exception:
                continue
    return {"present": False}


@app.get("/receipt/{sha256}")
def receipt(sha256: str):
    """Return a signed receipt for a given SHA256 if present in ledger."""
    if not os.path.exists(LEDGER_PATH):
        raise HTTPException(404, "ledger empty")
    with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            obj = json.loads(line)
            if obj.get('sha256') == sha256:
                payload = json.dumps({k: obj[k] for k in ['ts','filename','size','sha256','prev_hash','record_hash']}, ensure_ascii=False).encode()
                sig = sign_message(payload)
                return {"entry": obj, "signature": sig}
    raise HTTPException(404, "not found")


@app.get("/chain/report")
def chain_report():
    """Return the full append-only ledger."""
    items = []
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    items.append(json.loads(line))
                except Exception:
                    continue
    return {"items": items, "count": len(items)}
