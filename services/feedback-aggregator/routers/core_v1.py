"""
Core v1 router for feedback-aggregator service.
Provides health checks, readiness, and service info endpoints.
"""

import os
from typing import Dict, Any
from fastapi import APIRouter

router = APIRouter(tags=["Core"])


@router.get("/healthz")
def healthz() -> Dict[str, Any]:
    """Liveness probe - returns OK if service is running."""
    return {"ok": True}


@router.get("/readyz")  
def readyz() -> Dict[str, Any]:
    """Readiness probe - checks if service can handle requests."""
    checks = {}
    
    try:
        # Check database connectivity
        database_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/feedback_db")
        try:
            from sqlalchemy import create_engine
            # Quick connection test (don't keep connection open)
            engine = create_engine(database_url)
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            checks["database_connection"] = True
        except Exception as e:
            checks["database_connection"] = False
            checks["database_error"] = str(e)
        
        # Check Redis connectivity (optional)
        redis_available = False
        redis_error = None
        try:
            import aioredis
            checks["redis_library_available"] = True
            # Note: Can't test async connection in sync function
            redis_available = True
        except ImportError:
            checks["redis_library_available"] = False
            redis_error = "aioredis library not available"
        
        # Check GitHub integration setup (optional)
        github_token = os.getenv("GITHUB_TOKEN")
        checks["github_integration_configured"] = bool(github_token)
        
        # Check required libraries
        try:
            import requests
            import sqlalchemy
            import pydantic
            checks["required_libraries"] = True
        except ImportError as e:
            checks["required_libraries"] = False
            checks["library_error"] = str(e)
        
        # Overall readiness check
        critical_checks = [
            checks.get("database_connection", False),
            checks.get("required_libraries", False)
        ]
        
        all_ready = all(critical_checks)
        
        return {
            "ready": all_ready,
            "checks": checks,
            "optional_features": {
                "redis_caching": redis_available,
                "redis_error": redis_error,
                "github_issues": checks.get("github_integration_configured", False)
            }
        }
        
    except Exception as e:
        checks["error"] = str(e)
        return {"ready": False, "checks": checks}


@router.get("/info")
def info() -> Dict[str, Any]:
    """Service information and capabilities."""
    return {
        "service": "feedback-aggregator",
        "version": "v1",
        "description": "User feedback collection, analysis, and integration system for InfoTerminal",
        "capabilities": [
            "Feedback collection and categorization",
            "Intelligent feedback analysis and sentiment detection",
            "User voting and feedback prioritization",
            "GitHub issue automation",
            "Comprehensive analytics and reporting",
            "Real-time statistics and trends",
            "Multi-channel feedback aggregation",
            "Automated triage and routing"
        ],
        "feedback_types": [
            "bug_report - Software bugs and errors",
            "feature_request - New feature suggestions",
            "usability_issue - User experience problems",
            "performance_issue - Speed and performance concerns",
            "documentation_issue - Documentation improvements",
            "general_feedback - General comments and suggestions"
        ],
        "analysis_features": [
            "Sentiment analysis (positive/negative/neutral)",
            "Urgency detection from content keywords",
            "Automated priority suggestions",
            "Tag extraction and categorization",
            "Development effort estimation",
            "Trend analysis and pattern recognition"
        ],
        "integrations": [
            "GitHub Issues - Automated ticket creation",
            "Redis - Performance caching",
            "PostgreSQL - Persistent data storage",
            "Email notifications - Alert system",
            "Webhook support - External integrations"
        ],
        "analytics_capabilities": [
            "Feedback volume trends",
            "Rating distributions and averages",
            "Category and priority breakdowns",
            "User engagement metrics",
            "Response time analytics",
            "Growth rate calculations",
            "Tag popularity tracking"
        ],
        "data_privacy": [
            "Optional user identification",
            "Session-based tracking",
            "GDPR-compliant data handling",
            "Configurable data retention",
            "Anonymous feedback support"
        ],
        "build": "latest",
        "git": "main"
    }
