"""
InfoTerminal Egress Gateway Service
Provides anonymous/secure outbound connections for OSINT research.
"""

import asyncio
import os
import time
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse
import json
import logging

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, HttpUrl
import httpx
from fake_useragent import UserAgent
import structlog

from proxy import ProxyManager, ProxyType
from tor_controller import TorController

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer()
    ],
    logger_factory=structlog.WriteLoggerFactory(),
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

app = FastAPI(
    title="InfoTerminal Egress Gateway",
    description="Anonymous/secure outbound connections for OSINT research",
    version="0.2.0"
)

security = HTTPBasic()
ua = UserAgent()

# Global instances
proxy_manager = None
tor_controller = None

class ProxyRequest(BaseModel):
    url: HttpUrl
    method: str = "GET"
    headers: Optional[Dict[str, str]] = None
    data: Optional[Dict[str, Any]] = None
    proxy_type: ProxyType = ProxyType.AUTO
    rotate_identity: bool = False
    sanitize_headers: bool = True

class ProxyResponse(BaseModel):
    status_code: int
    headers: Dict[str, str]
    content: str
    proxy_used: str
    request_id: str
    anonymity_level: str

class ProxyStatus(BaseModel):
    tor_available: bool
    tor_circuit_established: bool
    vpn_pools: List[str]
    proxy_pools: List[str]
    active_proxy: str
    anonymity_level: str
    request_count: int
    last_rotation: float

@app.on_event("startup")
async def startup_event():
    """Initialize proxy systems on startup."""
    global proxy_manager, tor_controller
    
    logger.info("Starting Egress Gateway Service")
    
    # Initialize Tor Controller
    tor_controller = TorController()
    await tor_controller.initialize()
    
    # Initialize Proxy Manager
    proxy_manager = ProxyManager()
    await proxy_manager.initialize()
    
    logger.info("Egress Gateway Service started")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    global proxy_manager, tor_controller
    
    logger.info("Shutting down Egress Gateway Service")
    
    if proxy_manager:
        await proxy_manager.cleanup()
    
    if tor_controller:
        await tor_controller.cleanup()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify basic auth credentials for write operations."""
    correct_username = os.getenv("EGRESS_BASIC_USER", "dev")
    correct_password = os.getenv("EGRESS_BASIC_PASS", "devpass")
    
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/healthz")
async def health_check():
    """Health check endpoint."""
    status = {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "egress-gateway",
        "version": "0.2.0"
    }
    
    if proxy_manager:
        status["proxy_manager"] = "ready"
    if tor_controller:
        status["tor_controller"] = "ready"
        
    return status

@app.post("/proxy/request", response_model=ProxyResponse)
async def proxy_request(
    request: ProxyRequest,
    background_tasks: BackgroundTasks,
    credentials: str = Depends(verify_credentials)
):
    """Execute an anonymous HTTP request through proxy infrastructure."""
    
    request_id = f"req_{int(time.time() * 1000)}"
    
    logger.info(
        "Processing proxy request",
        request_id=request_id,
        url=str(request.url),
        method=request.method,
        proxy_type=request.proxy_type
    )
    
    try:
        # Rotate identity if requested
        if request.rotate_identity:
            await proxy_manager.rotate_identity()
            if tor_controller and tor_controller.is_available():
                await tor_controller.new_identity()
        
        # Get appropriate proxy
        proxy_config = await proxy_manager.get_proxy(request.proxy_type)
        
        # Prepare headers
        headers = request.headers or {}
        
        if request.sanitize_headers:
            headers = sanitize_headers(headers)
        
        # Add randomized User-Agent
        if "User-Agent" not in headers:
            headers["User-Agent"] = ua.random
        
        # Execute request through proxy
        async with httpx.AsyncClient(
            proxies=proxy_config.proxy_url if proxy_config else None,
            timeout=30.0,
            follow_redirects=True
        ) as client:
            
            response = await client.request(
                method=request.method,
                url=str(request.url),
                headers=headers,
                json=request.data if request.method.upper() in ["POST", "PUT", "PATCH"] else None
            )
        
        # Sanitize response headers
        response_headers = dict(response.headers)
        response_headers = sanitize_response_headers(response_headers)
        
        # Log request for audit (anonymized)
        background_tasks.add_task(
            log_proxy_request,
            request_id=request_id,
            url_domain=urlparse(str(request.url)).netloc,
            method=request.method,
            status_code=response.status_code,
            proxy_used=proxy_config.name if proxy_config else "direct",
            anonymity_level=proxy_config.anonymity_level if proxy_config else "none"
        )
        
        return ProxyResponse(
            status_code=response.status_code,
            headers=response_headers,
            content=response.text,
            proxy_used=proxy_config.name if proxy_config else "direct",
            request_id=request_id,
            anonymity_level=proxy_config.anonymity_level if proxy_config else "none"
        )
        
    except httpx.RequestError as e:
        logger.error(
            "Proxy request failed",
            request_id=request_id,
            error=str(e),
            url=str(request.url)
        )
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
    
    except Exception as e:
        logger.error(
            "Unexpected error in proxy request",
            request_id=request_id,
            error=str(e),
            url=str(request.url)
        )
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/proxy/status", response_model=ProxyStatus)
async def get_proxy_status():
    """Get current proxy infrastructure status."""
    
    tor_available = tor_controller.is_available() if tor_controller else False
    tor_circuit = tor_controller.is_circuit_established() if tor_controller else False
    
    vpn_pools = proxy_manager.get_vpn_pools() if proxy_manager else []
    proxy_pools = proxy_manager.get_proxy_pools() if proxy_manager else []
    active_proxy = proxy_manager.get_active_proxy() if proxy_manager else "none"
    
    return ProxyStatus(
        tor_available=tor_available,
        tor_circuit_established=tor_circuit,
        vpn_pools=vpn_pools,
        proxy_pools=proxy_pools,
        active_proxy=active_proxy,
        anonymity_level="high" if tor_available else "medium",
        request_count=proxy_manager.get_request_count() if proxy_manager else 0,
        last_rotation=proxy_manager.get_last_rotation() if proxy_manager else 0
    )

@app.post("/proxy/rotate")
async def rotate_proxy(
    proxy_type: Optional[ProxyType] = None,
    credentials: str = Depends(verify_credentials)
):
    """Manually rotate proxy/identity."""
    
    logger.info("Manual proxy rotation requested", proxy_type=proxy_type)
    
    try:
        if proxy_type == ProxyType.TOR and tor_controller:
            await tor_controller.new_identity()
        
        if proxy_manager:
            await proxy_manager.rotate_identity(proxy_type)
        
        return {"status": "rotated", "timestamp": time.time()}
        
    except Exception as e:
        logger.error("Proxy rotation failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Rotation failed: {str(e)}")

def sanitize_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """Remove potentially identifying headers."""
    
    # Headers to remove for anonymity
    remove_headers = [
        "X-Forwarded-For",
        "X-Real-IP", 
        "X-Client-IP",
        "X-Forwarded-Host",
        "X-Originating-IP",
        "X-Remote-IP",
        "X-Remote-Addr",
        "X-Cluster-Client-IP"
    ]
    
    sanitized = {
        k: v for k, v in headers.items() 
        if k not in remove_headers
    }
    
    return sanitized

def sanitize_response_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """Remove server-identifying headers from response."""
    
    # Headers to remove from response
    remove_headers = [
        "Server",
        "X-Powered-By",
        "X-AspNet-Version",
        "X-AspNetMvc-Version",
        "X-Drupal-Cache",
        "X-Generator"
    ]
    
    sanitized = {
        k: v for k, v in headers.items() 
        if k not in remove_headers
    }
    
    return sanitized

async def log_proxy_request(
    request_id: str,
    url_domain: str,
    method: str,
    status_code: int,
    proxy_used: str,
    anonymity_level: str
):
    """Log proxy request for audit (anonymized)."""
    
    log_entry = {
        "request_id": request_id,
        "timestamp": time.time(),
        "url_domain": url_domain,  # Only domain, not full URL
        "method": method,
        "status_code": status_code,
        "proxy_used": proxy_used,
        "anonymity_level": anonymity_level,
        "service": "egress-gateway"
    }
    
    # In production, this would go to a secure audit log
    logger.info("Proxy request completed", **log_entry)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8615,
        reload=True,
        log_level="info"
    )
