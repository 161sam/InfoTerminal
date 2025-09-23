"""Minimal Flowise connector MVP for Iteration 04a (H1).

This module exposes a lightweight FastAPI application that
implements the feature set required for the Wave 4 agent MVP:

* Feature flag guard (`AGENTS_ENABLED`).
* Static tool registry exposing exactly six tools.
* Single-turn chat endpoint that issues at most one mocked tool call.
* Governance primitives: allowlist enforcement, global rate limit,
  and cancel hook stub.
* Basic safety controls (input sanitisation, max tokens/steps metadata).
* Prometheus counters for policy denials, tool calls, and rate limits.
"""

from __future__ import annotations

import os
import time
import uuid
import string
import logging
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Deque, Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, root_validator
from prometheus_client import Counter
from starlette_exporter import PrometheusMiddleware, handle_metrics

logger = logging.getLogger("flowise-connector")
logging.basicConfig(level=logging.INFO)

# ---------------------------------------------------------------------------
# Constants / Feature Flags
# ---------------------------------------------------------------------------

RATE_LIMIT_MAX_CALLS = int(os.getenv("AGENT_RATE_LIMIT_MAX", "5"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("AGENT_RATE_LIMIT_WINDOW", "60"))
MAX_STEPS = 1
MAX_TOKENS = 512

# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    parameters: Dict[str, Dict[str, Any]]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


TOOL_REGISTRY: Dict[str, ToolDefinition] = {
    "search": ToolDefinition(
        name="search",
        description="Mocked document search against the offline catalogue.",
        parameters={
            "query": {
                "type": "string",
                "description": "Full text query used for the knowledge base lookup.",
                "required": True,
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of mock results to return (default 5).",
                "required": False,
                "default": 5,
            },
        },
    ),
    "doc-entities.ner": ToolDefinition(
        name="doc-entities.ner",
        description="Run named entity recognition on provided document text.",
        parameters={
            "text": {
                "type": "string",
                "description": "Document text that should be processed by the NER model.",
                "required": True,
            },
            "language": {
                "type": "string",
                "description": "ISO language code guiding the mock NER pipeline (default 'de').",
                "required": False,
                "default": "de",
            },
        },
    ),
    "graph.query": ToolDefinition(
        name="graph.query",
        description="Execute a canned Cypher query against the offline demo graph.",
        parameters={
            "cypher": {
                "type": "string",
                "description": "Cypher statement to run.",
                "required": True,
            },
            "parameters": {
                "type": "object",
                "description": "Parameter map injected into the Cypher statement.",
                "required": False,
                "default": {},
            },
        },
    ),
    "dossier.build": ToolDefinition(
        name="dossier.build",
        description="Assemble a dossier summary using mock search and graph context.",
        parameters={
            "subject": {
                "type": "string",
                "description": "Entity or topic the dossier should cover.",
                "required": True,
            },
            "include_sources": {
                "type": "boolean",
                "description": "Toggle mock source list in the summary output.",
                "required": False,
                "default": True,
            },
        },
    ),
    "plugin-runner.run": ToolDefinition(
        name="plugin-runner.run",
        description="Invoke a mocked plugin execution via the sandbox runner.",
        parameters={
            "plugin_id": {
                "type": "string",
                "description": "Identifier of the plugin to execute (e.g. nmap.scan).",
                "required": True,
            },
            "payload": {
                "type": "object",
                "description": "Arbitrary payload forwarded to the mocked plugin invocation.",
                "required": False,
                "default": {},
            },
        },
    ),
    "video.analyze": ToolDefinition(
        name="video.analyze",
        description="Submit a video asset for offline forensic analysis.",
        parameters={
            "source_url": {
                "type": "string",
                "description": "Public or internal URL of the video asset to inspect.",
                "required": True,
            },
            "analysis_profile": {
                "type": "string",
                "description": "Selects the mocked analysis profile (default 'objects').",
                "required": False,
                "default": "objects",
            },
        },
    ),
}

ALLOWED_TOOLS = set(TOOL_REGISTRY)

# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

agent_tool_calls_total = Counter(
    "agent_tool_calls_total",
    "Total number of tool calls executed by the agent MVP.",
    labelnames=("tool",),
)
agent_policy_denied_total = Counter(
    "agent_policy_denied_total",
    "Total number of denied tool requests due to static allowlist.",
)
agent_rate_limit_block_total = Counter(
    "agent_rate_limit_block_total",
    "Total number of chat requests rejected by the global rate limit.",
)

# ---------------------------------------------------------------------------
# Rate limiter implementation
# ---------------------------------------------------------------------------


class RateLimitExceededError(RuntimeError):
    """Raised when the global rate limit budget is exhausted."""


class GlobalRateLimiter:
    def __init__(self, max_calls: int, window_seconds: int) -> None:
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._events: Deque[float] = deque()

    def reset(self) -> None:
        self._events.clear()

    def check(self) -> None:
        now = time.monotonic()
        window_start = now - self.window_seconds
        while self._events and self._events[0] < window_start:
            self._events.popleft()
        if len(self._events) >= self.max_calls:
            agent_rate_limit_block_total.inc()
            raise RateLimitExceededError(
                f"Rate limit exceeded: {self.max_calls} calls per {self.window_seconds}s"
            )
        self._events.append(now)


global_rate_limiter = GlobalRateLimiter(
    max_calls=RATE_LIMIT_MAX_CALLS,
    window_seconds=RATE_LIMIT_WINDOW_SECONDS,
)

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class ToolModel(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Dict[str, Any]]


class ToolsResponse(BaseModel):
    tools: List[ToolModel]


class ChatRequest(BaseModel):
    message: str = Field(..., description="Single user message for this turn.")
    tool: Optional[str] = Field(
        default=None,
        description="Tool to execute. Defaults to dossier.build if omitted.",
    )
    tool_params: Dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters passed to the selected tool.",
    )
    conversation_id: Optional[str] = Field(
        default=None,
        description="Client supplied conversation id for correlation.",
    )

    @root_validator(pre=True)
    def ensure_single_turn(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        message = values.get("message")
        if isinstance(message, list):
            raise ValueError("message must be a string for the MVP single-turn flow")
        return values


class ToolCall(BaseModel):
    tool: str
    params: Dict[str, Any]
    started_at: str
    finished_at: str
    result: Dict[str, Any]


class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    tool_call: Optional[ToolCall]
    steps: List[Dict[str, Any]]
    max_steps: int
    max_tokens: int


class CancelResponse(BaseModel):
    conversation_id: str
    status: str
    detail: str


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


PRINTABLE_SET = set(string.printable)


def agents_enabled() -> bool:
    return os.getenv("AGENTS_ENABLED", "0") == "1"


def require_agents_enabled() -> None:
    if not agents_enabled():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Agent features are disabled. Set AGENTS_ENABLED=1 to activate.",
        )


def sanitise_message(message: str) -> str:
    clean = "".join(ch for ch in message if ch in PRINTABLE_SET).strip()
    if not clean:
        raise HTTPException(status_code=400, detail="Message is empty after sanitisation.")
    if len(clean) > 2000:
        clean = clean[:2000]
    return clean


def resolve_tool(tool: Optional[str]) -> str:
    if tool:
        if tool not in ALLOWED_TOOLS:
            agent_policy_denied_total.inc()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Tool '{tool}' is not allowed.",
            )
        return tool
    return "dossier.build"


def execute_tool(tool_name: str, params: Dict[str, Any], prompt: str) -> ToolCall:
    start_time = datetime.utcnow()
    agent_tool_calls_total.labels(tool=tool_name).inc()

    # Mock execution payload keeps the demo deterministic and offline.
    result_payload = {
        "summary": f"Mocked {tool_name} run for '{prompt[:120]}'",
        "parameters": params,
        "notes": "Offline execution – replace with real integration in Wave 4b.",
    }

    finished_at = datetime.utcnow()
    return ToolCall(
        tool=tool_name,
        params=params,
        started_at=start_time.isoformat() + "Z",
        finished_at=finished_at.isoformat() + "Z",
        result=result_payload,
    )


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(title="InfoTerminal Agent MVP", version="0.4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    PrometheusMiddleware,
    app_name="flowise-connector-mvp",
)
app.add_route("/metrics", handle_metrics)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    response = await call_next(request)
    response.headers["X-Request-Id"] = request_id
    return response


@app.get("/healthz")
def healthz() -> Dict[str, str]:
    return {"status": "ok", "agents_enabled": str(agents_enabled())}


@app.get("/readyz")
def readyz() -> Dict[str, Any]:
    return {
        "status": "ready" if agents_enabled() else "degraded",
        "agents_enabled": agents_enabled(),
        "tool_count": len(TOOL_REGISTRY),
        "rate_limit": {
            "max_calls": RATE_LIMIT_MAX_CALLS,
            "window_seconds": RATE_LIMIT_WINDOW_SECONDS,
        },
    }


@app.get("/tools", response_model=ToolsResponse)
async def list_tools(_: None = Depends(require_agents_enabled)) -> ToolsResponse:
    tools = [ToolModel(**tool.as_dict()) for tool in TOOL_REGISTRY.values()]
    return ToolsResponse(tools=tools)


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, _: None = Depends(require_agents_enabled)) -> ChatResponse:
    prompt = sanitise_message(request.message)
    conversation_id = request.conversation_id or str(uuid.uuid4())

    try:
        global_rate_limiter.check()
    except RateLimitExceededError as exc:
        logger.warning("rate_limit_block", extra={"conversation_id": conversation_id})
        raise HTTPException(status_code=429, detail=str(exc)) from exc

    selected_tool = resolve_tool(request.tool)
    tool_definition = TOOL_REGISTRY[selected_tool]

    # Hydrate default parameters when omitted to keep schema deterministic.
    params: Dict[str, Any] = {}
    for param_name, schema in tool_definition.parameters.items():
        if param_name in request.tool_params:
            params[param_name] = request.tool_params[param_name]
        elif "default" in schema:
            params[param_name] = schema["default"]
        elif schema.get("required"):
            raise HTTPException(
                status_code=400,
                detail=f"Missing required parameter '{param_name}' for tool '{selected_tool}'",
            )

    steps: List[Dict[str, Any]] = [
        {
            "status": "started",
            "tool": selected_tool,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    ]

    tool_call = execute_tool(selected_tool, params, prompt)
    steps.append(
        {
            "status": "completed",
            "tool": selected_tool,
            "timestamp": tool_call.finished_at,
        }
    )

    reply = (
        f"Executed {selected_tool} with max {MAX_STEPS} step. "
        f"Review the mocked summary for '{params.get('subject', prompt[:60])}'."
    )

    return ChatResponse(
        conversation_id=conversation_id,
        reply=reply,
        tool_call=tool_call,
        steps=steps,
        max_steps=MAX_STEPS,
        max_tokens=MAX_TOKENS,
    )


@app.post("/chat/{conversation_id}/cancel", response_model=CancelResponse)
async def cancel_chat(conversation_id: str) -> CancelResponse:
    logger.info("cancel_requested", extra={"conversation_id": conversation_id})
    return CancelResponse(
        conversation_id=conversation_id,
        status="cancelled",
        detail="Execution cancelled (stub – no running tasks in MVP).",
    )


@app.get("/info")
def info() -> Dict[str, Any]:
    return {
        "service": "flowise-connector",
        "version": "0.4.0",
        "agents_enabled": agents_enabled(),
        "tools": list(ALLOWED_TOOLS),
        "rate_limit": {
            "max_calls": RATE_LIMIT_MAX_CALLS,
            "window_seconds": RATE_LIMIT_WINDOW_SECONDS,
        },
    }


# Export utility symbols for tests
__all__ = [
    "TOOL_REGISTRY",
    "global_rate_limiter",
    "agent_tool_calls_total",
    "agent_policy_denied_total",
    "agent_rate_limit_block_total",
    "MAX_STEPS",
    "MAX_TOKENS",
    "app",
]
