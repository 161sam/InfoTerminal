"""
Response Models for Flowise Connector API v1

Standardized Pydantic models for all API responses.
"""

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum


class ExecutionStatus(str, Enum):
    """Status of tool or agent execution."""
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class ToolExecutionStep(BaseModel):
    """Individual step in agent execution."""
    step_number: int = Field(..., description="Sequential step number")
    tool_name: str = Field(..., description="Name of tool executed")
    parameters: Dict[str, Any] = Field(..., description="Parameters passed to tool")
    result: Any = Field(..., description="Tool execution result")
    status: ExecutionStatus = Field(..., description="Execution status")
    execution_time: float = Field(..., description="Time taken in seconds")
    error: Optional[str] = Field(None, description="Error message if failed")
    timestamp: datetime = Field(..., description="When this step was executed")


class ChatResponse(BaseModel):
    """Response model for agent chat interactions."""
    response: str = Field(..., description="Agent's response to the question")
    conversation_id: str = Field(..., description="Unique conversation identifier")
    agent_type: str = Field(..., description="Type of agent that processed the request")
    steps: List[ToolExecutionStep] = Field(
        default_factory=list,
        description="Detailed execution steps taken by the agent"
    )
    tools_used: List[str] = Field(
        default_factory=list,
        description="List of tools used during processing"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score of the response (0.0-1.0)"
    )
    execution_time: float = Field(..., description="Total execution time in seconds")
    iterations_used: int = Field(..., description="Number of tool execution iterations")
    context_updated: bool = Field(..., description="Whether conversation context was updated")
    sources: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Sources of information used in the response"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the execution"
    )


class ToolExecutionResponse(BaseModel):
    """Response model for direct tool execution."""
    success: bool = Field(..., description="Whether execution was successful")
    tool_name: str = Field(..., description="Name of the executed tool")
    result: Any = Field(..., description="Tool execution result")
    execution_time: float = Field(..., description="Execution time in seconds")
    error: Optional[str] = Field(None, description="Error message if failed")
    status: ExecutionStatus = Field(..., description="Execution status")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional execution metadata"
    )


class ToolInfo(BaseModel):
    """Information about an available tool."""
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    parameters: Dict[str, Any] = Field(..., description="Tool parameter schema")
    category: str = Field(..., description="Tool category (search, graph, nlp, etc.)")
    requires_auth: bool = Field(default=False, description="Whether tool requires authentication")
    estimated_time: Optional[float] = Field(None, description="Estimated execution time in seconds")


class ToolListResponse(BaseModel):
    """Response model for listing available tools."""
    tools: List[ToolInfo] = Field(..., description="List of available tools")
    total: int = Field(..., description="Total number of tools")
    categories: List[str] = Field(..., description="Available tool categories")


class WorkflowInfo(BaseModel):
    """Information about an agent workflow."""
    type: str = Field(..., description="Workflow type identifier")
    name: str = Field(..., description="Human-readable workflow name")
    description: str = Field(..., description="Workflow description")
    available_tools: List[str] = Field(..., description="Tools available to this workflow")
    max_iterations: int = Field(..., description="Maximum iterations allowed")
    default_temperature: float = Field(..., description="Default temperature setting")
    use_cases: List[str] = Field(
        default_factory=list,
        description="Common use cases for this workflow"
    )


class WorkflowListResponse(BaseModel):
    """Response model for listing available workflows."""
    workflows: List[WorkflowInfo] = Field(..., description="List of available workflows")
    total: int = Field(..., description="Total number of workflows")


class ConversationSummary(BaseModel):
    """Summary of a conversation."""
    conversation_id: str = Field(..., description="Conversation identifier")
    agent_type: str = Field(..., description="Agent type used")
    message_count: int = Field(..., description="Number of messages in conversation")
    tools_used: List[str] = Field(..., description="Tools used in conversation")
    created_at: datetime = Field(..., description="When conversation was created")
    last_activity: datetime = Field(..., description="Last activity timestamp")
    avg_confidence: float = Field(..., description="Average confidence score")
    total_execution_time: float = Field(..., description="Total execution time")


class ConversationHistoryResponse(BaseModel):
    """Response model for conversation history."""
    conversation_id: str = Field(..., description="Conversation identifier")
    agent_type: str = Field(..., description="Agent type used")
    messages: List[Dict[str, Any]] = Field(..., description="Conversation messages")
    execution_log: List[ToolExecutionStep] = Field(..., description="Detailed execution log")
    context: Dict[str, Any] = Field(..., description="Current conversation context")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional conversation metadata"
    )


class ConversationListResponse(BaseModel):
    """Response model for listing conversations."""
    conversations: List[ConversationSummary] = Field(..., description="List of conversations")
    total: int = Field(..., description="Total number of conversations")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    has_next: bool = Field(..., description="Whether there are more pages")


class AgentStatusResponse(BaseModel):
    """Response model for agent status information."""
    active_conversations: int = Field(..., description="Number of active conversations")
    total_executions: int = Field(..., description="Total tool executions")
    avg_response_time: float = Field(..., description="Average response time in seconds")
    success_rate: float = Field(..., description="Success rate percentage")
    most_used_tools: List[Dict[str, Any]] = Field(..., description="Most frequently used tools")
    agent_types_usage: Dict[str, int] = Field(..., description="Usage count by agent type")
    last_24h_stats: Dict[str, Any] = Field(..., description="Statistics for last 24 hours")
