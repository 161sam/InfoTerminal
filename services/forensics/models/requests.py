"""
Pydantic models for Forensics Service v1.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class VerifyRequest(BaseModel):
    """Request to verify evidence exists in chain of custody."""
    sha256: str = Field(..., description="SHA256 hash of the evidence to verify", min_length=64, max_length=64)


class EvidenceEntry(BaseModel):
    """Evidence entry in the chain of custody."""
    ts: str = Field(..., description="Timestamp when evidence was ingested")
    filename: str = Field(..., description="Original filename of the evidence")
    size: int = Field(..., description="File size in bytes", ge=0)
    sha256: str = Field(..., description="SHA256 hash of the evidence")
    prev_hash: Optional[str] = Field(None, description="Hash of previous record in chain")
    record_hash: Optional[str] = Field(None, description="Hash of this record")


class IngestResponse(BaseModel):
    """Response from evidence ingestion."""
    status: str = Field(..., description="Status of the ingestion operation")
    sha256: str = Field(..., description="SHA256 hash of the ingested evidence")
    message: str = Field(default="Evidence successfully ingested into chain of custody")


class VerifyResponse(BaseModel):
    """Response from evidence verification."""
    present: bool = Field(..., description="Whether evidence is present in chain of custody")
    entry: Optional[EvidenceEntry] = Field(None, description="Evidence entry if found")
    message: Optional[str] = Field(None, description="Additional verification information")


class ReceiptResponse(BaseModel):
    """Signed receipt for evidence."""
    entry: EvidenceEntry = Field(..., description="Evidence entry details")
    signature: str = Field(..., description="Cryptographic signature of the receipt")
    message: str = Field(default="Cryptographically signed receipt")


class ChainReport(BaseModel):
    """Full chain of custody report."""
    items: List[EvidenceEntry] = Field(..., description="All evidence entries in chronological order")
    count: int = Field(..., description="Total number of evidence entries", ge=0)
    integrity_verified: bool = Field(..., description="Whether the hash chain integrity is verified")
    message: str = Field(default="Complete chain of custody ledger")
