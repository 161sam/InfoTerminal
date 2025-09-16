# verification_api.py
"""
InfoTerminal v0.2.0 - Verification API Extensions for ops-controller
Enhanced orchestration for fact-checking and verification workflows
"""

import os
import json
import time
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from pathlib import Path

from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from _shared.audit import audit_log

# Verification API Models
class VerificationSessionRequest(BaseModel):
    text: str = Field(..., description="Text content to verify")
    url: Optional[str] = Field(None, description="Source URL if available")
    priority: str = Field("normal", description="Processing priority: low, normal, high")
    options: Optional[Dict[str, Any]] = Field({}, description="Additional verification options")

class VerificationSessionResponse(BaseModel):
    sessionId: str
    status: str
    workflow: Dict[str, Any]
    estimatedCompletionTime: str
    webhookUrl: Optional[str] = None

class VerificationStatusResponse(BaseModel):
    sessionId: str
    status: str  # pending, processing, completed, failed
    progress: Dict[str, Any]
    summary: Optional[Dict[str, Any]] = None
    results: Optional[List[Dict[str, Any]]] = None
    timestamp: str

class OrchestrationHealthResponse(BaseModel):
    nifi_status: str
    n8n_status: str
    verification_service_status: str
    pipeline_health: Dict[str, Any]
    active_sessions: int
    timestamp: str

# Global session tracking
verification_sessions: Dict[str, Dict[str, Any]] = {}

# Create API router
verification_router = APIRouter(prefix="/api/verification", tags=["verification"])

@verification_router.post("/start", response_model=VerificationSessionResponse)
async def start_verification_session(
    request: VerificationSessionRequest,
    background_tasks: BackgroundTasks,
    req: Request
):
    """
    Start a new verification session with full orchestration.
    Integrates NiFi, n8n, and verification services.
    """
    
    # Generate session ID
    session_id = f"verify-{int(time.time())}-{hash(request.text) % 10000:04d}"
    
    # Initialize session tracking
    verification_sessions[session_id] = {
        "id": session_id,
        "status": "initializing",
        "created_at": datetime.utcnow().isoformat(),
        "source_text": request.text,
        "source_url": request.url,
        "priority": request.priority,
        "options": request.options,
        "workflow": {
            "stage": "initialization",
            "total_steps": 5,
            "current_step": 0,
            "steps": [
                "initialization",
                "claim_extraction", 
                "evidence_retrieval",
                "stance_classification",
                "aggregation"
            ]
        },
        "progress": {
            "claims_extracted": 0,
            "evidence_found": 0,
            "stances_classified": 0,
            "credibility_checked": 0
        },
        "services": {
            "nifi_triggered": False,
            "n8n_triggered": False,
            "verification_active": False
        }
    }
    
    # Start orchestration in background
    background_tasks.add_task(
        orchestrate_verification_pipeline,
        session_id,
        request
    )
    
    # Audit log
    audit_log(
        action="verification_session_started",
        user=req.headers.get("X-User", "system"),
        resource=f"session:{session_id}",
        metadata={
            "text_length": len(request.text),
            "has_url": bool(request.url),
            "priority": request.priority
        }
    )
    
    # Estimate completion time based on text length and priority
    base_time = 30  # seconds
    text_factor = len(request.text) / 1000 * 5  # 5 seconds per 1000 chars
    priority_factor = {"low": 1.5, "normal": 1.0, "high": 0.7}[request.priority]
    
    estimated_seconds = int((base_time + text_factor) * priority_factor)
    completion_time = (datetime.utcnow() + timedelta(seconds=estimated_seconds)).isoformat()
    
    return VerificationSessionResponse(
        sessionId=session_id,
        status="initializing",
        workflow=verification_sessions[session_id]["workflow"],
        estimatedCompletionTime=completion_time,
        webhookUrl=f"/api/verification/webhook/{session_id}"
    )

@verification_router.get("/status/{session_id}", response_model=VerificationStatusResponse)
async def get_verification_status(session_id: str):
    """Get detailed status of a verification session."""
    
    if session_id not in verification_sessions:
        raise HTTPException(404, f"Session {session_id} not found")
    
    session = verification_sessions[session_id]
    
    return VerificationStatusResponse(
        sessionId=session_id,
        status=session["status"],
        progress=session.get("workflow", {}),
        summary=session.get("summary"),
        results=session.get("results"),
        timestamp=datetime.utcnow().isoformat()
    )

@verification_router.get("/sessions")
async def list_verification_sessions(
    status: Optional[str] = None,
    limit: int = 50
):
    """List all verification sessions with optional filtering."""
    
    sessions = list(verification_sessions.values())
    
    # Filter by status if provided
    if status:
        sessions = [s for s in sessions if s.get("status") == status]
    
    # Sort by creation time (newest first)
    sessions.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    # Limit results
    sessions = sessions[:limit]
    
    return {
        "sessions": sessions,
        "total": len(sessions),
        "timestamp": datetime.utcnow().isoformat()
    }

@verification_router.delete("/session/{session_id}")
async def cancel_verification_session(session_id: str, req: Request):
    """Cancel and cleanup a verification session."""
    
    if session_id not in verification_sessions:
        raise HTTPException(404, f"Session {session_id} not found")
    
    session = verification_sessions[session_id]
    
    # Update status
    session["status"] = "cancelled"
    session["cancelled_at"] = datetime.utcnow().isoformat()
    
    # TODO: Implement actual cancellation of running workflows
    # This would involve calling NiFi/n8n APIs to stop running processes
    
    audit_log(
        action="verification_session_cancelled",
        user=req.headers.get("X-User", "system"),
        resource=f"session:{session_id}",
        metadata={"cancelled_at": session["cancelled_at"]}
    )
    
    return {"success": True, "sessionId": session_id, "status": "cancelled"}

@verification_router.post("/webhook/{session_id}")
async def verification_webhook(session_id: str, payload: Dict[str, Any]):
    """Webhook endpoint for receiving updates from orchestration tools."""
    
    if session_id not in verification_sessions:
        raise HTTPException(404, f"Session {session_id} not found")
    
    session = verification_sessions[session_id]
    
    # Update session with webhook payload
    update_type = payload.get("type", "unknown")
    
    if update_type == "nifi_progress":
        session["services"]["nifi_triggered"] = True
        if "progress" in payload:
            session["progress"].update(payload["progress"])
            
    elif update_type == "n8n_complete":
        session["services"]["n8n_triggered"] = True
        if "summary" in payload:
            session["summary"] = payload["summary"]
        if "results" in payload:
            session["results"] = payload["results"]
            
    elif update_type == "verification_update":
        session["services"]["verification_active"] = True
        session["workflow"]["current_step"] = payload.get("step", 0)
        session["workflow"]["stage"] = payload.get("stage", "unknown")
    
    # Update timestamp
    session["updated_at"] = datetime.utcnow().isoformat()
    
    # Check if verification is complete
    if all([
        session["services"].get("nifi_triggered", False),
        session["services"].get("n8n_triggered", False),
        payload.get("status") == "completed"
    ]):
        session["status"] = "completed"
        session["completed_at"] = datetime.utcnow().isoformat()
    
    return {"success": True, "received": True}

@verification_router.post("/session-complete")
async def verification_session_complete(payload: Dict[str, Any]):
    """Endpoint called by n8n workflow when verification is complete."""
    
    session_id = payload.get("sessionId")
    if not session_id or session_id not in verification_sessions:
        raise HTTPException(404, f"Session {session_id} not found")
    
    session = verification_sessions[session_id]
    
    # Update session with final results
    session["status"] = "completed"
    session["completed_at"] = datetime.utcnow().isoformat()
    session["summary"] = payload.get("summary", {})
    session["results"] = payload.get("results", [])
    session["workflow"]["current_step"] = session["workflow"]["total_steps"]
    session["workflow"]["stage"] = "completed"
    
    # Calculate final statistics
    summary = session["summary"]
    session["statistics"] = {
        "processing_time_seconds": calculate_processing_time(session),
        "claims_per_minute": summary.get("totalClaims", 0) / max(calculate_processing_time(session) / 60, 1),
        "evidence_per_claim": summary.get("totalEvidence", 0) / max(summary.get("totalClaims", 1), 1),
        "average_confidence": summary.get("averageConfidence", 0),
        "average_credibility": summary.get("averageCredibility", 0)
    }
    
    return {"success": True, "sessionId": session_id, "status": "completed"}

@verification_router.get("/health", response_model=OrchestrationHealthResponse)
async def get_orchestration_health():
    """Get health status of all orchestration components."""
    
    health_data = {
        "nifi_status": await check_nifi_health(),
        "n8n_status": await check_n8n_health(), 
        "verification_service_status": await check_verification_service_health(),
        "pipeline_health": await check_pipeline_health(),
        "active_sessions": len([s for s in verification_sessions.values() if s.get("status") in ["processing", "initializing"]]),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return OrchestrationHealthResponse(**health_data)

@verification_router.post("/trigger-demo")
async def trigger_verification_demo(background_tasks: BackgroundTasks):
    """Trigger a demonstration of the verification pipeline."""
    
    demo_text = """
    Climate change is causing unprecedented global warming. Scientists report that 
    2023 was the hottest year on record, with average temperatures rising by 1.5 degrees 
    Celsius above pre-industrial levels. The melting of Arctic ice has accelerated, 
    contributing to rising sea levels worldwide. Renewable energy adoption has 
    increased by 300% over the past decade, making it the fastest-growing energy sector.
    """
    
    demo_request = VerificationSessionRequest(
        text=demo_text.strip(),
        priority="normal",
        options={"demo_mode": True, "accelerated": True}
    )
    
    # Start demo session
    from fastapi import Request as MockRequest
    mock_request = type('MockRequest', (), {'headers': {'get': lambda x, d=None: 'demo-user' if x == 'X-User' else d}})()
    
    response = await start_verification_session(demo_request, background_tasks, mock_request)
    
    return {
        "success": True,
        "message": "Demo verification started",
        "sessionId": response.sessionId,
        "demoText": demo_text.strip()[:100] + "...",
        "dashboardUrl": f"/verification/dashboard?session={response.sessionId}"
    }

# Helper Functions
async def orchestrate_verification_pipeline(session_id: str, request: VerificationSessionRequest):
    """Background task to orchestrate the full verification pipeline."""
    
    session = verification_sessions[session_id]
    
    try:
        # Update status
        session["status"] = "processing"
        session["workflow"]["stage"] = "orchestration"
        
        # Step 1: Trigger NiFi pipeline (if enabled)
        if os.getenv("IT_NIFI_ENABLE", "0") == "1":
            await trigger_nifi_verification(session_id, request)
            session["services"]["nifi_triggered"] = True
        
        # Step 2: Trigger n8n workflow
        if os.getenv("IT_N8N_ENABLE", "0") == "1":
            await trigger_n8n_verification(session_id, request)
            session["services"]["n8n_triggered"] = True
        
        # Step 3: Direct API calls if orchestration tools not available
        if not any(session["services"].values()):
            await direct_verification_pipeline(session_id, request)
            session["services"]["verification_active"] = True
        
        # Update workflow progress
        session["workflow"]["current_step"] = 3
        session["workflow"]["stage"] = "processing"
        
    except Exception as e:
        session["status"] = "failed"
        session["error"] = str(e)
        session["failed_at"] = datetime.utcnow().isoformat()
        
        audit_log(
            action="verification_session_failed",
            resource=f"session:{session_id}",
            metadata={"error": str(e)}
        )

async def trigger_nifi_verification(session_id: str, request: VerificationSessionRequest):
    """Trigger NiFi verification pipeline."""
    
    # NiFi HTTP POST to trigger pipeline
    import aiohttp
    
    nifi_url = os.getenv("IT_NIFI_URL", "http://localhost:8618/nifi-api")
    
    payload = {
        "sessionId": session_id,
        "text": request.text,
        "url": request.url,
        "priority": request.priority,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{nifi_url}/verification", json=payload, timeout=30) as response:
                if response.status != 200:
                    raise Exception(f"NiFi trigger failed: {response.status}")
                
    except Exception as e:
        raise Exception(f"Failed to trigger NiFi: {str(e)}")

async def trigger_n8n_verification(session_id: str, request: VerificationSessionRequest):
    """Trigger n8n verification workflow."""
    
    import aiohttp
    
    n8n_webhook_url = os.getenv("IT_N8N_WEBHOOK_URL", "http://localhost:5678/webhook/verify")
    
    payload = {
        "sessionId": session_id,
        "text": request.text,
        "url": request.url,
        "priority": request.priority,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(n8n_webhook_url, json=payload, timeout=60) as response:
                if response.status not in [200, 202]:
                    raise Exception(f"n8n trigger failed: {response.status}")
                
                result = await response.json()
                return result
                
    except Exception as e:
        raise Exception(f"Failed to trigger n8n: {str(e)}")

async def direct_verification_pipeline(session_id: str, request: VerificationSessionRequest):
    """Direct API-based verification when orchestration tools are not available."""
    
    import aiohttp
    
    verification_url = os.getenv("VERIFICATION_SERVICE_URL", "http://localhost:8617")
    frontend_api_url = os.getenv("FRONTEND_API_URL", "http://localhost:3000/api")
    
    session = verification_sessions[session_id]
    
    try:
        async with aiohttp.ClientSession() as http_session:
            
            # Step 1: Extract claims
            session["workflow"]["stage"] = "claim_extraction"
            claims_payload = {
                "text": request.text,
                "confidence_threshold": 0.7,
                "max_claims": 10
            }
            
            async with http_session.post(
                f"{frontend_api_url}/verification/extract-claims", 
                json=claims_payload
            ) as response:
                claims = await response.json()
                session["progress"]["claims_extracted"] = len(claims)
            
            # Step 2: Find evidence for each claim
            session["workflow"]["stage"] = "evidence_retrieval" 
            all_evidence = []
            
            for claim in claims[:5]:  # Limit to first 5 claims for demo
                evidence_payload = {
                    "claim": claim["text"],
                    "max_sources": 3,
                    "source_types": ["web", "wikipedia", "news"]
                }
                
                async with http_session.post(
                    f"{frontend_api_url}/verification/find-evidence",
                    json=evidence_payload
                ) as response:
                    evidence = await response.json()
                    all_evidence.extend(evidence)
            
            session["progress"]["evidence_found"] = len(all_evidence)
            
            # Step 3: Classify stance for high-quality evidence
            session["workflow"]["stage"] = "stance_classification"
            verification_results = []
            
            high_quality_evidence = [e for e in all_evidence if e.get("relevance_score", 0) > 0.6][:10]
            
            for i, evidence in enumerate(high_quality_evidence):
                if i < len(claims):
                    stance_payload = {
                        "claim": claims[i]["text"],
                        "evidence": evidence["snippet"],
                        "context": evidence.get("source_title", "")
                    }
                    
                    async with http_session.post(
                        f"{frontend_api_url}/verification/classify-stance",
                        json=stance_payload
                    ) as response:
                        stance = await response.json()
                        
                        verification_results.append({
                            "claim": claims[i],
                            "evidence": evidence,
                            "stance": stance,
                            "timestamp": datetime.utcnow().isoformat()
                        })
            
            session["progress"]["stances_classified"] = len(verification_results)
            
            # Step 4: Generate summary
            session["workflow"]["stage"] = "aggregation"
            summary = {
                "totalClaims": len(claims),
                "totalEvidence": len(all_evidence),
                "verificationResults": len(verification_results),
                "averageConfidence": sum([r["stance"]["confidence"] for r in verification_results]) / max(len(verification_results), 1),
                "supportingEvidence": len([r for r in verification_results if r["stance"]["stance"] == "support"]),
                "contradictingEvidence": len([r for r in verification_results if r["stance"]["stance"] == "contradict"]),
                "neutralEvidence": len([r for r in verification_results if r["stance"]["stance"] == "neutral"])
            }
            
            # Store results
            session["summary"] = summary
            session["results"] = verification_results
            session["status"] = "completed"
            session["completed_at"] = datetime.utcnow().isoformat()
            session["workflow"]["current_step"] = session["workflow"]["total_steps"]
            session["workflow"]["stage"] = "completed"
            
    except Exception as e:
        raise Exception(f"Direct verification failed: {str(e)}")

async def check_nifi_health() -> str:
    """Check NiFi service health."""
    try:
        import aiohttp
        
        nifi_url = os.getenv("IT_NIFI_URL", "http://localhost:8618/nifi-api")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{nifi_url}/system-diagnostics", timeout=10) as response:
                if response.status == 200:
                    return "healthy"
                else:
                    return f"unhealthy_{response.status}"
                    
    except Exception:
        return "unavailable"

async def check_n8n_health() -> str:
    """Check n8n service health."""
    try:
        import aiohttp
        
        n8n_url = os.getenv("IT_N8N_URL", "http://localhost:5678")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{n8n_url}/healthz", timeout=10) as response:
                if response.status == 200:
                    return "healthy"
                else:
                    return f"unhealthy_{response.status}"
                    
    except Exception:
        return "unavailable"

async def check_verification_service_health() -> str:
    """Check verification service health."""
    try:
        import aiohttp
        
        verification_url = os.getenv("VERIFICATION_SERVICE_URL", "http://localhost:8617")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{verification_url}/health", timeout=10) as response:
                if response.status == 200:
                    return "healthy"
                else:
                    return f"unhealthy_{response.status}"
                    
    except Exception:
        return "unavailable"

async def check_pipeline_health() -> Dict[str, Any]:
    """Check overall pipeline health."""
    
    # Count active sessions by status
    active_count = len([s for s in verification_sessions.values() if s.get("status") == "processing"])
    completed_count = len([s for s in verification_sessions.values() if s.get("status") == "completed"]) 
    failed_count = len([s for s in verification_sessions.values() if s.get("status") == "failed"])
    
    # Calculate success rate
    total_finished = completed_count + failed_count
    success_rate = (completed_count / max(total_finished, 1)) * 100
    
    # Calculate average processing time
    completed_sessions = [s for s in verification_sessions.values() if s.get("status") == "completed"]
    avg_processing_time = 0
    
    if completed_sessions:
        processing_times = [calculate_processing_time(s) for s in completed_sessions]
        avg_processing_time = sum(processing_times) / len(processing_times)
    
    return {
        "active_sessions": active_count,
        "completed_sessions": completed_count,
        "failed_sessions": failed_count,
        "success_rate_percent": round(success_rate, 1),
        "average_processing_time_seconds": round(avg_processing_time, 1),
        "pipeline_status": "healthy" if success_rate >= 80 else "degraded" if success_rate >= 50 else "unhealthy"
    }

def calculate_processing_time(session: Dict[str, Any]) -> float:
    """Calculate processing time for a session in seconds."""
    
    start_time = session.get("created_at")
    end_time = session.get("completed_at") or session.get("failed_at")
    
    if not start_time or not end_time:
        return 0.0
    
    try:
        start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        return (end - start).total_seconds()
    except Exception:
        return 0.0
