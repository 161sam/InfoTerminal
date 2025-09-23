"""
Request Models for Flowise Connector API v1

Standardized Pydantic models for all incoming requests.
"""

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from enum import Enum


class AgentType(str, Enum):
    """Available agent types for workflows."""
    RESEARCH_ASSISTANT = "research_assistant"
    GRAPH_ANALYST = "graph_analyst"
    SECURITY_ANALYST = "security_analyst"
    GEOSPATIAL_ANALYST = "geospatial_analyst"
    PERSON_INVESTIGATION = "person_investigation"
    FINANCIAL_RISK_ANALYSIS = "financial_risk_analysis"


class ChatRequest(BaseModel):
    """Request model for agent chat interactions."""
    question: str = Field(
        ..., 
        description="Question or task for the agent to process",
        min_length=1,
        max_length=5000
    )
    agent_type: AgentType = Field(
        default=AgentType.RESEARCH_ASSISTANT,
        description="Type of agent to use for processing"
    )
    context: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional context for the agent (previous conversation, documents, etc.)"
    )
    max_iterations: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of tool execution iterations allowed"
    )
    tools_allowed: List[str] = Field(
        default_factory=list,
        description="Specific tools the agent is allowed to use (empty = all tools)"
    )
    conversation_id: Optional[str] = Field(
        None,
        description="ID of existing conversation to continue (auto-generated if not provided)"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Creativity/randomness of agent responses (0.0 = deterministic, 2.0 = very creative)"
    )


class ToolExecutionRequest(BaseModel):
    """Request model for direct tool execution."""
    tool_name: str = Field(
        ...,
        description="Name of the tool to execute",
        min_length=1
    )
    parameters: Dict[str, Any] = Field(
        ...,
        description="Parameters to pass to the tool"
    )
    context: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional context for tool execution"
    )
    timeout: Optional[int] = Field(
        default=30,
        ge=1,
        le=300,
        description="Execution timeout in seconds"
    )


class WorkflowCreateRequest(BaseModel):
    """Request model for creating custom agent workflows."""
    name: str = Field(
        ...,
        description="Unique name for the workflow",
        min_length=1,
        max_length=100
    )
    description: str = Field(
        ...,
        description="Description of what the workflow does",
        min_length=1,
        max_length=500
    )
    agent_type: str = Field(
        ...,
        description="Base agent type to extend",
        min_length=1
    )
    system_prompt: str = Field(
        ...,
        description="Custom system prompt for the agent",
        min_length=1,
        max_length=2000
    )
    available_tools: List[str] = Field(
        ...,
        description="List of tools available to this workflow"
    )
    max_iterations: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum iterations for this workflow"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Default temperature for this workflow"
    )


class ConversationFilterRequest(BaseModel):
    """Request model for filtering conversation history."""
    since: Optional[str] = Field(
        None,
        description="ISO timestamp to filter conversations since"
    )
    agent_type: Optional[AgentType] = Field(
        None,
        description="Filter by agent type"
    )
    tools_used: Optional[List[str]] = Field(
        None,
        description="Filter by tools that were used"
    )
    min_confidence: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Filter by minimum confidence score"
    )
