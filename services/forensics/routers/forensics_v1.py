"""
Forensics v1 router for chain of custody operations.
Provides evidence ingestion, verification, receipts, and chain reporting.
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from pydantic import BaseModel, Field

# Import shared standards
import sys
from pathlib import Path
SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parent.parent
for p in (SERVICE_DIR, REPO_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

try:
    from _shared.api_standards.error_schemas import raise_http_error
    from _shared.api_standards.pagination import PaginatedResponse
except ImportError:
    # Fallback for legacy compatibility
    def raise_http_error(code: str, message: str, details: Optional[Dict] = None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                          detail={"error": {"code": code, "message": message, "details": details or {}}})
    
    class PaginatedResponse(BaseModel):
        items: list
        total: int
        page: int = 1
        size: int = 10

router = APIRouter(tags=["Forensics"], prefix="/v1")

LEDGER_PATH = os.getenv("FORENSICS_LEDGER", "/data/forensics_ledger.jsonl")


def sha256_bytes(b: bytes) -> str:
    """Calculate SHA256 hash of bytes."""
    return hashlib.sha256(b).hexdigest()


def append_ledger(entry: dict):
    """Append entry to blockchain-like ledger with previous hash linking."""
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    
    prev = None
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, 'rb') as f:
            try:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b"\\n":
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
        f.write(json.dumps(entry, ensure_ascii=False) + "\\n")


# Import models
from ..models import (
    VerifyRequest,
    EvidenceEntry,
    IngestResponse,
    VerifyResponse,
    ReceiptResponse,
    ChainReport
)


# API Endpoints
@router.post("/evidence/ingest", response_model=IngestResponse)
async def ingest_evidence(file: UploadFile = File(...)):
    """
    Ingest digital evidence into chain of custody.
    
    Creates an immutable record with:
    - Timestamp
    - File metadata
    - SHA256 hash
    - Previous record hash (blockchain-like)
    """
    try:
        data = await file.read()
        digest = sha256_bytes(data)
        
        entry = {
            "ts": datetime.utcnow().isoformat(),
            "filename": file.filename or "unknown",
            "size": len(data),
            "sha256": digest,
        }
        
        append_ledger(entry)
        
        return IngestResponse(
            status="success",
            sha256=digest
        )
        
    except Exception as e:
        raise_http_error("INGEST_FAILED", f"Failed to ingest evidence: {str(e)}")


@router.post("/evidence/verify", response_model=VerifyResponse)
def verify_evidence(req: VerifyRequest):
    """
    Verify if evidence exists in chain of custody.
    
    Searches the immutable ledger for the given SHA256 hash.
    """
    try:
        if not os.path.exists(LEDGER_PATH):
            return VerifyResponse(
                present=False,
                message="Chain of custody ledger is empty"
            )
        
        with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    if obj.get("sha256") == req.sha256:
                        return VerifyResponse(
                            present=True,
                            entry=EvidenceEntry(**obj),
                            message="Evidence found in chain of custody"
                        )
                except Exception:
                    continue
        
        return VerifyResponse(
            present=False,
            message="Evidence not found in chain of custody"
        )
        
    except Exception as e:
        raise_http_error("VERIFY_FAILED", f"Failed to verify evidence: {str(e)}")


@router.get("/evidence/{sha256}/receipt", response_model=ReceiptResponse)
def get_receipt(sha256: str):
    """
    Get cryptographically signed receipt for evidence.
    
    Returns the evidence entry with a digital signature for legal proof.
    """
    try:
        if not os.path.exists(LEDGER_PATH):
            raise_http_error("LEDGER_EMPTY", "Chain of custody ledger is empty")
        
        with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    if obj.get('sha256') == sha256:
                        # Create receipt payload
                        receipt_data = {k: obj[k] for k in ['ts','filename','size','sha256','prev_hash','record_hash'] if k in obj}
                        payload = json.dumps(receipt_data, ensure_ascii=False).encode()
                        
                        # Import crypto utils for signing
                        try:
                            from ..app.crypto_utils import sign_message
                            sig = sign_message(payload)
                        except ImportError:
                            # Fallback signature for demo
                            sig = f"demo_signature_{sha256_bytes(payload)[:16]}"
                        
                        return ReceiptResponse(
                            entry=EvidenceEntry(**obj),
                            signature=sig
                        )
                except Exception:
                    continue
        
        raise_http_error("EVIDENCE_NOT_FOUND", f"Evidence with SHA256 {sha256} not found in ledger")
        
    except HTTPException:
        raise
    except Exception as e:
        raise_http_error("RECEIPT_FAILED", f"Failed to generate receipt: {str(e)}")


@router.get("/chain/report", response_model=ChainReport)
def get_chain_report():
    """
    Get complete chain of custody report.
    
    Returns all evidence entries with integrity verification.
    """
    try:
        items = []
        if os.path.exists(LEDGER_PATH):
            with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        obj = json.loads(line)
                        items.append(EvidenceEntry(**obj))
                    except Exception:
                        continue
        
        # Basic integrity check - verify hash chain
        integrity_verified = True
        if len(items) > 1:
            for i in range(1, len(items)):
                expected_prev = items[i-1].record_hash
                actual_prev = items[i].prev_hash
                if expected_prev != actual_prev:
                    integrity_verified = False
                    break
        
        return ChainReport(
            items=items,
            count=len(items),
            integrity_verified=integrity_verified
        )
        
    except Exception as e:
        raise_http_error("REPORT_FAILED", f"Failed to generate chain report: {str(e)}")


@router.get("/evidence", response_model=PaginatedResponse)
def list_evidence(page: int = 1, size: int = 10):
    """
    List evidence entries with pagination.
    
    Returns paginated list of all evidence in chain of custody.
    """
    try:
        items = []
        if os.path.exists(LEDGER_PATH):
            with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        obj = json.loads(line)
                        items.append(obj)
                    except Exception:
                        continue
        
        # Apply pagination
        total = len(items)
        start = (page - 1) * size
        end = start + size
        paginated_items = items[start:end]
        
        return PaginatedResponse(
            items=paginated_items,
            total=total,
            page=page,
            size=size
        )
        
    except Exception as e:
        raise_http_error("LIST_FAILED", f"Failed to list evidence: {str(e)}")
