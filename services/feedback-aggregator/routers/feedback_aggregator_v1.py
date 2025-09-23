"""
Feedback Aggregator v1 router - User Feedback Collection and Analysis API.

Provides comprehensive feedback management including collection, analysis,
voting, statistics, GitHub integration, and team productivity metrics.
"""

import asyncio
import json
import logging
import os
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query, Path, Depends, Request
from fastapi.responses import JSONResponse

from service import FeedbackService
from _shared.api_standards.error_schemas import StandardError, ErrorCodes, create_error_response
from _shared.api_standards.pagination import PaginatedResponse, PaginationParams
from models.requests import (
    FeedbackCreate, FeedbackUpdate, FeedbackResponse, VoteCreate, VoteResponse,
    FeedbackStats, FeedbackTrends, FeedbackAnalysis, UserFeedbackSummary, TeamProductivity,
    BulkFeedbackOperation, BulkOperationResult, FeedbackFilter, FeedbackExport, FeedbackImport,
    GitHubIntegration, NotificationConfig, WebhookPayload, APIKeyConfig,
    FeedbackTemplate, FeedbackHealthStatus,
    FeedbackType, Priority, Status, Sentiment, VoteType
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Feedback Aggregator"])


def get_feedback_service(request: Request) -> FeedbackService:
    """Dependency to get feedback service from app state."""
    return request.app.state.feedback_service


# Dependency for error handling
def handle_feedback_errors(func):
    """Decorator to handle feedback operation errors with standard error format"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Feedback validation error: {e}")
            error_response = create_error_response(
                ErrorCodes.VALIDATION_ERROR,
                str(e),
                {"service": "feedback-aggregator"}
            )
            raise HTTPException(status_code=400, detail=error_response.dict())
        except Exception as e:
            logger.error(f"Feedback operation failed: {e}")
            error_response = create_error_response(
                ErrorCodes.INTERNAL_ERROR,
                "Internal feedback operation error",
                {"service": "feedback-aggregator", "original_error": str(e)}
            )
            raise HTTPException(status_code=500, detail=error_response.dict())
    return wrapper


# Core Feedback Management

@router.post("/feedback", response_model=FeedbackResponse)
@handle_feedback_errors
async def create_feedback(
    feedback_data: FeedbackCreate,
    background_tasks: BackgroundTasks,
    service: FeedbackService = Depends(get_feedback_service)
) -> FeedbackResponse:
    """
    Submit new user feedback with intelligent analysis.
    
    Automatically analyzes feedback for:
    - Sentiment detection (positive/negative/neutral)
    - Urgency classification based on keywords
    - Priority suggestions based on type and content
    - Tag extraction from description
    - Development effort estimation
    
    Background tasks:
    - GitHub issue creation (if configured)
    - Notification dispatch
    - Analytics update
    """
    try:
        response = await service.create_feedback(feedback_data, background_tasks)
        return response
    except Exception as e:
        logger.error(f"Failed to create feedback: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to create feedback entry",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.get("/feedback", response_model=PaginatedResponse[FeedbackResponse])
@handle_feedback_errors
async def list_feedback(
    pagination: PaginationParams = Depends(),
    feedback_type: Optional[List[FeedbackType]] = Query(None, description="Filter by feedback type"),
    priority: Optional[List[Priority]] = Query(None, description="Filter by priority"),
    status: Optional[List[Status]] = Query(None, description="Filter by status"),
    sentiment: Optional[List[Sentiment]] = Query(None, description="Filter by sentiment"),
    user_id: Optional[str] = Query(None, description="Filter by user"),
    assignee: Optional[str] = Query(None, description="Filter by assignee"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    rating_min: Optional[int] = Query(None, description="Minimum rating", ge=1, le=5),
    rating_max: Optional[int] = Query(None, description="Maximum rating", ge=1, le=5),
    search: Optional[str] = Query(None, description="Search in title and description"),
    has_github_issue: Optional[bool] = Query(None, description="Has GitHub issue"),
    service: FeedbackService = Depends(get_feedback_service)
) -> PaginatedResponse[FeedbackResponse]:
    """
    List feedback entries with comprehensive filtering and search.
    
    Supports filtering by:
    - Feedback type, priority, status, sentiment
    - User, assignee, tags, rating range
    - Text search across title and description
    - GitHub issue association
    - Date ranges and custom criteria
    """
    # Create filter object
    filters = FeedbackFilter(
        feedback_type=feedback_type,
        priority=priority,
        status=status,
        sentiment=sentiment,
        user_id=user_id,
        assignee=assignee,
        tags=tags,
        rating_min=rating_min,
        rating_max=rating_max,
        search=search,
        has_github_issue=has_github_issue
    )
    
    try:
        feedback_list = await service.get_filtered_feedback(filters, pagination)
        return feedback_list
    except Exception as e:
        logger.error(f"Failed to list feedback: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to retrieve feedback list",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.get("/feedback/{feedback_id}", response_model=FeedbackResponse)
@handle_feedback_errors
async def get_feedback_detail(
    feedback_id: int = Path(..., description="Feedback identifier"),
    service: FeedbackService = Depends(get_feedback_service)
) -> FeedbackResponse:
    """Get detailed information about a specific feedback item."""
    try:
        feedback = await service.get_feedback_by_id(feedback_id)
        if not feedback:
            error_response = create_error_response(
                ErrorCodes.RESOURCE_NOT_FOUND,
                f"Feedback not found: {feedback_id}",
                {"feedback_id": feedback_id}
            )
            raise HTTPException(status_code=404, detail=error_response.dict())
        
        return feedback
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get feedback {feedback_id}: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to retrieve feedback",
            {"feedback_id": feedback_id, "error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.put("/feedback/{feedback_id}", response_model=FeedbackResponse)
@handle_feedback_errors
async def update_feedback(
    feedback_id: int = Path(..., description="Feedback identifier"),
    feedback_data: FeedbackUpdate = ...,
    updated_by: str = Query(..., description="User performing update"),
    service: FeedbackService = Depends(get_feedback_service)
) -> FeedbackResponse:
    """
    Update feedback properties with change tracking.
    
    Supports updating:
    - Status and priority changes
    - Assignment to team members
    - Tag modifications
    - GitHub issue associations
    - Title and description edits
    """
    try:
        updated_feedback = await service.update_feedback(feedback_id, feedback_data, updated_by)
        if not updated_feedback:
            error_response = create_error_response(
                ErrorCodes.RESOURCE_NOT_FOUND,
                f"Feedback not found: {feedback_id}",
                {"feedback_id": feedback_id}
            )
            raise HTTPException(status_code=404, detail=error_response.dict())
        
        return updated_feedback
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update feedback {feedback_id}: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to update feedback",
            {"feedback_id": feedback_id, "error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


# Voting System

@router.post("/feedback/{feedback_id}/vote", response_model=VoteResponse)
@handle_feedback_errors
async def vote_on_feedback(
    feedback_id: int = Path(..., description="Feedback identifier"),
    vote_data: VoteCreate = ...,
    service: FeedbackService = Depends(get_feedback_service)
) -> VoteResponse:
    """
    Vote on feedback item to indicate user support.
    
    Users can upvote or downvote feedback to help prioritize
    development efforts based on community interest.
    """
    vote_data.feedback_id = feedback_id  # Set from path parameter
    
    try:
        vote_response = await service.vote_feedback(vote_data)
        if not vote_response:
            error_response = create_error_response(
                "VOTE_FAILED",
                "Failed to record vote on feedback",
                {"feedback_id": feedback_id, "user_id": vote_data.user_id}
            )
            raise HTTPException(status_code=400, detail=error_response.dict())
        
        return vote_response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to vote on feedback {feedback_id}: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to process vote",
            {"feedback_id": feedback_id, "error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.delete("/feedback/{feedback_id}/vote")
@handle_feedback_errors
async def remove_vote(
    feedback_id: int = Path(..., description="Feedback identifier"),
    user_id: str = Query(..., description="User removing vote"),
    service: FeedbackService = Depends(get_feedback_service)
) -> Dict[str, Any]:
    """Remove user's vote from feedback item."""
    try:
        success = await service.remove_vote(feedback_id, user_id)
        if not success:
            error_response = create_error_response(
                ErrorCodes.RESOURCE_NOT_FOUND,
                "Vote not found",
                {"feedback_id": feedback_id, "user_id": user_id}
            )
            raise HTTPException(status_code=404, detail=error_response.dict())
        
        return {
            "feedback_id": feedback_id,
            "user_id": user_id,
            "message": "Vote removed successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to remove vote on feedback {feedback_id}: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to remove vote",
            {"feedback_id": feedback_id, "error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


# Analytics and Statistics

@router.get("/feedback/stats", response_model=FeedbackStats)
@handle_feedback_errors
async def get_feedback_statistics(
    service: FeedbackService = Depends(get_feedback_service)
) -> FeedbackStats:
    """
    Get comprehensive feedback statistics and metrics.
    
    Includes:
    - Volume breakdowns by type, priority, status, sentiment
    - Average ratings and satisfaction metrics
    - Popular tags and trending topics
    - Recent activity trends and growth rates
    - Resolution time metrics
    """
    try:
        stats = await service.get_feedback_stats()
        return stats
    except Exception as e:
        logger.error(f"Failed to get feedback stats: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to retrieve feedback statistics",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.get("/feedback/trends", response_model=FeedbackTrends)
@handle_feedback_errors
async def get_feedback_trends(
    period: str = Query("weekly", description="Trend period (daily, weekly, monthly)"),
    days: int = Query(30, description="Number of days to analyze", ge=7, le=365),
    service: FeedbackService = Depends(get_feedback_service)
) -> FeedbackTrends:
    """
    Get feedback trends over time with pattern analysis.
    
    Analyzes:
    - Volume trends over specified periods
    - Growth rates and seasonal patterns
    - Peak activity identification
    - Satisfaction score trends
    - Type distribution changes
    """
    try:
        trends = await service.get_trends_analysis(period, days)
        return trends
    except Exception as e:
        logger.error(f"Failed to get feedback trends: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to retrieve feedback trends",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.get("/health", response_model=FeedbackHealthStatus)
async def get_feedback_health(
    service: FeedbackService = Depends(get_feedback_service)
) -> FeedbackHealthStatus:
    """
    Get comprehensive feedback aggregator health status.
    
    Includes:
    - Database and Redis connectivity
    - GitHub integration status
    - Recent activity metrics
    - Processing queue status
    - Resource utilization
    - Service uptime
    """
    try:
        health = await service.get_health_status()
        return health
    except Exception as e:
        logger.error(f"Failed to get health status: {e}")
        # Return degraded status instead of error
        return FeedbackHealthStatus(
            status="degraded",
            service="feedback-aggregator",
            database_healthy=False,
            redis_healthy=False,
            github_integration_healthy=False,
            total_feedback=0,
            pending_analysis=0,
            recent_activity=0,
            uptime_seconds=0,
            memory_usage_mb=0
        )


# Additional endpoints for bulk operations, exports, etc. can be added here
# For now, focusing on core functionality for migration completion

@router.post("/feedback/bulk", response_model=BulkOperationResult)
@handle_feedback_errors
async def bulk_feedback_operation(
    operation: BulkFeedbackOperation,
    performed_by: str = Query(..., description="User performing bulk operation"),
    service: FeedbackService = Depends(get_feedback_service)
) -> BulkOperationResult:
    """
    Perform bulk operations on multiple feedback items.
    
    Supported operations:
    - update_status: Change status for multiple items
    - update_priority: Bulk priority updates
    - assign: Bulk assignment to team members
    - add_tags: Add tags to multiple items
    - close: Close multiple feedback items
    - delete: Bulk deletion with authorization
    """
    try:
        result = await service.bulk_operation(operation, performed_by)
        return result
    except Exception as e:
        logger.error(f"Bulk operation failed: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Bulk operation failed",
            {"operation": operation.operation, "error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


@router.get("/feedback/tags", response_model=List[Dict[str, Any]])
@handle_feedback_errors
async def get_popular_tags(
    limit: int = Query(50, description="Maximum number of tags to return", ge=1, le=200),
    min_count: int = Query(1, description="Minimum usage count", ge=1),
    service: FeedbackService = Depends(get_feedback_service)
) -> List[Dict[str, Any]]:
    """
    Get most popular feedback tags with usage statistics.
    
    Returns tags sorted by usage frequency with counts
    and trending information.
    """
    try:
        tags = await service.get_popular_tags(limit, min_count)
        return tags
    except Exception as e:
        logger.error(f"Failed to get popular tags: {e}")
        error_response = create_error_response(
            ErrorCodes.INTERNAL_ERROR,
            "Failed to retrieve popular tags",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())
