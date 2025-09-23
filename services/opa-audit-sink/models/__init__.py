"""
OPA Audit Sink API Models

This module contains all Pydantic models for the OPA Audit Sink service API.
"""

from .requests import (
    OPADecisionLogRequest,
    OPABulkLogRequest,
    AuditQueryRequest,
    AuditRetentionRequest
)

from .responses import (
    OPADecisionLog,
    AuditIngestResult,
    AuditStatistics,
    AuditQueryResult,
    RetentionPolicyStatus,
    AuditHealthStatus
)

__all__ = [
    # Requests
    "OPADecisionLogRequest",
    "OPABulkLogRequest",
    "AuditQueryRequest", 
    "AuditRetentionRequest",
    
    # Responses
    "OPADecisionLog",
    "AuditIngestResult",
    "AuditStatistics",
    "AuditQueryResult",
    "RetentionPolicyStatus",
    "AuditHealthStatus"
]
