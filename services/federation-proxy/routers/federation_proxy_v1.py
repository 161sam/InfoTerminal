"""
Federation Proxy v1 router - Federation Management and Proxying API.

Provides comprehensive federation capabilities for InfoTerminal distributed deployments
including remote service management, intelligent request routing, health monitoring,
and security enforcement.
"""

import asyncio
import json
import logging
import os
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse

import httpx
import yaml
from fastapi import APIRouter, HTTPException, Query, Path, Depends, Request, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse

from _shared.api_standards.error_schemas import StandardError, ErrorCodes, create_error_response
from _shared.api_standards.pagination import PaginatedResponse, PaginationParams
from models.requests import (
    FederationConfig, RemoteEndpoint, ProxyRequest, ProxyResponse,
    HealthStatus, FederationMetrics, RoutingRule, SecurityPolicy,
    ConnectionPool, CircuitBreaker, LoadBalancer,
    FederationTopology, ServiceDiscovery, ConfigurationSync
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Federation Proxy"])


def get_federation_service(request: Request):
    """Dependency to get federation service from app state."""
    return request.app.state.federation_service


# Configuration Management

@router.get("/federation/config", response_model=FederationConfig)
async def get_federation_config(
    service = Depends(get_federation_service)
) -> FederationConfig:
    """
    Get current federation configuration.
    
    Returns the complete federation setup including:
    - Remote endpoint definitions
    - Routing rules and policies
    - Security configurations
    - Load balancing settings
    """
    try:
        config = await service.get_federation_config()
        return config
    except Exception as e:
        logger.error(f"Failed to get federation config: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to retrieve federation configuration",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.put("/federation/config")
async def update_federation_config(
    config: FederationConfig,
    service = Depends(get_federation_service),
    background_tasks: BackgroundTasks = None
) -> Dict[str, Any]:
    """
    Update federation configuration with validation and hot reload.
    
    Features:
    - Configuration validation before applying
    - Hot reload without service restart
    - Backup of previous configuration
    - Gradual rollout with health checking
    """
    try:
        result = await service.update_federation_config(config, background_tasks)
        return {
            "message": "Federation configuration updated successfully",
            "config_id": result.get("config_id"),
            "applied_at": datetime.utcnow().isoformat(),
            "endpoints_updated": result.get("endpoints_updated", 0),
            "validation_passed": True
        }
    except ValueError as e:
        logger.warning(f"Federation config validation failed: {e}")
        error_response = create_error_response(
            ErrorCodes.VALIDATION_ERROR,
            "Federation configuration validation failed",
            {"validation_errors": str(e)}
        )
        raise HTTPException(status_code=400, detail=error_response.dict())
    except Exception as e:
        logger.error(f"Failed to update federation config: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to update federation configuration",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.post("/federation/config/validate")
async def validate_federation_config(
    config: FederationConfig,
    service = Depends(get_federation_service)
) -> Dict[str, Any]:
    """
    Validate federation configuration without applying changes.
    
    Performs comprehensive validation including:
    - Endpoint connectivity tests
    - Security policy validation
    - Routing rule conflicts
    - Resource requirement checks
    """
    try:
        validation_result = await service.validate_federation_config(config)
        return {
            "valid": validation_result["valid"],
            "validation_details": validation_result["details"],
            "warnings": validation_result.get("warnings", []),
            "recommendations": validation_result.get("recommendations", [])
        }
    except Exception as e:
        logger.error(f"Config validation error: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Configuration validation failed",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


# Remote Endpoint Management

@router.get("/federation/endpoints", response_model=PaginatedResponse[RemoteEndpoint])
async def list_remote_endpoints(
    pagination: PaginationParams = Depends(),
    status: Optional[str] = Query(None, description="Filter by status (healthy/unhealthy/unknown)"),
    region: Optional[str] = Query(None, description="Filter by region"),
    service_type: Optional[str] = Query(None, description="Filter by service type"),
    service = Depends(get_federation_service)
) -> PaginatedResponse[RemoteEndpoint]:
    """
    List all configured remote federation endpoints with filtering.
    
    Provides detailed information about each endpoint including:
    - Current health status and metrics
    - Connection pool statistics
    - Recent error rates and response times
    - Security policy assignments
    """
    try:
        endpoints = await service.list_remote_endpoints(
            pagination=pagination,
            filters={
                "status": status,
                "region": region,
                "service_type": service_type
            }
        )
        return endpoints
    except Exception as e:
        logger.error(f"Failed to list endpoints: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to retrieve remote endpoints",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.get("/federation/endpoints/{endpoint_id}", response_model=RemoteEndpoint)
async def get_remote_endpoint(
    endpoint_id: str = Path(..., description="Remote endpoint identifier"),
    service = Depends(get_federation_service)
) -> RemoteEndpoint:
    """Get detailed information about a specific remote endpoint."""
    try:
        endpoint = await service.get_remote_endpoint(endpoint_id)
        if not endpoint:
            error_response = create_error_response(
                ErrorCodes.RESOURCE_NOT_FOUND,
                f"Remote endpoint not found: {endpoint_id}",
                {"endpoint_id": endpoint_id}
            )
            raise HTTPException(status_code=404, detail=error_response.dict())
        
        return endpoint
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get endpoint {endpoint_id}: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to retrieve remote endpoint",
            {"endpoint_id": endpoint_id, "error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.post("/federation/endpoints", response_model=RemoteEndpoint)
async def create_remote_endpoint(
    endpoint: RemoteEndpoint,
    service = Depends(get_federation_service),
    background_tasks: BackgroundTasks = None
) -> RemoteEndpoint:
    """
    Register a new remote federation endpoint.
    
    Automatically performs:
    - Connectivity validation
    - Security handshake
    - Service discovery
    - Initial health checks
    """
    try:
        created_endpoint = await service.create_remote_endpoint(endpoint, background_tasks)
        return created_endpoint
    except ValueError as e:
        logger.warning(f"Endpoint validation failed: {e}")
        error_response = create_error_response(
            ErrorCodes.VALIDATION_ERROR,
            "Remote endpoint validation failed",
            {"validation_errors": str(e)}
        )
        raise HTTPException(status_code=400, detail=error_response.dict())
    except Exception as e:
        logger.error(f"Failed to create endpoint: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to create remote endpoint",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.put("/federation/endpoints/{endpoint_id}", response_model=RemoteEndpoint)
async def update_remote_endpoint(
    endpoint_id: str = Path(..., description="Remote endpoint identifier"),
    endpoint_update: RemoteEndpoint = ...,
    service = Depends(get_federation_service)
) -> RemoteEndpoint:
    """Update remote endpoint configuration with validation."""
    try:
        updated_endpoint = await service.update_remote_endpoint(endpoint_id, endpoint_update)
        if not updated_endpoint:
            error_response = create_error_response(
                ErrorCodes.RESOURCE_NOT_FOUND,
                f"Remote endpoint not found: {endpoint_id}",
                {"endpoint_id": endpoint_id}
            )
            raise HTTPException(status_code=404, detail=error_response.dict())
        
        return updated_endpoint
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Endpoint update validation failed: {e}")
        error_response = create_error_response(
            ErrorCodes.VALIDATION_ERROR,
            "Endpoint update validation failed",
            {"validation_errors": str(e)}
        )
        raise HTTPException(status_code=400, detail=error_response.dict())
    except Exception as e:
        logger.error(f"Failed to update endpoint {endpoint_id}: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to update remote endpoint",
            {"endpoint_id": endpoint_id, "error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.delete("/federation/endpoints/{endpoint_id}")
async def delete_remote_endpoint(
    endpoint_id: str = Path(..., description="Remote endpoint identifier"),
    force: bool = Query(False, description="Force deletion even if endpoint is healthy"),
    service = Depends(get_federation_service)
) -> Dict[str, Any]:
    """
    Remove a remote federation endpoint.
    
    Safely removes endpoint with:
    - Graceful connection draining
    - Request routing updates
    - Configuration cleanup
    """
    try:
        success = await service.delete_remote_endpoint(endpoint_id, force=force)
        if not success:
            error_response = create_error_response(
                ErrorCodes.RESOURCE_NOT_FOUND,
                f"Remote endpoint not found: {endpoint_id}",
                {"endpoint_id": endpoint_id}
            )
            raise HTTPException(status_code=404, detail=error_response.dict())
        
        return {
            "endpoint_id": endpoint_id,
            "message": "Remote endpoint deleted successfully",
            "deleted_at": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete endpoint {endpoint_id}: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to delete remote endpoint",
            {"endpoint_id": endpoint_id, "error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


# Request Proxying

@router.api_route("/federation/proxy/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def proxy_request(
    request: Request,
    path: str = Path(..., description="Target path to proxy"),
    target_endpoint: Optional[str] = Query(None, description="Specific endpoint to target"),
    timeout: Optional[int] = Query(30, description="Request timeout in seconds"),
    service = Depends(get_federation_service)
):
    """
    Proxy HTTP requests to federated remote endpoints.
    
    Features:
    - Intelligent endpoint selection
    - Load balancing across healthy endpoints
    - Automatic failover and retry
    - Request/response transformation
    - Authentication token propagation
    """
    try:
        # Prepare proxy request
        proxy_req = ProxyRequest(
            method=request.method,
            path=path,
            headers=dict(request.headers),
            query_params=dict(request.query_params),
            body=await request.body() if request.method in ["POST", "PUT", "PATCH"] else None,
            target_endpoint=target_endpoint,
            timeout=timeout
        )
        
        # Execute proxy request
        proxy_response = await service.proxy_request(proxy_req)
        
        # Return response
        return JSONResponse(
            content=proxy_response.body,
            status_code=proxy_response.status_code,
            headers=proxy_response.headers
        )
        
    except httpx.TimeoutException:
        error_response = create_error_response(
            "PROXY_TIMEOUT",
            f"Request to {path} timed out after {timeout} seconds",
            {"path": path, "timeout": timeout}
        )
        raise HTTPException(status_code=504, detail=error_response.dict())
    except httpx.ConnectError:
        error_response = create_error_response(
            "PROXY_CONNECTION_ERROR",
            f"Failed to connect to remote endpoint for {path}",
            {"path": path}
        )
        raise HTTPException(status_code=502, detail=error_response.dict())
    except Exception as e:
        logger.error(f"Proxy request failed for {path}: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Proxy request failed",
            {"path": path, "error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


# Health Monitoring

@router.get("/federation/health", response_model=List[HealthStatus])
async def get_federation_health(
    include_details: bool = Query(True, description="Include detailed health information"),
    service = Depends(get_federation_service)
) -> List[HealthStatus]:
    """
    Get comprehensive health status of all federated endpoints.
    
    Provides real-time health information including:
    - Connection status and response times
    - Error rates and success rates
    - Resource utilization metrics
    - Security handshake status
    """
    try:
        health_statuses = await service.get_federation_health(include_details=include_details)
        return health_statuses
    except Exception as e:
        logger.error(f"Failed to get federation health: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to retrieve federation health status",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.post("/federation/endpoints/{endpoint_id}/health-check")
async def trigger_health_check(
    endpoint_id: str = Path(..., description="Remote endpoint identifier"),
    force: bool = Query(False, description="Force immediate health check"),
    service = Depends(get_federation_service)
) -> HealthStatus:
    """Trigger an immediate health check for a specific endpoint."""
    try:
        health_status = await service.trigger_health_check(endpoint_id, force=force)
        if not health_status:
            error_response = create_error_response(
                ErrorCodes.RESOURCE_NOT_FOUND,
                f"Remote endpoint not found: {endpoint_id}",
                {"endpoint_id": endpoint_id}
            )
            raise HTTPException(status_code=404, detail=error_response.dict())
        
        return health_status
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Health check failed for {endpoint_id}: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Health check failed",
            {"endpoint_id": endpoint_id, "error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


# Metrics and Analytics

@router.get("/federation/metrics", response_model=FederationMetrics)
async def get_federation_metrics(
    time_range: str = Query("1h", description="Time range for metrics (1h, 24h, 7d, 30d)"),
    endpoint_id: Optional[str] = Query(None, description="Filter by specific endpoint"),
    service = Depends(get_federation_service)
) -> FederationMetrics:
    """
    Get comprehensive federation performance metrics.
    
    Includes:
    - Request volume and response time statistics
    - Error rates and success rates by endpoint
    - Load balancing efficiency metrics
    - Security event statistics
    """
    try:
        metrics = await service.get_federation_metrics(
            time_range=time_range,
            endpoint_id=endpoint_id
        )
        return metrics
    except Exception as e:
        logger.error(f"Failed to get federation metrics: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to retrieve federation metrics",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


# Topology and Discovery

@router.get("/federation/topology", response_model=FederationTopology)
async def get_federation_topology(
    include_inactive: bool = Query(False, description="Include inactive endpoints"),
    service = Depends(get_federation_service)
) -> FederationTopology:
    """
    Get current federation topology and service discovery information.
    
    Provides:
    - Network topology visualization data
    - Service discovery status
    - Inter-service dependencies
    - Regional distribution
    """
    try:
        topology = await service.get_federation_topology(include_inactive=include_inactive)
        return topology
    except Exception as e:
        logger.error(f"Failed to get federation topology: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to retrieve federation topology",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.post("/federation/discovery/refresh")
async def refresh_service_discovery(
    service = Depends(get_federation_service),
    background_tasks: BackgroundTasks = None
) -> Dict[str, Any]:
    """
    Trigger a refresh of service discovery across all federated endpoints.
    
    Performs:
    - Service capability detection
    - Endpoint health verification
    - Configuration synchronization
    - Topology map updates
    """
    try:
        discovery_result = await service.refresh_service_discovery(background_tasks)
        return {
            "message": "Service discovery refresh initiated",
            "discovery_id": discovery_result.get("discovery_id"),
            "endpoints_discovered": discovery_result.get("endpoints_discovered", 0),
            "services_updated": discovery_result.get("services_updated", 0),
            "refresh_started_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Service discovery refresh failed: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Service discovery refresh failed",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


# Security and Policies

@router.get("/federation/security/policies", response_model=List[SecurityPolicy])
async def list_security_policies(
    service = Depends(get_federation_service)
) -> List[SecurityPolicy]:
    """List all federation security policies and their assignments."""
    try:
        policies = await service.list_security_policies()
        return policies
    except Exception as e:
        logger.error(f"Failed to list security policies: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to retrieve security policies",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.post("/federation/security/policies", response_model=SecurityPolicy)
async def create_security_policy(
    policy: SecurityPolicy,
    service = Depends(get_federation_service)
) -> SecurityPolicy:
    """Create a new federation security policy."""
    try:
        created_policy = await service.create_security_policy(policy)
        return created_policy
    except ValueError as e:
        logger.warning(f"Security policy validation failed: {e}")
        error_response = create_error_response(
            ErrorCodes.VALIDATION_ERROR,
            "Security policy validation failed",
            {"validation_errors": str(e)}
        )
        raise HTTPException(status_code=400, detail=error_response.dict())
    except Exception as e:
        logger.error(f"Failed to create security policy: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to create security policy",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


# Load Balancing Configuration

@router.get("/federation/load-balancer", response_model=LoadBalancer)
async def get_load_balancer_config(
    service = Depends(get_federation_service)
) -> LoadBalancer:
    """Get current load balancing configuration and status."""
    try:
        lb_config = await service.get_load_balancer_config()
        return lb_config
    except Exception as e:
        logger.error(f"Failed to get load balancer config: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to retrieve load balancer configuration",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.put("/federation/load-balancer")
async def update_load_balancer_config(
    lb_config: LoadBalancer,
    service = Depends(get_federation_service)
) -> Dict[str, Any]:
    """Update load balancing configuration."""
    try:
        result = await service.update_load_balancer_config(lb_config)
        return {
            "message": "Load balancer configuration updated successfully",
            "config_applied_at": datetime.utcnow().isoformat(),
            "endpoints_affected": result.get("endpoints_affected", 0)
        }
    except ValueError as e:
        logger.warning(f"Load balancer config validation failed: {e}")
        error_response = create_error_response(
            ErrorCodes.VALIDATION_ERROR,
            "Load balancer configuration validation failed",
            {"validation_errors": str(e)}
        )
        raise HTTPException(status_code=400, detail=error_response.dict())
    except Exception as e:
        logger.error(f"Failed to update load balancer config: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to update load balancer configuration",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())
