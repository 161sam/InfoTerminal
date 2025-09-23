"""
Flowise Connector Models

Pydantic models for request/response schemas.
"""

from .requests import (
    AgentType,
    ChatRequest,
    ToolExecutionRequest,
    WorkflowCreateRequest,
    ConversationFilterRequest
)

from .responses import (
    ExecutionStatus,
    ToolExecutionStep,
    ChatResponse,
    ToolExecutionResponse,
    ToolInfo,
    ToolListResponse,
    WorkflowInfo,
    WorkflowListResponse,
    ConversationSummary,
    ConversationHistoryResponse,
    ConversationListResponse,
    AgentStatusResponse
)

__all__ = [
    # Request models
    "AgentType",
    "ChatRequest", 
    "ToolExecutionRequest",
    "WorkflowCreateRequest",
    "ConversationFilterRequest",
    
    # Response models
    "ExecutionStatus",
    "ToolExecutionStep",
    "ChatResponse",
    "ToolExecutionResponse",
    "ToolInfo",
    "ToolListResponse",
    "WorkflowInfo",
    "WorkflowListResponse",
    "ConversationSummary",
    "ConversationHistoryResponse",
    "ConversationListResponse",
    "AgentStatusResponse"
]
