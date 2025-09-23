"""
Flowise Connector Agents Router - v1 API

Standardized agent orchestration endpoints for InfoTerminal.
"""

import os
import sys
import uuid
import asyncio
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Add shared standards to Python path
SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import JSONResponse

from _shared.api_standards import (
    PaginatedResponse,
    PaginationParams,
    APIError,
    ErrorCodes,
    StandardError
)

from ..models import (
    ChatRequest,
    ChatResponse,
    ToolExecutionRequest,
    ToolExecutionResponse,
    ToolListResponse,
    WorkflowListResponse,
    ConversationHistoryResponse,
    ConversationListResponse,
    AgentStatusResponse,
    ToolInfo,
    WorkflowInfo,
    AgentType
)

# Import the existing agent execution logic
from ..app.main import AgentExecution, agent_sessions

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with AI Agent",
    description="Send a question or task to an AI agent for processing with tool orchestration"
)
async def chat_with_agent(request: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint for agent interactions.
    
    Processes natural language questions using specialized AI agents that can:
    - Execute research tasks
    - Query graph databases  
    - Analyze documents
    - Perform geospatial analysis
    - Run security investigations
    
    The agent will automatically select and execute appropriate tools based on the question.
    """
    try:
        # Generate or use existing conversation ID
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Get or create agent session
        if conversation_id not in agent_sessions:
            agent_sessions[conversation_id] = AgentExecution(conversation_id)
        
        agent = agent_sessions[conversation_id]
        
        # Execute agent workflow
        start_time = datetime.now()
        response = await agent.execute_agent_workflow(request)
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Convert to standardized response format
        return ChatResponse(
            response=response.get("response", ""),
            conversation_id=conversation_id,
            agent_type=request.agent_type.value,
            steps=response.get("steps", []),
            tools_used=response.get("tools_used", []),
            confidence=response.get("confidence", 0.8),
            execution_time=execution_time,
            iterations_used=response.get("iterations_used", 0),
            context_updated=True,
            sources=response.get("sources", []),
            metadata=response.get("metadata", {})
        )
        
    except ValueError as e:
        raise APIError(
            code=ErrorCodes.VALIDATION_ERROR,
            message=str(e),
            status_code=400,
            details={"agent_type": request.agent_type.value}
        )
    except TimeoutError as e:
        raise APIError(
            code=ErrorCodes.TIMEOUT_ERROR,
            message="Agent execution timed out",
            status_code=408,
            details={"max_iterations": request.max_iterations}
        )
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Agent execution failed",
            status_code=500,
            details={"error": str(e)}
        )


@router.post(
    "/execute",
    response_model=ToolExecutionResponse,
    summary="Execute Single Tool",
    description="Execute a specific tool directly without agent orchestration"
)
async def execute_tool(request: ToolExecutionRequest) -> ToolExecutionResponse:
    """
    Execute a single tool directly.
    
    Useful for:
    - Testing individual tools
    - Building custom workflows
    - Direct API integration
    """
    try:
        agent = AgentExecution()
        
        start_time = datetime.now()
        result = await agent.execute_tool(request.tool_name, request.parameters)
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return ToolExecutionResponse(
            success=result.get("success", False),
            tool_name=request.tool_name,
            result=result.get("result"),
            execution_time=execution_time,
            error=result.get("error"),
            status="success" if result.get("success") else "failed",
            metadata=result.get("metadata", {})
        )
        
    except ValueError as e:
        raise APIError(
            code=ErrorCodes.VALIDATION_ERROR,
            message=f"Invalid tool or parameters: {str(e)}",
            status_code=400,
            details={"tool_name": request.tool_name}
        )
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Tool execution failed",
            status_code=500,
            details={"tool_name": request.tool_name, "error": str(e)}
        )


@router.get(
    "/tools",
    response_model=ToolListResponse,
    summary="List Available Tools",
    description="Get list of all tools available for agent workflows"
)
async def list_tools() -> ToolListResponse:
    """
    List all available tools for agent workflows.
    
    Tools are organized by category:
    - search: Document and web search tools
    - graph: Graph database and analytics tools  
    - nlp: Natural language processing tools
    - geo: Geospatial analysis tools
    - forensics: Digital forensics tools
    - osint: Open source intelligence tools
    """
    try:
        agent = AgentExecution()
        tools_info = []
        categories = set()
        
        for tool_name, tool_config in agent.available_tools.items():
            category = tool_config.get("category", "general")
            categories.add(category)
            
            tool_info = ToolInfo(
                name=tool_name,
                description=tool_config["description"],
                parameters=tool_config["parameters"],
                category=category,
                requires_auth=tool_config.get("requires_auth", False),
                estimated_time=tool_config.get("estimated_time")
            )
            tools_info.append(tool_info)
        
        return ToolListResponse(
            tools=tools_info,
            total=len(tools_info),
            categories=sorted(list(categories))
        )
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve tools",
            status_code=500,
            details={"error": str(e)}
        )


@router.get(
    "/workflows",
    response_model=WorkflowListResponse,
    summary="List Agent Workflows",
    description="Get list of available agent workflow types and their capabilities"
)
async def list_workflows() -> WorkflowListResponse:
    """
    List available agent workflow types.
    
    Each workflow is specialized for different types of tasks:
    - research_assistant: General research and analysis
    - graph_analyst: Graph database analysis and visualization
    - security_analyst: Security investigations and threat analysis
    - geospatial_analyst: Geographic and location-based analysis
    - person_investigation: Person-focused OSINT investigations
    - financial_risk_analysis: Financial analysis and risk assessment
    """
    try:
        agent = AgentExecution()
        workflows = []
        
        workflow_types = [
            "research_assistant",
            "graph_analyst", 
            "security_analyst",
            "geospatial_analyst",
            "person_investigation",
            "financial_risk_analysis"
        ]
        
        for agent_type in workflow_types:
            workflow_config = agent._get_workflow(agent_type)
            
            workflow_info = WorkflowInfo(
                type=agent_type,
                name=agent_type.replace("_", " ").title(),
                description=workflow_config["system_prompt"][:200] + "...",
                available_tools=workflow_config["available_tools"],
                max_iterations=workflow_config.get("max_iterations", 10),
                default_temperature=workflow_config.get("temperature", 0.7),
                use_cases=workflow_config.get("use_cases", [])
            )
            workflows.append(workflow_info)
        
        return WorkflowListResponse(
            workflows=workflows,
            total=len(workflows)
        )
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve workflows",
            status_code=500,
            details={"error": str(e)}
        )


@router.get(
    "/conversations",
    response_model=ConversationListResponse,
    summary="List Conversations",
    description="Get paginated list of agent conversations with filtering options"
)
async def list_conversations(
    pagination: PaginationParams = Depends(),
    agent_type: Optional[AgentType] = Query(None, description="Filter by agent type"),
    since: Optional[str] = Query(None, description="Filter conversations since ISO timestamp")
) -> ConversationListResponse:
    """
    List agent conversations with optional filtering.
    
    Supports filtering by:
    - Agent type used
    - Time range (since parameter)
    - Pagination for large result sets
    """
    try:
        # This is a simplified implementation - in production you'd use a proper database
        conversations = []
        total = len(agent_sessions)
        
        # Apply pagination (simplified)
        offset = (pagination.page - 1) * pagination.size
        paginated_sessions = list(agent_sessions.items())[offset:offset + pagination.size]
        
        for conversation_id, agent in paginated_sessions:
            # Create conversation summary (simplified)
            conversations.append({
                "conversation_id": conversation_id,
                "agent_type": "research_assistant",  # Would get from agent session
                "message_count": len(agent.execution_log),
                "tools_used": [],
                "created_at": datetime.now(),
                "last_activity": datetime.now(),
                "avg_confidence": 0.8,
                "total_execution_time": 0.0
            })
        
        return ConversationListResponse(
            conversations=conversations,
            total=total,
            page=pagination.page,
            size=pagination.size,
            has_next=pagination.page * pagination.size < total
        )
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve conversations",
            status_code=500,
            details={"error": str(e)}
        )


@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationHistoryResponse,
    summary="Get Conversation History",
    description="Retrieve detailed history and context of a specific conversation"
)
async def get_conversation(conversation_id: str) -> ConversationHistoryResponse:
    """
    Get detailed conversation history.
    
    Returns:
    - All messages in the conversation
    - Detailed execution log with tool usage
    - Current conversation context
    - Metadata about the conversation
    """
    try:
        if conversation_id not in agent_sessions:
            raise APIError(
                code=ErrorCodes.RESOURCE_NOT_FOUND,
                message=f"Conversation {conversation_id} not found",
                status_code=404,
                details={"conversation_id": conversation_id}
            )
        
        agent = agent_sessions[conversation_id]
        
        return ConversationHistoryResponse(
            conversation_id=conversation_id,
            agent_type="research_assistant",  # Would get from agent session
            messages=[],  # Would get from agent session
            execution_log=agent.execution_log,
            context=agent.context,
            metadata={}
        )
        
    except APIError:
        raise
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve conversation",
            status_code=500,
            details={"conversation_id": conversation_id, "error": str(e)}
        )


@router.delete(
    "/conversations/{conversation_id}",
    summary="Delete Conversation",
    description="Clear conversation history and remove from memory"
)
async def delete_conversation(conversation_id: str) -> JSONResponse:
    """
    Clear conversation history and context.
    
    This removes the conversation from active memory but does not delete
    any persistent conversation logs (if enabled).
    """
    try:
        if conversation_id in agent_sessions:
            del agent_sessions[conversation_id]
            
        return JSONResponse(
            content={"message": f"Conversation {conversation_id} deleted successfully"},
            status_code=200
        )
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to delete conversation",
            status_code=500,
            details={"conversation_id": conversation_id, "error": str(e)}
        )


@router.get(
    "/status",
    response_model=AgentStatusResponse,
    summary="Agent System Status",
    description="Get current status and statistics of the agent system"
)
async def get_agent_status() -> AgentStatusResponse:
    """
    Get agent system status and statistics.
    
    Provides insights into:
    - Active conversation count
    - Tool execution statistics
    - Performance metrics
    - Usage patterns
    """
    try:
        # This is a simplified implementation - in production you'd track these metrics properly
        return AgentStatusResponse(
            active_conversations=len(agent_sessions),
            total_executions=sum(len(agent.execution_log) for agent in agent_sessions.values()),
            avg_response_time=2.5,  # Would calculate from actual data
            success_rate=95.0,  # Would calculate from actual data
            most_used_tools=[
                {"tool": "search_documents", "count": 150},
                {"tool": "query_graph", "count": 120},
                {"tool": "analyze_text", "count": 100}
            ],
            agent_types_usage={
                "research_assistant": 80,
                "graph_analyst": 45,
                "security_analyst": 30
            },
            last_24h_stats={
                "conversations": 25,
                "tool_executions": 120,
                "avg_response_time": 2.1
            }
        )
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve agent status",
            status_code=500,
            details={"error": str(e)}
        )
