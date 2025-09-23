"""
Feedback Aggregator Service Models

Comprehensive Pydantic models for user feedback collection, analysis, and management.
Includes models for feedback submission, voting, analytics, and external integrations.
"""

from .requests import (
    # Enums
    FeedbackType,
    Priority,
    Status,
    Sentiment,
    VoteType,
    
    # Core models
    FeedbackCreate,
    FeedbackUpdate,
    FeedbackResponse,
    VoteCreate,
    VoteResponse,
    
    # Analytics and statistics
    FeedbackStats,
    FeedbackTrends,
    FeedbackAnalysis,
    UserFeedbackSummary,
    TeamProductivity,
    
    # Operations
    BulkFeedbackOperation,
    BulkOperationResult,
    FeedbackFilter,
    FeedbackExport,
    FeedbackImport,
    
    # Integrations
    GitHubIntegration,
    NotificationConfig,
    WebhookPayload,
    APIKeyConfig,
    
    # Templates and configuration
    FeedbackTemplate,
    
    # Health and monitoring
    FeedbackHealthStatus,
)

__all__ = [
    # Enums
    "FeedbackType",
    "Priority",
    "Status", 
    "Sentiment",
    "VoteType",
    
    # Core feedback operations
    "FeedbackCreate",
    "FeedbackUpdate",
    "FeedbackResponse",
    "VoteCreate",
    "VoteResponse",
    
    # Analytics
    "FeedbackStats",
    "FeedbackTrends",
    "FeedbackAnalysis",
    "UserFeedbackSummary",
    "TeamProductivity",
    
    # Bulk operations
    "BulkFeedbackOperation",
    "BulkOperationResult",
    "FeedbackFilter",
    "FeedbackExport",
    "FeedbackImport",
    
    # Integrations
    "GitHubIntegration",
    "NotificationConfig",
    "WebhookPayload",
    "APIKeyConfig",
    
    # Templates
    "FeedbackTemplate",
    
    # Monitoring
    "FeedbackHealthStatus",
]
