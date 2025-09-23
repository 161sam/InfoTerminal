"""
Pydantic models for Feedback Aggregator Service v1.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum
import uuid


class FeedbackType(str, Enum):
    """Types of feedback that can be collected."""
    BUG_REPORT = "bug_report"
    FEATURE_REQUEST = "feature_request"
    USABILITY_ISSUE = "usability_issue"
    PERFORMANCE_ISSUE = "performance_issue"
    DOCUMENTATION_ISSUE = "documentation_issue"
    GENERAL_FEEDBACK = "general_feedback"


class Priority(str, Enum):
    """Priority levels for feedback items."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Status(str, Enum):
    """Processing status of feedback items."""
    NEW = "new"
    TRIAGED = "triaged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Sentiment(str, Enum):
    """Detected sentiment of feedback."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class VoteType(str, Enum):
    """Types of votes for feedback."""
    UPVOTE = "upvote"
    DOWNVOTE = "downvote"


class FeedbackCreate(BaseModel):
    """Request to create new feedback entry."""
    session_id: str = Field(..., description="Session identifier for tracking")
    user_id: Optional[str] = Field(None, description="User identifier (optional for anonymous feedback)")
    feedback_type: FeedbackType = Field(..., description="Type of feedback")
    title: str = Field(..., description="Feedback title", min_length=5, max_length=200)
    description: str = Field(..., description="Detailed feedback description", min_length=10, max_length=5000)
    rating: Optional[int] = Field(None, description="User rating (1-5 scale)", ge=1, le=5)
    page_url: str = Field(..., description="URL where feedback was submitted")
    user_agent: str = Field(..., description="Browser user agent string")
    browser_info: Dict[str, Any] = Field(default_factory=dict, description="Browser and system information")
    steps_to_reproduce: Optional[str] = Field(None, description="Steps to reproduce the issue", max_length=2000)
    expected_behavior: Optional[str] = Field(None, description="Expected behavior description", max_length=1000)
    actual_behavior: Optional[str] = Field(None, description="Actual behavior description", max_length=1000)
    tags: List[str] = Field(default_factory=list, description="User-defined tags", max_items=10)
    attachments: List[str] = Field(default_factory=list, description="Attachment file URLs", max_items=5)
    contact_email: Optional[str] = Field(None, description="Contact email for follow-up")
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "session_12345",
                "user_id": "user_67890",
                "feedback_type": "bug_report",
                "title": "Search results not loading properly",
                "description": "When I search for entities, the results page shows a loading spinner indefinitely and never displays results.",
                "rating": 2,
                "page_url": "https://infoterminal.example.com/search",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "browser_info": {
                    "browser": "Chrome",
                    "version": "91.0.4472.124",
                    "os": "Windows 10"
                },
                "steps_to_reproduce": "1. Go to search page\n2. Enter 'test query'\n3. Click search button",
                "expected_behavior": "Search results should be displayed within 2-3 seconds",
                "actual_behavior": "Loading spinner appears and never stops",
                "tags": ["search", "ui", "loading"],
                "contact_email": "user@example.com"
            }
        }


class FeedbackUpdate(BaseModel):
    """Request to update feedback properties."""
    title: Optional[str] = Field(None, description="Updated title", min_length=5, max_length=200)
    description: Optional[str] = Field(None, description="Updated description", min_length=10, max_length=5000)
    status: Optional[Status] = Field(None, description="Updated status")
    priority: Optional[Priority] = Field(None, description="Updated priority")
    tags: Optional[List[str]] = Field(None, description="Updated tags", max_items=10)
    assignee: Optional[str] = Field(None, description="Assigned team member")
    github_issue_url: Optional[str] = Field(None, description="Associated GitHub issue URL")


class FeedbackResponse(BaseModel):
    """Response model for feedback entries."""
    id: int = Field(..., description="Feedback identifier")
    session_id: str = Field(..., description="Session identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    feedback_type: FeedbackType = Field(..., description="Feedback type")
    title: str = Field(..., description="Feedback title")
    description: str = Field(..., description="Feedback description")
    rating: Optional[int] = Field(None, description="User rating")
    priority: Priority = Field(..., description="Assigned priority")
    status: Status = Field(..., description="Current status")
    votes: int = Field(..., description="Net vote score", ge=0)
    tags: List[str] = Field(..., description="Associated tags")
    github_issue_url: Optional[str] = Field(None, description="GitHub issue URL")
    assignee: Optional[str] = Field(None, description="Assigned team member")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    page_url: str = Field(..., description="Source page URL")
    sentiment: Optional[Sentiment] = Field(None, description="Detected sentiment")
    urgency: Optional[str] = Field(None, description="Detected urgency level")
    estimated_effort: Optional[str] = Field(None, description="Estimated development effort")


class VoteCreate(BaseModel):
    """Request to vote on feedback."""
    user_id: str = Field(..., description="User casting the vote")
    vote_type: VoteType = Field(..., description="Type of vote")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "user_12345",
                "vote_type": "upvote"
            }
        }


class VoteResponse(BaseModel):
    """Response for vote operations."""
    feedback_id: int = Field(..., description="Feedback item ID")
    user_id: str = Field(..., description="User who voted")
    vote_type: VoteType = Field(..., description="Type of vote")
    created_at: datetime = Field(..., description="Vote timestamp")


class FeedbackStats(BaseModel):
    """Comprehensive feedback statistics."""
    total_feedback: int = Field(..., description="Total feedback entries", ge=0)
    by_type: Dict[str, int] = Field(..., description="Feedback count by type")
    by_priority: Dict[str, int] = Field(..., description="Feedback count by priority")
    by_status: Dict[str, int] = Field(..., description="Feedback count by status")
    by_sentiment: Dict[str, int] = Field(..., description="Feedback count by sentiment")
    average_rating: float = Field(..., description="Average user rating", ge=0, le=5)
    top_tags: List[Dict[str, Any]] = Field(..., description="Most popular tags")
    recent_trends: Dict[str, Any] = Field(..., description="Recent activity trends")
    resolution_metrics: Dict[str, Any] = Field(..., description="Resolution time metrics")


class FeedbackTrends(BaseModel):
    """Feedback trends over time."""
    period: str = Field(..., description="Time period (daily, weekly, monthly)")
    data_points: List[Dict[str, Any]] = Field(..., description="Trend data points")
    growth_rate: float = Field(..., description="Growth rate percentage")
    peak_periods: List[Dict[str, Any]] = Field(..., description="Peak activity periods")
    seasonal_patterns: Dict[str, Any] = Field(..., description="Seasonal pattern analysis")


class FeedbackAnalysis(BaseModel):
    """Automated feedback analysis results."""
    sentiment: Sentiment = Field(..., description="Detected sentiment")
    urgency: str = Field(..., description="Urgency level (critical/high/medium/low)")
    suggested_priority: Priority = Field(..., description="AI-suggested priority")
    extracted_tags: List[str] = Field(..., description="Automatically extracted tags")
    estimated_effort: str = Field(..., description="Estimated development effort")
    similar_feedback: List[int] = Field(..., description="Similar feedback item IDs")
    confidence_score: float = Field(..., description="Analysis confidence score", ge=0, le=1)


class BulkFeedbackOperation(BaseModel):
    """Bulk operation on multiple feedback items."""
    feedback_ids: List[int] = Field(..., description="Feedback IDs to operate on", min_items=1, max_items=100)
    operation: str = Field(..., description="Operation type", regex="^(update_status|update_priority|assign|add_tags|close|delete)$")
    parameters: Dict[str, Any] = Field(..., description="Operation parameters")
    
    class Config:
        schema_extra = {
            "example": {
                "feedback_ids": [1, 2, 3, 5, 8],
                "operation": "update_status",
                "parameters": {"status": "triaged"}
            }
        }


class BulkOperationResult(BaseModel):
    """Result of bulk feedback operation."""
    total_items: int = Field(..., description="Total items processed", ge=0)
    successful: int = Field(..., description="Successfully processed items", ge=0)
    failed: int = Field(..., description="Failed items", ge=0)
    errors: List[Dict[str, str]] = Field(default_factory=list, description="Error details")


class GitHubIntegration(BaseModel):
    """GitHub integration configuration."""
    enabled: bool = Field(..., description="Whether GitHub integration is enabled")
    repository: str = Field(..., description="GitHub repository (owner/repo)")
    auto_create_issues: bool = Field(..., description="Automatically create GitHub issues")
    label_mapping: Dict[str, List[str]] = Field(..., description="Feedback type to GitHub labels mapping")
    webhook_url: Optional[str] = Field(None, description="Webhook URL for GitHub events")


class NotificationConfig(BaseModel):
    """Notification configuration."""
    email_enabled: bool = Field(default=False, description="Enable email notifications")
    webhook_enabled: bool = Field(default=False, description="Enable webhook notifications")
    notification_rules: List[Dict[str, Any]] = Field(default_factory=list, description="Notification rules")
    escalation_rules: List[Dict[str, Any]] = Field(default_factory=list, description="Escalation rules")


class FeedbackFilter(BaseModel):
    """Filtering options for feedback queries."""
    feedback_type: Optional[List[FeedbackType]] = Field(None, description="Filter by feedback type")
    priority: Optional[List[Priority]] = Field(None, description="Filter by priority")
    status: Optional[List[Status]] = Field(None, description="Filter by status")
    sentiment: Optional[List[Sentiment]] = Field(None, description="Filter by sentiment")
    user_id: Optional[str] = Field(None, description="Filter by user")
    assignee: Optional[str] = Field(None, description="Filter by assignee")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    rating_min: Optional[int] = Field(None, description="Minimum rating", ge=1, le=5)
    rating_max: Optional[int] = Field(None, description="Maximum rating", ge=1, le=5)
    created_after: Optional[datetime] = Field(None, description="Created after date")
    created_before: Optional[datetime] = Field(None, description="Created before date")
    search: Optional[str] = Field(None, description="Search in title and description")
    has_github_issue: Optional[bool] = Field(None, description="Has associated GitHub issue")


class FeedbackExport(BaseModel):
    """Feedback export configuration."""
    format: str = Field(..., description="Export format", regex="^(csv|json|xlsx)$")
    filters: Optional[FeedbackFilter] = Field(None, description="Export filters")
    include_analysis: bool = Field(default=True, description="Include analysis data")
    include_comments: bool = Field(default=False, description="Include comments")
    date_range: Optional[Dict[str, datetime]] = Field(None, description="Date range for export")


class FeedbackImport(BaseModel):
    """Feedback import configuration."""
    source: str = Field(..., description="Import source (csv, json, api)")
    mapping: Dict[str, str] = Field(..., description="Field mapping configuration")
    validation_rules: List[Dict[str, Any]] = Field(default_factory=list, description="Validation rules")
    duplicate_handling: str = Field(default="skip", description="Duplicate handling strategy")


class UserFeedbackSummary(BaseModel):
    """Summary of feedback from a specific user."""
    user_id: str = Field(..., description="User identifier")
    total_feedback: int = Field(..., description="Total feedback submitted", ge=0)
    average_rating: float = Field(..., description="Average rating given", ge=0, le=5)
    feedback_by_type: Dict[str, int] = Field(..., description="Breakdown by feedback type")
    most_common_tags: List[str] = Field(..., description="Most frequently used tags")
    first_feedback: datetime = Field(..., description="First feedback timestamp")
    last_feedback: datetime = Field(..., description="Most recent feedback timestamp")
    engagement_score: float = Field(..., description="User engagement score", ge=0, le=10)


class TeamProductivity(BaseModel):
    """Team productivity metrics for feedback handling."""
    period: str = Field(..., description="Analysis period")
    total_processed: int = Field(..., description="Total feedback processed", ge=0)
    average_resolution_time: float = Field(..., description="Average resolution time in hours", ge=0)
    resolution_rate: float = Field(..., description="Resolution rate percentage", ge=0, le=100)
    team_performance: List[Dict[str, Any]] = Field(..., description="Individual team member performance")
    bottlenecks: List[Dict[str, Any]] = Field(..., description="Identified process bottlenecks")
    improvement_suggestions: List[str] = Field(..., description="Performance improvement suggestions")


class FeedbackHealthStatus(BaseModel):
    """Feedback aggregator health status."""
    status: str = Field(..., description="Overall health status")
    service: str = Field(..., description="Service name")
    database_healthy: bool = Field(..., description="Database connection status")
    redis_healthy: bool = Field(..., description="Redis connection status")
    github_integration_healthy: bool = Field(..., description="GitHub integration status")
    total_feedback: int = Field(..., description="Total feedback in system", ge=0)
    pending_analysis: int = Field(..., description="Feedback pending analysis", ge=0)
    recent_activity: int = Field(..., description="Activity in last 24 hours", ge=0)
    uptime_seconds: float = Field(..., description="Service uptime", ge=0)
    memory_usage_mb: float = Field(..., description="Memory usage in MB", ge=0)


class WebhookPayload(BaseModel):
    """Webhook notification payload."""
    event_type: str = Field(..., description="Event type")
    feedback_id: int = Field(..., description="Feedback item ID")
    feedback_data: FeedbackResponse = Field(..., description="Feedback data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Event timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional event metadata")


class APIKeyConfig(BaseModel):
    """API key configuration for external integrations."""
    name: str = Field(..., description="API key name")
    key: str = Field(..., description="API key value")
    permissions: List[str] = Field(..., description="API key permissions")
    rate_limit: int = Field(default=1000, description="Requests per hour limit")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")


class FeedbackTemplate(BaseModel):
    """Template for structured feedback collection."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Template ID")
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")
    fields: List[Dict[str, Any]] = Field(..., description="Form field definitions")
    feedback_type: FeedbackType = Field(..., description="Default feedback type")
    auto_tags: List[str] = Field(default_factory=list, description="Auto-applied tags")
    validation_rules: List[Dict[str, Any]] = Field(default_factory=list, description="Field validation rules")
    is_active: bool = Field(default=True, description="Template active status")
