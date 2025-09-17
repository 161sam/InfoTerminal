import logging
import os
import time
import json
import asyncio
from typing import Any, Dict, Optional, List
from datetime import datetime
import uuid

import httpx
from fastapi import FastAPI, Header, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.requests import Request
from starlette_exporter import PrometheusMiddleware, handle_metrics
from pydantic import BaseModel

try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
except Exception:  # pragma: no cover - optional dependency
    FastAPIInstrumentor = None

from .errors import AgentUpstreamError, WorkflowTriggerError
from .http_client import request as http_request
from .it_logging import setup_logging

# Configuration
AGENT_BASE_URL = os.getenv("AGENT_BASE_URL", "http://localhost:3417")
FLOWISE_API_KEY = os.getenv("FLOWISE_API_KEY", "")
N8N_BASE = os.getenv("N8N_BASE_URL")
N8N_KEY = os.getenv("N8N_API_KEY")
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK_URL")

# Service URLs
SEARCH_API_URL = f"http://localhost:{os.getenv('IT_PORT_SEARCH_API', '8611')}"
GRAPH_API_URL = f"http://localhost:{os.getenv('IT_PORT_GRAPH_API', '8612')}"
DOC_ENTITIES_URL = f"http://localhost:{os.getenv('IT_PORT_DOC_ENTITIES', '8613')}"
VERIFICATION_URL = f"http://localhost:{os.getenv('IT_PORT_VERIFICATION', '8617')}"
PLUGIN_RUNNER_URL = f"http://localhost:{os.getenv('IT_PORT_PLUGIN_RUNNER', '8621')}"
MEDIA_FORENSICS_URL = f"http://localhost:{os.getenv('IT_PORT_MEDIA_FORENSICS', '8618')}"

logger = logging.getLogger("flowise-connector")

app = FastAPI(
    title="InfoTerminal Agent Orchestrator", 
    description="AI Agent workflow orchestration for OSINT operations",
    version="0.2.0"
)
setup_logging(app, "flowise-connector")
if os.getenv("IT_ENABLE_METRICS") == "1":
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", handle_metrics)

if FastAPIInstrumentor:
    try:
        FastAPIInstrumentor.instrument_app(app)
    except Exception:
        pass

# Pydantic Models
class ChatRequest(BaseModel):
    question: str
    agent_type: str = "research_assistant"
    context: Optional[Dict[str, Any]] = None
    max_iterations: int = 10
    tools_allowed: List[str] = []
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    steps: List[Dict[str, Any]]
    tools_used: List[str]
    confidence: float
    execution_time: float
    conversation_id: str

class ToolExecutionRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None

class ToolExecutionResponse(BaseModel):
    success: bool
    result: Any
    error: Optional[str] = None
    execution_time: float

class AgentWorkflow(BaseModel):
    name: str
    description: str
    agent_type: str
    system_prompt: str
    available_tools: List[str]
    max_iterations: int = 10
    temperature: float = 0.7

class AgentExecution:
    """Enhanced agent execution with comprehensive tool integration."""
    
    def __init__(self, session_id: str = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.execution_log = []
        self.context = {}
        self.available_tools = self._get_available_tools()
        self.http_client = httpx.AsyncClient(timeout=30.0)
    
    def _get_available_tools(self) -> Dict[str, Dict]:
        """Define comprehensive tool set for agent workflows."""
        return {
            "search_documents": {
                "description": "Search documents in the knowledge base using semantic search",
                "parameters": {
                    "query": {"type": "string", "description": "Search query"},
                    "filters": {"type": "object", "description": "Search filters", "optional": True},
                    "limit": {"type": "integer", "description": "Max results", "default": 10}
                },
                "endpoint": f"{SEARCH_API_URL}/query",
                "method": "POST"
            },
            "extract_entities": {
                "description": "Extract named entities from text using NLP models",
                "parameters": {
                    "text": {"type": "string", "description": "Text to analyze"},
                    "lang": {"type": "string", "description": "Language code", "default": "en"}
                },
                "endpoint": f"{DOC_ENTITIES_URL}/ner",
                "method": "POST"
            },
            "analyze_document": {
                "description": "Perform comprehensive document analysis including NER and relation extraction",
                "parameters": {
                    "text": {"type": "string", "description": "Document text"},
                    "title": {"type": "string", "description": "Document title", "optional": True},
                    "extract_relations": {"type": "boolean", "description": "Extract relations", "default": True},
                    "do_summary": {"type": "boolean", "description": "Generate summary", "default": False}
                },
                "endpoint": f"{DOC_ENTITIES_URL}/annotate",
                "method": "POST"
            },
            "query_graph": {
                "description": "Query the knowledge graph using Cypher queries",
                "parameters": {
                    "cypher": {"type": "string", "description": "Cypher query"},
                    "limit": {"type": "integer", "description": "Max results", "default": 50}
                },
                "endpoint": f"{GRAPH_API_URL}/query",
                "method": "POST"
            },
            "get_neighbors": {
                "description": "Find neighboring nodes in the knowledge graph",
                "parameters": {
                    "node_id": {"type": "string", "description": "Node ID"},
                    "limit": {"type": "integer", "description": "Max results", "default": 20}
                },
                "endpoint": f"{GRAPH_API_URL}/neighbors",
                "method": "GET"
            },
            "analyze_centrality": {
                "description": "Perform centrality analysis on graph nodes",
                "parameters": {
                    "centrality_type": {"type": "string", "description": "Type: degree or betweenness", "default": "degree"},
                    "node_type": {"type": "string", "description": "Filter by node type", "optional": True},
                    "limit": {"type": "integer", "description": "Max results", "default": 20}
                },
                "endpoint": f"{GRAPH_API_URL}/analytics/centrality/{{centrality_type}}",
                "method": "GET"
            },
            "detect_communities": {
                "description": "Detect communities in the knowledge graph",
                "parameters": {
                    "algorithm": {"type": "string", "description": "Algorithm: louvain", "default": "louvain"},
                    "min_community_size": {"type": "integer", "description": "Min community size", "default": 3}
                },
                "endpoint": f"{GRAPH_API_URL}/analytics/communities",
                "method": "POST"
            },
            "verify_information": {
                "description": "Verify claims and information using multiple sources",
                "parameters": {
                    "claim": {"type": "string", "description": "Claim to verify"},
                    "context": {"type": "string", "description": "Additional context", "optional": True}
                },
                "endpoint": f"{VERIFICATION_URL}/verify",
                "method": "POST"
            },
            "run_security_scan": {
                "description": "Execute security scanning tools (nmap, whois, etc.)",
                "parameters": {
                    "plugin_name": {"type": "string", "description": "Tool name: nmap, whois, subfinder"},
                    "target": {"type": "string", "description": "Target IP, domain, or host"},
                    "scan_type": {"type": "string", "description": "Scan type", "default": "basic"},
                    "timeout": {"type": "integer", "description": "Timeout in seconds", "default": 300}
                },
                "endpoint": f"{PLUGIN_RUNNER_URL}/execute",
                "method": "POST"
            },
            "analyze_image": {
                "description": "Perform forensic analysis on images (EXIF, hashing, etc.)",
                "parameters": {
                    "image_url": {"type": "string", "description": "URL or path to image", "optional": True},
                    "include_reverse_search": {"type": "boolean", "description": "Include reverse image search", "default": False}
                },
                "endpoint": f"{MEDIA_FORENSICS_URL}/image/analyze",
                "method": "POST"
            },
            "geocode_location": {
                "description": "Convert location names to coordinates",
                "parameters": {
                    "location": {"type": "string", "description": "Location name"},
                    "country_code": {"type": "string", "description": "Country code", "optional": True}
                },
                "endpoint": f"{GRAPH_API_URL}/geo/geocode",
                "method": "POST"
            },
            "find_geo_entities": {
                "description": "Find entities within a geographic area",
                "parameters": {
                    "south": {"type": "number", "description": "Southern boundary"},
                    "west": {"type": "number", "description": "Western boundary"}, 
                    "north": {"type": "number", "description": "Northern boundary"},
                    "east": {"type": "number", "description": "Eastern boundary"},
                    "limit": {"type": "integer", "description": "Max results", "default": 50}
                },
                "endpoint": f"{GRAPH_API_URL}/geo/entities",
                "method": "GET"
            },
            "generate_dossier": {
                "description": "Generate comprehensive dossier for an entity or topic",
                "parameters": {
                    "entity_name": {"type": "string", "description": "Entity name or topic"},
                    "entity_type": {"type": "string", "description": "Entity type", "optional": True},
                    "include_graph": {"type": "boolean", "description": "Include graph analysis", "default": True},
                    "include_timeline": {"type": "boolean", "description": "Include timeline", "default": True}
                },
                "endpoint": f"{SEARCH_API_URL}/dossier",
                "method": "POST"
            }
        }
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> ToolExecutionResponse:
        """Execute a specific tool with given parameters."""
        start_time = time.time()
        
        if tool_name not in self.available_tools:
            return ToolExecutionResponse(
                success=False,
                result=None,
                error=f"Unknown tool: {tool_name}",
                execution_time=time.time() - start_time
            )
        
        tool_config = self.available_tools[tool_name]
        
        try:
            # Prepare request
            endpoint = tool_config["endpoint"]
            method = tool_config.get("method", "POST")
            
            # Handle URL templating (e.g., for centrality_type)
            if "{" in endpoint and "}" in endpoint:
                endpoint = endpoint.format(**parameters)
            
            # Prepare request data
            if method == "GET":
                response = await self.http_client.get(endpoint, params=parameters)
            elif method == "POST":
                response = await self.http_client.post(endpoint, json=parameters)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            if response.status_code >= 400:
                raise httpx.HTTPStatusError(
                    f"Tool execution failed: {response.status_code}",
                    request=response.request,
                    response=response
                )
            
            result = response.json()
            
            # Log execution
            self.execution_log.append({
                "tool": tool_name,
                "parameters": parameters,
                "result_summary": str(result)[:200] + "..." if len(str(result)) > 200 else str(result),
                "timestamp": datetime.utcnow().isoformat(),
                "execution_time": time.time() - start_time
            })
            
            return ToolExecutionResponse(
                success=True,
                result=result,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"Tool execution failed for {tool_name}: {str(e)}")
            return ToolExecutionResponse(
                success=False,
                result=None,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    async def execute_agent_workflow(self, request: ChatRequest) -> ChatResponse:
        """Execute complete agent workflow with LLM integration."""
        start_time = time.time()
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Get predefined workflow
        workflow = self._get_workflow(request.agent_type)
        
        steps = []
        tools_used = []
        
        try:
            # Initial LLM call to understand the request
            llm_response = await self._call_flowise_agent(
                message=request.question,
                conversation_id=conversation_id,
                system_prompt=workflow["system_prompt"],
                available_tools=workflow["available_tools"]
            )
            
            # Extract tool calls from LLM response
            tool_calls = self._extract_tool_calls(llm_response)
            
            # Execute tools
            tool_results = {}
            for tool_call in tool_calls:
                tool_name = tool_call["tool"]
                parameters = tool_call["parameters"]
                
                if tool_name in request.tools_allowed or not request.tools_allowed:
                    result = await self.execute_tool(tool_name, parameters)
                    tool_results[tool_name] = result.result if result.success else result.error
                    tools_used.append(tool_name)
                    
                    steps.append({
                        "type": "tool_execution",
                        "tool": tool_name,
                        "parameters": parameters,
                        "result": result.result if result.success else None,
                        "error": result.error,
                        "timestamp": datetime.utcnow().isoformat()
                    })
            
            # Final LLM call with tool results
            final_context = {
                "original_question": request.question,
                "tool_results": tool_results,
                "context": request.context or {}
            }
            
            final_response = await self._call_flowise_agent(
                message=f"Based on the tool results, provide a comprehensive answer: {json.dumps(final_context)}",
                conversation_id=conversation_id,
                system_prompt="Synthesize the information and provide a clear, actionable response."
            )
            
            return ChatResponse(
                response=final_response,
                steps=steps,
                tools_used=tools_used,
                confidence=0.8,  # TODO: Implement confidence scoring
                execution_time=time.time() - start_time,
                conversation_id=conversation_id
            )
            
        except Exception as e:
            logger.error(f"Agent workflow execution failed: {str(e)}")
            return ChatResponse(
                response=f"I encountered an error while processing your request: {str(e)}",
                steps=steps,
                tools_used=tools_used,
                confidence=0.0,
                execution_time=time.time() - start_time,
                conversation_id=conversation_id
            )
    
    async def _call_flowise_agent(self, message: str, conversation_id: str, 
                                 system_prompt: str = "", available_tools: List[str] = None) -> str:
        """Call Flowise API for LLM processing."""
        try:
            payload = {
                "question": message,
                "overrideConfig": {
                    "systemMessage": system_prompt,
                    "conversationId": conversation_id
                }
            }
            
            if available_tools:
                payload["overrideConfig"]["availableTools"] = available_tools
            
            headers = {}
            if FLOWISE_API_KEY:
                headers["Authorization"] = f"Bearer {FLOWISE_API_KEY}"
            
            response = await self.http_client.post(
                f"{AGENT_BASE_URL}/api/v1/prediction/your-chatflow-id",  # TODO: Make configurable
                json=payload,
                headers=headers
            )
            
            if response.status_code != 200:
                raise AgentUpstreamError(f"Flowise API error: {response.status_code}")
            
            data = response.json()
            return data.get("text", "No response from agent")
            
        except Exception as e:
            logger.error(f"Flowise API call failed: {str(e)}")
            return f"Agent communication error: {str(e)}"
    
    def _extract_tool_calls(self, llm_response: str) -> List[Dict[str, Any]]:
        """Extract tool calls from LLM response."""
        # Simple pattern matching for tool calls
        # In production, this would use proper function calling with structured output
        tool_calls = []
        
        # Look for patterns like "search_documents(query='example')"
        import re
        pattern = r'(\w+)\((.*?)\)'
        matches = re.findall(pattern, llm_response)
        
        for tool_name, params_str in matches:
            if tool_name in self.available_tools:
                try:
                    # Simple parameter parsing - in production use proper parsing
                    parameters = {}
                    if params_str:
                        # Basic parsing for key=value pairs
                        for param in params_str.split(','):
                            if '=' in param:
                                key, value = param.split('=', 1)
                                key = key.strip().strip("'\"")
                                value = value.strip().strip("'\"")
                                parameters[key] = value
                    
                    tool_calls.append({
                        "tool": tool_name,
                        "parameters": parameters
                    })
                except Exception as e:
                    logger.warning(f"Failed to parse tool call {tool_name}: {e}")
        
        return tool_calls
    
    def _get_workflow(self, agent_type: str) -> Dict[str, Any]:
        """Get predefined agent workflow configuration."""
        workflows = {
            "research_assistant": {
                "system_prompt": """You are an OSINT research assistant. Your goal is to help users gather, analyze, and synthesize information from multiple sources. 

Available tools:
- search_documents: Search the knowledge base
- extract_entities: Extract named entities from text  
- analyze_document: Comprehensive document analysis
- query_graph: Query knowledge graph with Cypher
- get_neighbors: Find related entities in graph
- verify_information: Verify claims against sources

When a user asks a question, think step by step:
1. Search for relevant information
2. Extract key entities and relationships
3. Cross-reference with knowledge graph
4. Verify important claims
5. Synthesize findings into a comprehensive response

Be precise, cite sources, and highlight confidence levels.""",
                "available_tools": ["search_documents", "extract_entities", "analyze_document", "query_graph", "get_neighbors", "verify_information"]
            },
            "graph_analyst": {
                "system_prompt": """You are a network analysis expert specializing in knowledge graphs and relationship mapping.

Use graph analytics tools to:
- Identify key nodes and relationships
- Discover communities and clusters  
- Analyze centrality and influence patterns
- Map network structures and pathways

Focus on uncovering hidden connections and providing network insights.""",
                "available_tools": ["query_graph", "get_neighbors", "analyze_centrality", "detect_communities"]
            },
            "security_analyst": {
                "system_prompt": """You are a cybersecurity analyst focused on reconnaissance and security assessment.

Use security tools to:
- Perform network reconnaissance
- Analyze domains and infrastructure
- Assess security posture
- Identify potential vulnerabilities

Always follow responsible disclosure practices.""",
                "available_tools": ["run_security_scan", "verify_information", "analyze_document"]
            },
            "geospatial_analyst": {
                "system_prompt": """You are a geospatial intelligence analyst specializing in location-based investigations.

Use geographic tools to:
- Geocode locations and addresses
- Find entities within geographic areas
- Analyze spatial relationships
- Map geographic patterns

Combine geographic and network analysis for comprehensive insights.""",
                "available_tools": ["geocode_location", "find_geo_entities", "query_graph", "analyze_document"]
            }
        }
        
        return workflows.get(agent_type, workflows["research_assistant"])

# Global agent execution manager
agent_sessions = {}

@app.get("/healthz")
async def health_check():
    return {"status": "healthy"}

@app.get("/readyz")
async def readiness_check():
    return {"status": "ready", "services": ["flowise", "tools"]}

@app.get("/tools")
async def list_available_tools():
    """List all available tools for agent workflows."""
    agent = AgentExecution()
    tools_info = []
    
    for tool_name, tool_config in agent.available_tools.items():
        tools_info.append({
            "name": tool_name,
            "description": tool_config["description"],
            "parameters": tool_config["parameters"]
        })
    
    return {
        "tools": tools_info,
        "total": len(tools_info)
    }

@app.post("/tools/execute")
async def execute_single_tool(request: ToolExecutionRequest):
    """Execute a single tool directly."""
    agent = AgentExecution()
    result = await agent.execute_tool(request.tool_name, request.parameters)
    return result

@app.post("/chat")
async def chat_with_agent(request: ChatRequest):
    """Main chat endpoint for agent interactions."""
    session_id = request.conversation_id or str(uuid.uuid4())
    
    if session_id not in agent_sessions:
        agent_sessions[session_id] = AgentExecution(session_id)
    
    agent = agent_sessions[session_id]
    response = await agent.execute_agent_workflow(request)
    
    return response

@app.get("/conversations/{conversation_id}/history")
async def get_conversation_history(conversation_id: str):
    """Get conversation execution history."""
    if conversation_id not in agent_sessions:
        raise HTTPException(404, "Conversation not found")
    
    agent = agent_sessions[conversation_id]
    return {
        "conversation_id": conversation_id,
        "execution_log": agent.execution_log,
        "context": agent.context
    }

@app.delete("/conversations/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """Clear conversation history and context."""
    if conversation_id in agent_sessions:
        del agent_sessions[conversation_id]
    
    return {"message": "Conversation cleared"}

@app.get("/workflows")
async def list_workflows():
    """List available agent workflow types."""
    agent = AgentExecution()
    workflows = []
    
    for agent_type in ["research_assistant", "graph_analyst", "security_analyst", "geospatial_analyst"]:
        workflow = agent._get_workflow(agent_type)
        workflows.append({
            "type": agent_type,
            "description": workflow["system_prompt"][:200] + "...",
            "available_tools": workflow["available_tools"]
        })
    
    return {
        "workflows": workflows,
        "total": len(workflows)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
