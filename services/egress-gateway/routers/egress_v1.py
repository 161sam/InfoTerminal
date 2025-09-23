"""
Egress Gateway router for v1 API.

Handles all proxy-related operations including request proxying, identity rotation,
and proxy system management.
"""

import time
import uuid
import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
from urllib.parse import urlparse
from pathlib import Path

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse

import httpx
from fake_useragent import UserAgent
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
    ProxyRequest,
    ProxyRotateRequest,
    ProxyConfigRequest,
    ProxyBulkRequest,
    ProxyFilterRequest,
    ProxyType,
    AnonymityLevel
)

from ..models.responses import (
    ProxyResponse,
    ProxyStatus,
    ProxyStatistics,
    ProxyHealthStatus,
    RotationResult,
    ProxyConfigInfo,
    BulkProxyResponse,
    ProxyCapabilities
)

logger = structlog.get_logger()
router = APIRouter()
security = HTTPBasic()
ua = UserAgent()

# Global references - will be set by main app
proxy_manager = None
tor_controller = None
request_history = []
proxy_configs = {}


def set_proxy_system(proxy_mgr, tor_ctrl):
    """Set proxy system references from main application."""
    global proxy_manager, tor_controller
    proxy_manager = proxy_mgr
    tor_controller = tor_ctrl


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify basic auth credentials for write operations."""
    import os
    correct_username = os.getenv("EGRESS_BASIC_USER", "dev")
    correct_password = os.getenv("EGRESS_BASIC_PASS", "devpass")
    
    if credentials.username != correct_username or credentials.password != correct_password:
        raise APIError(
            code=ErrorCodes.AUTHENTICATION_FAILED,
            message="Invalid credentials",
            status_code=401
        )
    return credentials.username


def sanitize_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """Remove potentially identifying headers."""
    remove_headers = [
        "X-Forwarded-For", "X-Real-IP", "X-Client-IP", "X-Forwarded-Host",
        "X-Originating-IP", "X-Remote-IP", "X-Remote-Addr", "X-Cluster-Client-IP"
    ]
    
    return {k: v for k, v in headers.items() if k not in remove_headers}


def sanitize_response_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """Remove server-identifying headers from response."""
    remove_headers = [
        "Server", "X-Powered-By", "X-AspNet-Version", "X-AspNetMvc-Version",
        "X-Drupal-Cache", "X-Generator"
    ]
    
    return {k: v for k, v in headers.items() if k not in remove_headers}


async def log_proxy_request(
    request_id: str,
    url_domain: str,
    method: str,
    status_code: int,
    proxy_used: str,
    anonymity_level: str,
    execution_time: float,
    tags: List[str] = None
):
    """Log proxy request for audit (anonymized)."""
    log_entry = {
        "request_id": request_id,
        "timestamp": datetime.utcnow(),
        "url_domain": url_domain,
        "method": method,
        "status_code": status_code,
        "proxy_used": proxy_used,
        "anonymity_level": anonymity_level,
        "execution_time": execution_time,
        "tags": tags or [],
        "service": "egress-gateway"
    }
    
    # Store in request history (limited size)
    global request_history
    request_history.append(log_entry)
    if len(request_history) > 1000:  # Keep last 1000 requests
        request_history = request_history[-1000:]
    
    logger.info("Proxy request completed", **log_entry)


# ===== PROXY REQUEST ENDPOINTS =====

@router.post(
    "/proxy/request",
    response_model=ProxyResponse,
    summary="Execute Proxy Request",
    description="Execute an HTTP request through anonymous proxy infrastructure"
)
async def proxy_request(
    request: ProxyRequest,
    background_tasks: BackgroundTasks,
    credentials: str = Depends(verify_credentials)
) -> ProxyResponse:
    """
    Execute an anonymous HTTP request through proxy infrastructure.
    
    Supports multiple proxy types (Tor, VPN, proxy, direct) with configurable
    anonymity levels and automatic identity rotation.
    """
    if not proxy_manager:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Proxy manager not available",
            status_code=503
        )
    
    request_id = f"req_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"
    start_time = time.time()
    
    logger.info(
        "Processing proxy request",
        request_id=request_id,
        url=str(request.url),
        method=request.method,
        proxy_type=request.proxy_type,
        anonymity_level=request.anonymity_level
    )
    
    try:
        # Rotate identity if requested
        if request.rotate_identity:
            await proxy_manager.rotate_identity()
            if tor_controller and tor_controller.is_available():
                await tor_controller.new_identity()
        
        # Get appropriate proxy configuration
        proxy_config = await proxy_manager.get_proxy(request.proxy_type)
        if not proxy_config and request.proxy_type != ProxyType.DIRECT:
            raise APIError(
                code=ErrorCodes.SERVICE_UNAVAILABLE,
                message=f"No {request.proxy_type} proxy available",
                status_code=503
            )
        
        # Prepare headers
        headers = request.headers or {}
        if request.sanitize_headers:
            headers = sanitize_headers(headers)
        
        # Add randomized User-Agent if not provided
        if "User-Agent" not in headers:
            headers["User-Agent"] = ua.random
        
        # Execute request through proxy
        redirects = []
        proxy_url = proxy_config.proxy_url if proxy_config else None
        
        async with httpx.AsyncClient(
            proxies=proxy_url,
            timeout=request.timeout,
            follow_redirects=request.follow_redirects
        ) as client:
            
            response = await client.request(
                method=request.method,
                url=str(request.url),
                headers=headers,
                json=request.data if request.method.upper() in ["POST", "PUT", "PATCH"] else None
            )
        
        execution_time = time.time() - start_time
        
        # Sanitize response headers
        response_headers = sanitize_response_headers(dict(response.headers))
        
        # Log request for audit
        background_tasks.add_task(
            log_proxy_request,
            request_id=request_id,
            url_domain=urlparse(str(request.url)).netloc,
            method=request.method,
            status_code=response.status_code,
            proxy_used=proxy_config.name if proxy_config else "direct",
            anonymity_level=proxy_config.anonymity_level if proxy_config else "none",
            execution_time=execution_time,
            tags=request.tags
        )
        
        return ProxyResponse(
            request_id=request_id,
            status_code=response.status_code,
            headers=response_headers,
            content=response.text,
            content_type=response.headers.get("content-type"),
            content_length=len(response.content),
            proxy_used=proxy_config.name if proxy_config else "direct",
            proxy_type=request.proxy_type,
            anonymity_level=proxy_config.anonymity_level if proxy_config else AnonymityLevel.NONE,
            execution_time=execution_time,
            target_url=str(response.url),
            method=request.method,
            redirects=redirects,
            retry_count=0,  # TODO: Implement retry logic
            tags=request.tags,
            timestamp=datetime.utcnow()
        )
        
    except httpx.RequestError as e:
        logger.error(
            "Proxy request failed",
            request_id=request_id,
            error=str(e),
            url=str(request.url)
        )
        raise APIError(
            code=ErrorCodes.EXTERNAL_SERVICE_ERROR,
            message=f"Request failed: {str(e)}",
            status_code=502,
            details={"request_id": request_id, "target_url": str(request.url)}
        )
    
    except Exception as e:
        logger.error(
            "Unexpected error in proxy request",
            request_id=request_id,
            error=str(e),
            url=str(request.url)
        )
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Internal server error",
            status_code=500,
            details={"request_id": request_id}
        )


@router.post(
    "/proxy/bulk",
    response_model=BulkProxyResponse,
    summary="Execute Bulk Proxy Requests",
    description="Execute multiple proxy requests in batch"
)
async def bulk_proxy_request(
    request: ProxyBulkRequest,
    background_tasks: BackgroundTasks,
    credentials: str = Depends(verify_credentials)
) -> BulkProxyResponse:
    """
    Execute multiple proxy requests in batch mode.
    
    Supports both sequential and parallel execution with shared session options.
    """
    if not proxy_manager:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Proxy manager not available",
            status_code=503
        )
    
    batch_id = f"batch_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"
    start_time = time.time()
    
    logger.info(
        "Processing bulk proxy request",
        batch_id=batch_id,
        total_requests=len(request.requests),
        sequential=request.sequential
    )
    
    responses = []
    successful_count = 0
    failed_count = 0
    
    try:
        if request.sequential:
            # Execute sequentially
            for i, proxy_req in enumerate(request.requests):
                try:
                    # Execute individual request (simplified version)
                    response = await proxy_request(proxy_req, background_tasks, credentials)
                    responses.append(response)
                    successful_count += 1
                except Exception as e:
                    failed_count += 1
                    if request.stop_on_error:
                        break
                    # Create error response
                    error_response = ProxyResponse(
                        request_id=f"{batch_id}_req_{i}",
                        status_code=0,
                        headers={},
                        content=f"Error: {str(e)}",
                        proxy_used="none",
                        proxy_type=proxy_req.proxy_type,
                        anonymity_level=AnonymityLevel.NONE,
                        execution_time=0.0,
                        target_url=str(proxy_req.url),
                        method=proxy_req.method,
                        tags=proxy_req.tags
                    )
                    responses.append(error_response)
        else:
            # Execute in parallel (simplified - would need proper async handling)
            tasks = []
            for proxy_req in request.requests:
                task = proxy_request(proxy_req, background_tasks, credentials)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, Exception):
                    failed_count += 1
                    # Create error response for failed requests
                    error_response = ProxyResponse(
                        request_id=f"{batch_id}_error",
                        status_code=0,
                        headers={},
                        content=f"Error: {str(result)}",
                        proxy_used="none",
                        proxy_type=ProxyType.AUTO,
                        anonymity_level=AnonymityLevel.NONE,
                        execution_time=0.0,
                        target_url="unknown",
                        method="GET"
                    )
                    responses.append(error_response)
                else:
                    successful_count += 1
                    responses.append(result)
        
        execution_time = time.time() - start_time
        
        return BulkProxyResponse(
            batch_id=batch_id,
            total_requests=len(request.requests),
            completed_requests=len(responses),
            successful_requests=successful_count,
            failed_requests=failed_count,
            responses=responses,
            execution_time=execution_time,
            batch_metadata={
                "sequential": request.sequential,
                "stop_on_error": request.stop_on_error,
                "shared_session": request.shared_session,
                "batch_name": request.batch_name
            }
        )
        
    except Exception as e:
        logger.error("Bulk proxy request failed", batch_id=batch_id, error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Bulk request processing failed",
            status_code=500,
            details={"batch_id": batch_id}
        )


# ===== PROXY STATUS & MANAGEMENT =====

@router.get(
    "/proxy/status",
    response_model=ProxyStatus,
    summary="Get Proxy Status",
    description="Get current status of proxy infrastructure"
)
async def get_proxy_status() -> ProxyStatus:
    """
    Get current proxy infrastructure status.
    
    Returns comprehensive status including Tor, VPN, and proxy availability.
    """
    try:
        # Tor status
        tor_available = tor_controller.is_available() if tor_controller else False
        tor_circuit = tor_controller.is_circuit_established() if tor_controller else False
        
        # Proxy manager status
        vpn_pools = proxy_manager.get_vpn_pools() if proxy_manager else []
        proxy_pools = proxy_manager.get_proxy_pools() if proxy_manager else []
        active_proxy = proxy_manager.get_active_proxy() if proxy_manager else "none"
        
        # Performance metrics
        request_count = len(request_history)
        successful_requests = sum(1 for req in request_history if 200 <= req.get("status_code", 0) < 400)
        success_rate = (successful_requests / request_count * 100) if request_count > 0 else 0.0
        
        avg_response_time = 0.0
        if request_history:
            response_times = [req.get("execution_time", 0.0) for req in request_history]
            avg_response_time = sum(response_times) / len(response_times)
        
        # Last rotation
        last_rotation = None
        if proxy_manager and hasattr(proxy_manager, 'get_last_rotation'):
            last_rotation_timestamp = proxy_manager.get_last_rotation()
            if last_rotation_timestamp:
                last_rotation = datetime.fromtimestamp(last_rotation_timestamp)
        
        return ProxyStatus(
            tor_available=tor_available,
            tor_circuit_established=tor_circuit,
            tor_country_exit=None,  # Would need to get from Tor controller
            vpn_available=len(vpn_pools) > 0,
            vpn_pools=vpn_pools,
            active_vpn=None,  # Would need to get from proxy manager
            proxy_pools=proxy_pools,
            active_proxy=active_proxy,
            anonymity_level=AnonymityLevel.HIGH if tor_available else AnonymityLevel.MEDIUM,
            active_proxy_type=ProxyType.TOR if tor_available else ProxyType.DIRECT,
            request_count=request_count,
            success_rate=success_rate,
            average_response_time=avg_response_time,
            last_rotation=last_rotation,
            rotation_interval=3600,  # Default 1 hour
            auto_rotation_enabled=True,
            uptime_seconds=int(time.time()),  # Simplified
            health_status="healthy",
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error("Failed to get proxy status", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve proxy status",
            status_code=500,
            details={"error": str(e)}
        )


@router.post(
    "/proxy/rotate",
    response_model=RotationResult,
    summary="Rotate Proxy Identity",
    description="Manually rotate proxy identity for enhanced anonymity"
)
async def rotate_proxy(
    request: ProxyRotateRequest,
    credentials: str = Depends(verify_credentials)
) -> RotationResult:
    """
    Manually rotate proxy/identity.
    
    Forces identity rotation for specified proxy type or all proxies.
    """
    if not proxy_manager:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Proxy manager not available",
            status_code=503
        )
    
    start_time = time.time()
    
    logger.info(
        "Manual proxy rotation requested",
        proxy_type=request.proxy_type,
        force_new_circuit=request.force_new_circuit
    )
    
    try:
        previous_proxy = proxy_manager.get_active_proxy() if proxy_manager else "unknown"
        
        # Perform rotation
        if request.proxy_type == ProxyType.TOR and tor_controller:
            if request.force_new_circuit:
                await tor_controller.new_identity()
            else:
                await tor_controller.new_identity()
        
        if proxy_manager:
            await proxy_manager.rotate_identity(request.proxy_type)
        
        new_proxy = proxy_manager.get_active_proxy() if proxy_manager else "unknown"
        rotation_time = time.time() - start_time
        
        # Log rotation
        logger.info(
            "Proxy rotation completed",
            previous_proxy=previous_proxy,
            new_proxy=new_proxy,
            rotation_time=rotation_time,
            reason=request.reason
        )
        
        return RotationResult(
            success=True,
            rotation_type=request.proxy_type.value if request.proxy_type else "all",
            previous_proxy=previous_proxy,
            new_proxy=new_proxy,
            previous_anonymity=AnonymityLevel.MEDIUM,  # Would need to track this
            new_anonymity=AnonymityLevel.HIGH,  # Would need to calculate this
            rotation_time=rotation_time,
            message="Identity rotation completed successfully",
            metadata={
                "force_new_circuit": request.force_new_circuit,
                "clear_session": request.clear_session,
                "reason": request.reason
            }
        )
        
    except Exception as e:
        logger.error("Proxy rotation failed", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message=f"Rotation failed: {str(e)}",
            status_code=500
        )


# ===== STATISTICS & MONITORING =====

@router.get(
    "/proxy/statistics",
    response_model=ProxyStatistics,
    summary="Get Proxy Statistics",
    description="Get comprehensive proxy usage statistics"
)
async def get_proxy_statistics(
    time_range: Optional[str] = Query("24h", description="Statistics time range")
) -> ProxyStatistics:
    """
    Get comprehensive proxy usage statistics.
    
    Returns detailed statistics about proxy usage, performance, and success rates.
    """
    try:
        # Calculate statistics from request history
        total_requests = len(request_history)
        successful_requests = sum(1 for req in request_history if 200 <= req.get("status_code", 0) < 400)
        failed_requests = total_requests - successful_requests
        
        # Timing statistics
        execution_times = [req.get("execution_time", 0.0) for req in request_history if req.get("execution_time")]
        avg_response_time = sum(execution_times) / len(execution_times) if execution_times else 0.0
        fastest_time = min(execution_times) if execution_times else 0.0
        slowest_time = max(execution_times) if execution_times else 0.0
        
        # Proxy type usage
        proxy_type_usage = {}
        anonymity_level_usage = {}
        status_code_distribution = {}
        
        for req in request_history:
            # Proxy type usage
            proxy_used = req.get("proxy_used", "unknown")
            proxy_type_usage[proxy_used] = proxy_type_usage.get(proxy_used, 0) + 1
            
            # Anonymity level usage
            anonymity = req.get("anonymity_level", "unknown")
            anonymity_level_usage[anonymity] = anonymity_level_usage.get(anonymity, 0) + 1
            
            # Status code distribution
            status_code = str(req.get("status_code", 0))
            status_code_distribution[status_code] = status_code_distribution.get(status_code, 0) + 1
        
        # Top domains
        domain_counts = {}
        for req in request_history:
            domain = req.get("url_domain", "unknown")
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        top_domains = [
            {"domain": domain, "count": count}
            for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
        
        return ProxyStatistics(
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            average_response_time=avg_response_time,
            fastest_response_time=fastest_time,
            slowest_response_time=slowest_time,
            proxy_type_usage=proxy_type_usage,
            anonymity_level_usage=anonymity_level_usage,
            status_code_distribution=status_code_distribution,
            top_domains=top_domains,
            error_types={},  # Would need error classification
            identity_rotations=0,  # Would need to track this
            average_rotation_interval=0.0,
            total_bytes_sent=0,  # Would need to track this
            total_bytes_received=0,  # Would need to track this
            statistics_period=time_range,
            last_updated=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error("Failed to get proxy statistics", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve statistics",
            status_code=500,
            details={"error": str(e)}
        )


@router.get(
    "/proxy/health",
    response_model=ProxyHealthStatus,
    summary="Get Proxy Health Status",
    description="Get detailed health status of proxy system components"
)
async def get_proxy_health() -> ProxyHealthStatus:
    """
    Get detailed health status of proxy system components.
    
    Returns comprehensive health information including component status and alerts.
    """
    try:
        components = {}
        connectivity_tests = {}
        alerts = []
        
        # Test proxy manager
        if proxy_manager:
            components["proxy_manager"] = {
                "status": "healthy",
                "active_proxy": getattr(proxy_manager, 'get_active_proxy', lambda: "unknown")(),
                "request_count": getattr(proxy_manager, 'get_request_count', lambda: 0)()
            }
            connectivity_tests["proxy_manager"] = True
        else:
            components["proxy_manager"] = {"status": "unhealthy", "error": "Not initialized"}
            connectivity_tests["proxy_manager"] = False
            alerts.append({
                "type": "error",
                "component": "proxy_manager",
                "message": "Proxy manager not available",
                "timestamp": datetime.utcnow()
            })
        
        # Test Tor controller
        if tor_controller:
            tor_available = getattr(tor_controller, 'is_available', lambda: False)()
            components["tor"] = {
                "status": "healthy" if tor_available else "degraded",
                "available": tor_available,
                "circuit_established": getattr(tor_controller, 'is_circuit_established', lambda: False)()
            }
            connectivity_tests["tor"] = tor_available
            
            if not tor_available:
                alerts.append({
                    "type": "warning",
                    "component": "tor",
                    "message": "Tor not available - reduced anonymity",
                    "timestamp": datetime.utcnow()
                })
        else:
            components["tor"] = {"status": "disabled"}
            connectivity_tests["tor"] = False
        
        # Performance metrics
        performance_metrics = {
            "total_requests": len(request_history),
            "success_rate": 0.0,
            "average_response_time": 0.0
        }
        
        if request_history:
            successful = sum(1 for req in request_history if 200 <= req.get("status_code", 0) < 400)
            performance_metrics["success_rate"] = successful / len(request_history) * 100
            
            response_times = [req.get("execution_time", 0.0) for req in request_history]
            performance_metrics["average_response_time"] = sum(response_times) / len(response_times)
        
        # Determine overall health
        critical_components_healthy = components.get("proxy_manager", {}).get("status") == "healthy"
        overall_health = "healthy" if critical_components_healthy else "degraded"
        
        return ProxyHealthStatus(
            overall_health=overall_health,
            components=components,
            connectivity_tests=connectivity_tests,
            performance_metrics=performance_metrics,
            resource_usage={
                "memory_usage": "N/A",  # Would need actual monitoring
                "cpu_usage": "N/A",
                "network_usage": "N/A"
            },
            active_alerts=alerts,
            last_health_check=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error("Failed to get proxy health status", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve health status",
            status_code=500,
            details={"error": str(e)}
        )


@router.get(
    "/proxy/capabilities",
    response_model=ProxyCapabilities,
    summary="Get Proxy Capabilities",
    description="Get system proxy capabilities and limits"
)
async def get_proxy_capabilities() -> ProxyCapabilities:
    """
    Get proxy system capabilities and configuration limits.
    
    Returns information about supported proxy types, limits, and features.
    """
    try:
        return ProxyCapabilities(
            supported_proxy_types=[ProxyType.TOR, ProxyType.VPN, ProxyType.PROXY, ProxyType.DIRECT, ProxyType.AUTO],
            supported_anonymity_levels=[AnonymityLevel.NONE, AnonymityLevel.LOW, AnonymityLevel.MEDIUM, AnonymityLevel.HIGH, AnonymityLevel.EXTREME],
            max_concurrent_requests=50,
            max_request_timeout=300,
            max_bulk_requests=20,
            features={
                "identity_rotation": True,
                "header_sanitization": True,
                "user_agent_rotation": True,
                "tor_support": tor_controller is not None,
                "vpn_support": proxy_manager is not None,
                "bulk_requests": True,
                "request_logging": True,
                "statistics": True,
                "health_monitoring": True
            },
            rate_limits={
                "requests_per_minute": 60,
                "requests_per_hour": 1000,
                "bulk_requests_per_hour": 50
            },
            supported_protocols=["HTTP", "HTTPS"],
            geographical_coverage=["Global", "EU", "US", "Asia-Pacific"]  # Would depend on actual proxy configuration
        )
        
    except Exception as e:
        logger.error("Failed to get proxy capabilities", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve capabilities",
            status_code=500,
            details={"error": str(e)}
        )


# ===== REQUEST HISTORY & LOGS =====

@router.get(
    "/proxy/requests",
    response_model=PaginatedResponse[Dict[str, Any]],
    summary="Get Request History",
    description="Get paginated list of proxy request history"
)
async def get_request_history(
    pagination: PaginationParams = Depends(),
    filter_request: ProxyFilterRequest = Depends()
) -> PaginatedResponse[Dict[str, Any]]:
    """
    Get paginated list of proxy request history with filtering.
    
    Returns anonymized request logs for monitoring and analysis.
    """
    try:
        # Apply filters to request history
        filtered_requests = request_history.copy()
        
        # Filter by proxy type
        if filter_request.proxy_type:
            filtered_requests = [
                req for req in filtered_requests
                if req.get("proxy_used", "").startswith(filter_request.proxy_type.value)
            ]
        
        # Filter by anonymity level
        if filter_request.anonymity_level:
            filtered_requests = [
                req for req in filtered_requests
                if req.get("anonymity_level") == filter_request.anonymity_level.value
            ]
        
        # Filter by status code
        if filter_request.status_code:
            filtered_requests = [
                req for req in filtered_requests
                if req.get("status_code") == filter_request.status_code
            ]
        
        # Filter by domain
        if filter_request.domain:
            filtered_requests = [
                req for req in filtered_requests
                if filter_request.domain.lower() in req.get("url_domain", "").lower()
            ]
        
        # Sort by timestamp (newest first)
        filtered_requests.sort(key=lambda x: x.get("timestamp", datetime.min), reverse=True)
        
        # Apply pagination
        total = len(filtered_requests)
        start = pagination.offset
        end = start + pagination.limit
        page_requests = filtered_requests[start:end]
        
        # Sanitize response (remove sensitive data)
        sanitized_requests = []
        for req in page_requests:
            sanitized_req = {
                "request_id": req.get("request_id"),
                "timestamp": req.get("timestamp"),
                "url_domain": req.get("url_domain"),
                "method": req.get("method"),
                "status_code": req.get("status_code"),
                "proxy_used": req.get("proxy_used"),
                "anonymity_level": req.get("anonymity_level"),
                "execution_time": req.get("execution_time"),
                "tags": req.get("tags", [])
            }
            sanitized_requests.append(sanitized_req)
        
        return PaginatedResponse.create(sanitized_requests, total, pagination)
        
    except Exception as e:
        logger.error("Failed to get request history", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve request history",
            status_code=500,
            details={"error": str(e)}
        )


@router.delete(
    "/proxy/requests/history",
    summary="Clear Request History",
    description="Clear proxy request history logs"
)
async def clear_request_history(
    credentials: str = Depends(verify_credentials)
) -> Dict[str, Any]:
    """
    Clear proxy request history logs.
    
    Permanently removes all stored request history for privacy.
    """
    try:
        global request_history
        cleared_count = len(request_history)
        request_history = []
        
        logger.info("Request history cleared", cleared_count=cleared_count)
        
        return {
            "message": "Request history cleared successfully",
            "cleared_requests": cleared_count,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to clear request history", error=str(e))
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to clear request history",
            status_code=500,
            details={"error": str(e)}
        )
