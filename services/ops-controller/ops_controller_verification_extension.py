# ops_controller_verification_extension.py
"""
Extension to add verification orchestration to ops-controller app.py
This should be integrated into the main app.py file.
"""

# Add these imports to the top of app.py after existing imports:
try:
    from verification_api import verification_router
    VERIFICATION_ENABLED = True
except ImportError:
    VERIFICATION_ENABLED = False

# Add this after the existing APP = FastAPI(...) line:
if VERIFICATION_ENABLED:
    APP.include_router(verification_router)

# Add these endpoints before the existing security endpoints:

@APP.get("/api/orchestration/health")
async def get_orchestration_health():
    """Get health status of all orchestration services."""
    if not VERIFICATION_ENABLED:
        return {"status": "verification_disabled"}
    
    # Import here to avoid circular imports
    from verification_api import get_orchestration_health
    return await get_orchestration_health()

@APP.post("/api/orchestration/trigger-pipeline")
async def trigger_orchestration_pipeline(
    request: Dict[str, Any],
    background_tasks: BackgroundTasks,
    req: Request
):
    """Trigger orchestration pipeline manually."""
    _require_enabled()
    _require_rbac(req)
    
    if not VERIFICATION_ENABLED:
        raise HTTPException(503, "Verification orchestration not available")
    
    from verification_api import VerificationSessionRequest, start_verification_session
    
    try:
        verification_request = VerificationSessionRequest(**request)
        response = await start_verification_session(verification_request, background_tasks, req)
        
        _audit("orchestration_pipeline_triggered", req, session_id=response.sessionId)
        
        return {
            "success": True,
            "sessionId": response.sessionId,
            "message": "Orchestration pipeline triggered successfully"
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to trigger pipeline: {str(e)}")

@APP.get("/api/orchestration/sessions")
async def list_orchestration_sessions(
    status: Optional[str] = None,
    limit: int = 50
):
    """List all orchestration sessions."""
    if not VERIFICATION_ENABLED:
        return {"sessions": [], "total": 0, "message": "Verification disabled"}
    
    from verification_api import list_verification_sessions
    return await list_verification_sessions(status, limit)

# Add this to the startup_event function:
async def enhanced_startup_event():
    """Enhanced startup with verification orchestration."""
    global security_manager
    
    if ENABLED:
        security_manager = SessionManager()
        await security_manager.initialize()
        
        # Initialize verification orchestration if enabled
        if VERIFICATION_ENABLED:
            print("🔍 InfoTerminal v0.2.0 - Verification Orchestration Enabled")
            print("   - NiFi Integration:", "✅" if os.getenv("IT_NIFI_ENABLE") == "1" else "❌")
            print("   - n8n Integration:", "✅" if os.getenv("IT_N8N_ENABLE") == "1" else "❌")
            print("   - Direct API Mode:", "✅" if os.getenv("IT_VERIFICATION_DIRECT") == "1" else "❌")

# Replace the existing @APP.on_event("startup") with:
@APP.on_event("startup")
async def startup_event():
    await enhanced_startup_event()

# Add these new environment variable checks:
NIFI_ENABLED = os.getenv("IT_NIFI_ENABLE", "0") == "1"
N8N_ENABLED = os.getenv("IT_N8N_ENABLE", "0") == "1" 
VERIFICATION_DIRECT = os.getenv("IT_VERIFICATION_DIRECT", "0") == "1"

# Add new endpoint for system configuration:
@APP.get("/api/system/config")
async def get_system_config():
    """Get current system configuration."""
    
    return {
        "version": "0.2.0",
        "features": {
            "ops_controller": ENABLED,
            "security_layer": bool(security_manager),
            "verification_orchestration": VERIFICATION_ENABLED,
            "nifi_integration": NIFI_ENABLED,
            "n8n_integration": N8N_ENABLED,
            "direct_verification": VERIFICATION_DIRECT
        },
        "services": {
            "mode": MODE,
            "compose_command": COMPOSE,
            "docker_socket": SOCKET,
            "lock_timeout": LOCK_TIMEOUT
        },
        "endpoints": {
            "health": "/health",
            "stacks": "/api/ops/stacks",
            "security": "/api/security/*",
            "verification": "/api/verification/*" if VERIFICATION_ENABLED else None,
            "orchestration": "/api/orchestration/*"
        },
        "timestamp": time.time()
    }

# Add comprehensive health check endpoint:
@APP.get("/health/comprehensive")
async def comprehensive_health_check():
    """Comprehensive health check for all InfoTerminal services."""
    
    health = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.2.0",
        "services": {}
    }
    
    try:
        # Check ops controller
        health["services"]["ops_controller"] = {
            "status": "healthy" if ENABLED else "disabled",
            "enabled": ENABLED,
            "mode": MODE
        }
        
        # Check security manager
        health["services"]["security_manager"] = {
            "status": "healthy" if security_manager else "unavailable",
            "initialized": bool(security_manager)
        }
        
        # Check verification orchestration
        if VERIFICATION_ENABLED:
            from verification_api import check_nifi_health, check_n8n_health, check_verification_service_health
            
            health["services"]["nifi"] = {
                "status": await check_nifi_health(),
                "enabled": NIFI_ENABLED
            }
            
            health["services"]["n8n"] = {
                "status": await check_n8n_health(), 
                "enabled": N8N_ENABLED
            }
            
            health["services"]["verification_service"] = {
                "status": await check_verification_service_health(),
                "direct_mode": VERIFICATION_DIRECT
            }
        else:
            health["services"]["verification_orchestration"] = {
                "status": "disabled",
                "reason": "verification_api_not_available"
            }
        
        # Check Docker (if in docker mode)
        if MODE == "docker":
            try:
                import docker
                client = docker.from_env()
                client.ping()
                health["services"]["docker"] = {"status": "healthy"}
            except Exception as e:
                health["services"]["docker"] = {"status": "unhealthy", "error": str(e)}
        
        # Determine overall status
        service_statuses = [s.get("status", "unknown") for s in health["services"].values()]
        unhealthy_count = len([s for s in service_statuses if s not in ["healthy", "disabled"]])
        
        if unhealthy_count > 0:
            health["status"] = "degraded" if unhealthy_count == 1 else "unhealthy"
            
    except Exception as e:
        health["status"] = "error"
        health["error"] = str(e)
    
    return health

# Add endpoint for triggering demo workflows:
@APP.post("/api/demo/verification")
async def demo_verification_workflow(background_tasks: BackgroundTasks, req: Request):
    """Trigger a demonstration of the complete verification workflow."""
    
    if not VERIFICATION_ENABLED:
        raise HTTPException(503, "Verification not available")
    
    from verification_api import trigger_verification_demo
    
    result = await trigger_verification_demo(background_tasks)
    
    _audit("demo_verification_triggered", req, session_id=result.get("sessionId"))
    
    return result
