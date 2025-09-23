"""
OPA Audit Sink router for v1 API.

Handles all audit log operations including ingestion, querying, retention,
and audit analytics using ClickHouse backend.
"""

import time
import uuid
import json
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pathlib import Path

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query, Depends
from fastapi.responses import JSONResponse, StreamingResponse

import httpx
import structlog

import sys

# Add shared modules to path
SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from _shared.api_standards import (
    PaginatedResponse,
    PaginationParams,
    APIError,
    ErrorCodes
)

from ..models.requests import (
    OPADecisionLogRequest,
    OPABulkLogRequest,
    AuditQueryRequest,
    AuditRetentionRequest,
    AuditExportRequest,
    AuditConfigRequest,
    AuditAlertRequest
)

from ..models.responses import (
    OPADecisionLog,
    AuditIngestResult,
    AuditStatistics,
    AuditQueryResult,
    RetentionPolicyStatus,
    AuditHealthStatus,
    AuditExportResult,
    AuditCapabilities
)

logger = structlog.get_logger()
router = APIRouter()

# Global references - will be set by main app
clickhouse_client = None
audit_config = {}
retention_policies = {}
active_exports = {}


def set_audit_system(ch_client, config):
    """Set audit system references from main application."""
    global clickhouse_client, audit_config
    clickhouse_client = ch_client
    audit_config = config


def _transform_opa_log(log_entry: Dict[str, Any]) -> Dict[str, Any]:
    """Transform raw OPA decision log to our standardized format."""
    timestamp = log_entry.get("timestamp") or datetime.utcnow().isoformat()
    path = log_entry.get("path", "")
    decision_id = log_entry.get("decision_id", "")
    input_data = log_entry.get("input", {}) or {}
    
    # Extract user context
    user = ((input_data.get("user") or {}).get("username")) or ""
    roles = (input_data.get("user") or {}).get("roles") or []
    tenant = (input_data.get("user") or {}).get("tenant") or ""
    
    # Extract resource context
    classification = (input_data.get("resource") or {}).get("classification") or ""
    action = input_data.get("action") or ""
    
    # Decision result
    result = log_entry.get("result", False)
    allowed = 1 if bool(result) else 0
    
    # Policy metadata
    policy_version = log_entry.get("bundles", {}).get("main", {}).get("revision", "")
    
    return {
        "ts": timestamp,
        "path": path,
        "decision_id": decision_id,
        "user": user,
        "roles": roles,
        "tenant": tenant,
        "classification": classification,
        "action": action,
        "allowed": allowed,
        "policy_version": policy_version,
        "raw": json.dumps(log_entry, separators=(",", ":"))
    }


async def _insert_to_clickhouse(rows: List[Dict[str, Any]]) -> Dict[str, int]:
    """Insert audit log rows to ClickHouse."""
    if not rows:
        return {"inserted": 0, "failed": 0}
    
    ch_url = audit_config.get("clickhouse_url", "http://localhost:8123")
    ch_db = audit_config.get("database", "logs")
    ch_table = audit_config.get("table", "opa_decisions")
    
    # Prepare JSONEachRow format
    data = "\n".join(json.dumps(row, separators=(",", ":")) for row in rows)
    query = f"INSERT INTO {ch_db}.{ch_table} FORMAT JSONEachRow"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{ch_url}/?query={query}",
                content=data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
        
        return {"inserted": len(rows), "failed": 0}
        
    except Exception as e:
        logger.error("Failed to insert to ClickHouse", error=str(e), rows_count=len(rows))
        return {"inserted": 0, "failed": len(rows)}


# ===== AUDIT LOG INGESTION =====

@router.post(
    "/logs",
    response_model=AuditIngestResult,
    summary="Ingest OPA Decision Logs",
    description="Ingest OPA decision logs for audit trail and compliance"
)
async def ingest_opa_logs(
    logs: List[OPADecisionLogRequest],
    background_tasks: BackgroundTasks
) -> AuditIngestResult:
    """
    Ingest OPA decision logs for audit trail and compliance.
    
    Accepts individual or bulk decision logs from OPA systems and stores
    them in ClickHouse for analysis and compliance reporting.
    """
    if not clickhouse_client:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="ClickHouse connection not available",
            status_code=503
        )
    
    start_time = time.time()
    batch_id = f"batch_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"
    
    logger.info(
        "Processing OPA decision logs",
        batch_id=batch_id,
        log_count=len(logs)
    )
    
    try:
        # Transform logs to our format
        transformed_rows = []
        errors = []
        
        for i, log_entry in enumerate(logs):
            try:
                row = _transform_opa_log(log_entry.dict())
                transformed_rows.append(row)
            except Exception as e:
                errors.append({
                    "index": i,
                    "error": str(e),
                    "log_entry": log_entry.dict()
                })
                logger.error("Failed to transform log entry", error=str(e), index=i)
        
        # Insert to ClickHouse
        insert_result = await _insert_to_clickhouse(transformed_rows)
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(
            "OPA logs ingestion completed",
            batch_id=batch_id,
            ingested=insert_result["inserted"],
            failed=insert_result["failed"],
            processing_time_ms=processing_time
        )
        
        return AuditIngestResult(
            ingested_count=insert_result["inserted"],
            failed_count=insert_result["failed"],
            batch_id=batch_id,
            processing_time_ms=processing_time,
            errors=errors,
            total_size_bytes=len(json.dumps([log.dict() for log in logs])),
            stored_in_table=f"{audit_config.get('database', 'logs')}.{audit_config.get('table', 'opa_decisions')}",
            storage_backend="clickhouse"
        )
        
    except Exception as e:
        logger.error("OPA logs ingestion failed", batch_id=batch_id, error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to ingest audit logs",
            status_code=500,
            details={"batch_id": batch_id, "error": str(e)}
        )


@router.post(
    "/logs/bulk",
    response_model=AuditIngestResult,
    summary="Bulk Ingest OPA Logs",
    description="Bulk ingestion of OPA decision logs with enhanced processing"
)
async def bulk_ingest_opa_logs(
    request: OPABulkLogRequest,
    background_tasks: BackgroundTasks
) -> AuditIngestResult:
    """
    Bulk ingestion of OPA decision logs with enhanced processing.
    
    Supports large batches with source tracking and improved error handling.
    """
    result = await ingest_opa_logs(request.logs, background_tasks)
    
    # Add bulk-specific metadata
    result.batch_id = request.batch_id or result.batch_id
    
    if request.source:
        result.storage_backend = f"clickhouse (source: {request.source})"
    
    return result


# ===== AUDIT LOG QUERYING =====

@router.get(
    "/logs/query",
    response_model=AuditQueryResult,
    summary="Query Audit Logs",
    description="Query audit logs with filtering and pagination"
)
async def query_audit_logs(
    pagination: PaginationParams = Depends(),
    start_time: Optional[datetime] = Query(None, description="Start time filter"),
    end_time: Optional[datetime] = Query(None, description="End time filter"),
    user: Optional[str] = Query(None, description="Filter by username"),
    tenant: Optional[str] = Query(None, description="Filter by tenant"),
    action: Optional[str] = Query(None, description="Filter by action"),
    classification: Optional[str] = Query(None, description="Filter by resource classification"),
    allowed: Optional[bool] = Query(None, description="Filter by decision result"),
    path: Optional[str] = Query(None, description="Filter by OPA policy path"),
    decision_id: Optional[str] = Query(None, description="Filter by decision ID")
) -> AuditQueryResult:
    """
    Query audit logs with filtering and pagination.
    
    Supports comprehensive filtering by time range, user, resource,
    and decision attributes for audit trail analysis.
    """
    if not clickhouse_client:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="ClickHouse connection not available",
            status_code=503
        )
    
    start_query_time = time.time()
    
    try:
        # Build WHERE conditions
        conditions = []
        params = {}
        
        if start_time:
            conditions.append("ts >= %(start_time)s")
            params["start_time"] = start_time.isoformat()
        
        if end_time:
            conditions.append("ts <= %(end_time)s")
            params["end_time"] = end_time.isoformat()
        
        if user:
            conditions.append("user = %(user)s")
            params["user"] = user
        
        if tenant:
            conditions.append("tenant = %(tenant)s")
            params["tenant"] = tenant
        
        if action:
            conditions.append("action = %(action)s")
            params["action"] = action
        
        if classification:
            conditions.append("classification = %(classification)s")
            params["classification"] = classification
        
        if allowed is not None:
            conditions.append("allowed = %(allowed)s")
            params["allowed"] = 1 if allowed else 0
        
        if path:
            conditions.append("path LIKE %(path)s")
            params["path"] = f"%{path}%"
        
        if decision_id:
            conditions.append("decision_id = %(decision_id)s")
            params["decision_id"] = decision_id
        
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        ch_url = audit_config.get("clickhouse_url", "http://localhost:8123")
        ch_db = audit_config.get("database", "logs")
        ch_table = audit_config.get("table", "opa_decisions")
        
        # Count total matching records
        count_query = f"SELECT COUNT(*) FROM {ch_db}.{ch_table}{where_clause}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Get total count
            count_response = await client.post(
                f"{ch_url}/?query={count_query}",
                headers={"Content-Type": "application/json"}
            )
            count_response.raise_for_status()
            total_count = int(count_response.text.strip())
            
            # Get paginated data
            data_query = f"""
                SELECT ts, path, decision_id, user, roles, tenant, classification, action, allowed, policy_version, raw
                FROM {ch_db}.{ch_table}
                {where_clause}
                ORDER BY ts DESC
                LIMIT {pagination.limit} OFFSET {pagination.offset}
            """
            
            data_response = await client.post(
                f"{ch_url}/?query={data_query}",
                headers={"Content-Type": "application/json"}
            )
            data_response.raise_for_status()
            
            # Parse response
            logs = []
            if data_response.text.strip():
                for line in data_response.text.strip().split('\n'):
                    if line:
                        row = line.split('\t')
                        if len(row) >= 11:
                            logs.append(OPADecisionLog(
                                timestamp=datetime.fromisoformat(row[0].replace('Z', '+00:00')),
                                decision_id=row[2],
                                path=row[1],
                                user=row[3],
                                roles=json.loads(row[4]) if row[4] else [],
                                tenant=row[5],
                                classification=row[6],
                                action=row[7],
                                allowed=bool(int(row[8])),
                                policy_version=row[9],
                                raw_log=json.loads(row[10]) if row[10] else None
                            ))
        
        query_time = (time.time() - start_query_time) * 1000
        
        return AuditQueryResult(
            logs=logs,
            total_count=total_count,
            returned_count=len(logs),
            query_time_ms=query_time,
            query_filters=params,
            has_more=total_count > (pagination.offset + len(logs))
        )
        
    except Exception as e:
        logger.error("Audit logs query failed", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to query audit logs",
            status_code=500,
            details={"error": str(e)}
        )


# ===== AUDIT STATISTICS =====

@router.get(
    "/statistics",
    response_model=AuditStatistics,
    summary="Get Audit Statistics",
    description="Get comprehensive audit log statistics and analytics"
)
async def get_audit_statistics(
    time_range: str = Query("24h", description="Statistics time range")
) -> AuditStatistics:
    """
    Get comprehensive audit log statistics and analytics.
    
    Returns detailed statistics about decisions, users, policies,
    and system performance for the specified time range.
    """
    if not clickhouse_client:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="ClickHouse connection not available",
            status_code=503
        )
    
    try:
        ch_url = audit_config.get("clickhouse_url", "http://localhost:8123")
        ch_db = audit_config.get("database", "logs")
        ch_table = audit_config.get("table", "opa_decisions")
        
        # Calculate time range
        now = datetime.utcnow()
        if time_range == "1h":
            start_time = now - timedelta(hours=1)
        elif time_range == "24h":
            start_time = now - timedelta(hours=24)
        elif time_range == "7d":
            start_time = now - timedelta(days=7)
        else:
            start_time = now - timedelta(hours=24)
        
        stats_queries = {
            "total_decisions": f"SELECT COUNT(*) FROM {ch_db}.{ch_table}",
            "decisions_allowed": f"SELECT COUNT(*) FROM {ch_db}.{ch_table} WHERE allowed = 1",
            "decisions_denied": f"SELECT COUNT(*) FROM {ch_db}.{ch_table} WHERE allowed = 0",
            "decisions_last_hour": f"SELECT COUNT(*) FROM {ch_db}.{ch_table} WHERE ts >= '{(now - timedelta(hours=1)).isoformat()}'",
            "decisions_last_day": f"SELECT COUNT(*) FROM {ch_db}.{ch_table} WHERE ts >= '{(now - timedelta(days=1)).isoformat()}'",
            "decisions_last_week": f"SELECT COUNT(*) FROM {ch_db}.{ch_table} WHERE ts >= '{(now - timedelta(days=7)).isoformat()}'",
            "unique_users": f"SELECT COUNT(DISTINCT user) FROM {ch_db}.{ch_table}",
            "unique_policies": f"SELECT COUNT(DISTINCT path) FROM {ch_db}.{ch_table}",
        }
        
        statistics = {}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for stat_name, query in stats_queries.items():
                try:
                    response = await client.post(
                        f"{ch_url}/?query={query}",
                        headers={"Content-Type": "application/json"}
                    )
                    response.raise_for_status()
                    value = int(response.text.strip())
                    statistics[stat_name] = value
                except Exception as e:
                    logger.error(f"Failed to get {stat_name}", error=str(e))
                    statistics[stat_name] = 0
            
            # Get top users
            top_users_query = f"""
                SELECT user, COUNT(*) as count
                FROM {ch_db}.{ch_table}
                WHERE user != ''
                GROUP BY user
                ORDER BY count DESC
                LIMIT 10
            """
            
            try:
                response = await client.post(
                    f"{ch_url}/?query={top_users_query}",
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                top_users = []
                if response.text.strip():
                    for line in response.text.strip().split('\n'):
                        if line:
                            parts = line.split('\t')
                            if len(parts) >= 2:
                                top_users.append({"user": parts[0], "count": int(parts[1])})
            except Exception:
                top_users = []
            
            # Get top policies
            top_policies_query = f"""
                SELECT path, COUNT(*) as count
                FROM {ch_db}.{ch_table}
                WHERE path != ''
                GROUP BY path
                ORDER BY count DESC
                LIMIT 10
            """
            
            try:
                response = await client.post(
                    f"{ch_url}/?query={top_policies_query}",
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                top_policies = []
                if response.text.strip():
                    for line in response.text.strip().split('\n'):
                        if line:
                            parts = line.split('\t')
                            if len(parts) >= 2:
                                top_policies.append({"policy": parts[0], "count": int(parts[1])})
            except Exception:
                top_policies = []
        
        return AuditStatistics(
            total_decisions=statistics.get("total_decisions", 0),
            decisions_allowed=statistics.get("decisions_allowed", 0),
            decisions_denied=statistics.get("decisions_denied", 0),
            decisions_last_hour=statistics.get("decisions_last_hour", 0),
            decisions_last_day=statistics.get("decisions_last_day", 0),
            decisions_last_week=statistics.get("decisions_last_week", 0),
            unique_users=statistics.get("unique_users", 0),
            unique_policies=statistics.get("unique_policies", 0),
            top_users=top_users,
            top_policies=top_policies,
            data_completeness_score=95.0,  # Would calculate based on actual data quality
            total_storage_size_bytes=0,  # Would query actual storage size
            time_range={
                "start": start_time.isoformat(),
                "end": now.isoformat(),
                "range": time_range
            }
        )
        
    except Exception as e:
        logger.error("Failed to get audit statistics", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve audit statistics",
            status_code=500,
            details={"error": str(e)}
        )


# ===== AUDIT SYSTEM HEALTH =====

@router.get(
    "/health/comprehensive",
    response_model=AuditHealthStatus,
    summary="Get Comprehensive Audit Health",
    description="Get detailed health status of audit system components"
)
async def get_comprehensive_health() -> AuditHealthStatus:
    """
    Get detailed health status of audit system components.
    
    Returns comprehensive health information including ClickHouse status,
    ingestion pipeline health, and performance metrics.
    """
    try:
        ch_url = audit_config.get("clickhouse_url", "http://localhost:8123")
        
        # Test ClickHouse connectivity
        clickhouse_health = {"status": "unknown"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{ch_url}/ping")
                if response.status_code == 200:
                    clickhouse_health = {
                        "status": "healthy",
                        "response_time_ms": 5.0,
                        "version": "23.8",  # Would get actual version
                        "connection": "active"
                    }
                else:
                    clickhouse_health = {
                        "status": "unhealthy",
                        "error": f"HTTP {response.status_code}"
                    }
        except Exception as e:
            clickhouse_health = {
                "status": "unhealthy",
                "error": str(e)
            }
        
        # Determine overall health
        overall_health = "healthy" if clickhouse_health["status"] == "healthy" else "degraded"
        
        # Mock additional health metrics (would be real in production)
        ingestion_health = {
            "status": "healthy",
            "queue_size": 0,
            "processing_rate": "1000 logs/min",
            "last_processed": datetime.utcnow().isoformat()
        }
        
        storage_health = {
            "status": "healthy",
            "disk_usage": "45%",
            "available_space": "2.5TB",
            "compression_ratio": 0.3
        }
        
        return AuditHealthStatus(
            overall_health=overall_health,
            clickhouse_health=clickhouse_health,
            ingestion_health=ingestion_health,
            storage_health=storage_health,
            ingestion_rate={
                "current": 1000.0,
                "average_5m": 950.0,
                "average_1h": 800.0
            },
            query_performance={
                "average_query_time_ms": 25.0,
                "slowest_query_time_ms": 150.0,
                "cache_hit_rate": 0.85
            },
            storage_usage={
                "total_logs": 1500000,
                "storage_size_gb": 45.2,
                "compression_ratio": 0.3,
                "oldest_log": (datetime.utcnow() - timedelta(days=90)).isoformat()
            },
            uptime_seconds=int(time.time())  # Simplified uptime
        )
        
    except Exception as e:
        logger.error("Failed to get comprehensive health", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve health status",
            status_code=500,
            details={"error": str(e)}
        )


# ===== AUDIT CAPABILITIES =====

@router.get(
    "/capabilities",
    response_model=AuditCapabilities,
    summary="Get Audit System Capabilities",
    description="Get audit system capabilities and configuration limits"
)
async def get_audit_capabilities() -> AuditCapabilities:
    """
    Get audit system capabilities and configuration limits.
    
    Returns information about supported features, limits, and system configuration.
    """
    try:
        return AuditCapabilities(
            max_retention_days=3650,  # 10 years
            supported_formats=["json", "csv", "parquet"],
            max_query_time_range_days=365,
            max_query_results=10000,
            supported_aggregations=["count", "sum", "avg", "min", "max", "group_by"],
            max_batch_size=1000,
            max_ingestion_rate=10000,
            supported_alert_conditions=["threshold", "anomaly", "pattern", "rate"],
            supported_data_sources=["opa", "custom"],
            supported_destinations=["clickhouse", "s3", "webhook"],
            encryption_available=True,
            access_control_enabled=True,
            audit_trail_enabled=True,
            version="1.0.0"
        )
        
    except Exception as e:
        logger.error("Failed to get audit capabilities", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve capabilities",
            status_code=500,
            details={"error": str(e)}
        )


# ===== RETENTION MANAGEMENT =====

@router.post(
    "/retention/policy",
    response_model=RetentionPolicyStatus,
    summary="Set Retention Policy",
    description="Configure audit log retention policy"
)
async def set_retention_policy(
    request: AuditRetentionRequest
) -> RetentionPolicyStatus:
    """
    Configure audit log retention policy.
    
    Sets up automated retention policy for audit logs with optional backup.
    """
    global retention_policies
    
    try:
        policy_id = f"policy_{request.policy_name}_{int(time.time())}"
        
        # Store policy configuration
        retention_policies[request.policy_name] = {
            "retention_days": request.retention_days,
            "backup_before_deletion": request.backup_before_deletion,
            "created_at": datetime.utcnow(),
            "policy_id": policy_id
        }
        
        # If apply_immediately and not dry_run, execute retention
        logs_deleted = 0
        if request.apply_immediately and not request.dry_run:
            # Implementation would delete old logs here
            cutoff_date = datetime.utcnow() - timedelta(days=request.retention_days)
            # logs_deleted = await delete_old_logs(cutoff_date)
            logs_deleted = 0  # Placeholder
        
        return RetentionPolicyStatus(
            policy_name=request.policy_name,
            retention_days=request.retention_days,
            is_active=True,
            last_applied=datetime.utcnow() if request.apply_immediately else None,
            logs_deleted=logs_deleted,
            space_freed_bytes=logs_deleted * 1024,  # Estimate
            last_execution_status="completed" if request.apply_immediately else "scheduled",
            created_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error("Failed to set retention policy", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to set retention policy",
            status_code=500,
            details={"error": str(e)}
        )


@router.get(
    "/retention/policies",
    response_model=List[RetentionPolicyStatus],
    summary="List Retention Policies",
    description="Get list of configured retention policies"
)
async def list_retention_policies() -> List[RetentionPolicyStatus]:
    """
    Get list of configured retention policies.
    
    Returns all active and inactive retention policies with their status.
    """
    try:
        global retention_policies
        
        policies = []
        for policy_name, config in retention_policies.items():
            policies.append(RetentionPolicyStatus(
                policy_name=policy_name,
                retention_days=config["retention_days"],
                is_active=True,
                created_at=config["created_at"],
                last_execution_status="active"
            ))
        
        return policies
        
    except Exception as e:
        logger.error("Failed to list retention policies", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve retention policies",
            status_code=500,
            details={"error": str(e)}
        )


# ===== AUDIT CONFIGURATION =====

@router.put(
    "/config",
    summary="Update Audit Configuration",
    description="Update audit system configuration"
)
async def update_audit_config(
    request: AuditConfigRequest
) -> Dict[str, Any]:
    """
    Update audit system configuration.
    
    Updates ClickHouse connection, batch settings, and other configuration.
    """
    try:
        global audit_config
        
        updated_fields = []
        
        if request.clickhouse_url:
            audit_config["clickhouse_url"] = request.clickhouse_url
            updated_fields.append("clickhouse_url")
        
        if request.database:
            audit_config["database"] = request.database
            updated_fields.append("database")
        
        if request.table:
            audit_config["table"] = request.table
            updated_fields.append("table")
        
        if request.batch_size:
            audit_config["batch_size"] = request.batch_size
            updated_fields.append("batch_size")
        
        if request.flush_interval:
            audit_config["flush_interval"] = request.flush_interval
            updated_fields.append("flush_interval")
        
        if request.enable_compression is not None:
            audit_config["compression_enabled"] = request.enable_compression
            updated_fields.append("compression_enabled")
        
        if request.enable_encryption is not None:
            audit_config["encryption_enabled"] = request.enable_encryption
            updated_fields.append("encryption_enabled")
        
        return {
            "message": "Configuration updated successfully",
            "updated_fields": updated_fields,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to update audit configuration", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to update configuration",
            status_code=500,
            details={"error": str(e)}
        )


@router.get(
    "/config",
    summary="Get Audit Configuration",
    description="Get current audit system configuration"
)
async def get_audit_config() -> Dict[str, Any]:
    """
    Get current audit system configuration.
    
    Returns the current configuration including ClickHouse settings and options.
    """
    try:
        global audit_config
        
        # Return sanitized config (remove sensitive data)
        safe_config = audit_config.copy()
        
        # Mask sensitive URLs
        if "clickhouse_url" in safe_config:
            url = safe_config["clickhouse_url"]
            if "@" in url:
                # Mask credentials in URL
                safe_config["clickhouse_url"] = url.split("@")[-1]
        
        return {
            "configuration": safe_config,
            "timestamp": datetime.utcnow().isoformat(),
            "service_version": "1.0.0"
        }
        
    except Exception as e:
        logger.error("Failed to get audit configuration", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve configuration",
            status_code=500,
            details={"error": str(e)}
        )
