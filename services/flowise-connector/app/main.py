"""Minimal Flowise connector MVP for Iteration 04a (H1).

This module exposes a lightweight FastAPI application that
implements the feature set required for the Wave 4 agent MVP:

* Feature flag guard (`AGENTS_ENABLED`).
* Static tool registry exposing exactly six tools.
* Single-turn chat endpoint that issues at most one mocked tool call.
* Governance primitives: OPA-backed policy enforcement, rate limits, and
  cancel hook stub.
* Basic safety controls (input sanitisation, max tokens/steps metadata).
* Prometheus metrics for policy denials, tool calls, rate-limit blocks, and
  mocked tool execution latency.
"""

from __future__ import annotations

import hashlib
import os
import time
import uuid
import string
import logging
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Deque, Dict, List, Optional, Tuple

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, root_validator
from prometheus_client import Counter, Histogram
from starlette.responses import JSONResponse
from starlette_exporter import PrometheusMiddleware, handle_metrics

from app.policy import PolicyDecision, policy_engine

logger = logging.getLogger("flowise-connector")
logging.basicConfig(level=logging.INFO)

# ---------------------------------------------------------------------------
# Constants / Feature Flags
# ---------------------------------------------------------------------------

RATE_LIMIT_MAX_CALLS = int(os.getenv("AGENT_RATE_LIMIT_MAX", "5"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("AGENT_RATE_LIMIT_WINDOW", "60"))
USER_TOOL_RATE_LIMIT_MAX_CALLS = int(
    os.getenv("AGENT_USER_TOOL_RATE_LIMIT_MAX")
    or os.getenv("AGENT_RATE_LIMIT_MAX", "5")
)
USER_TOOL_RATE_LIMIT_WINDOW_SECONDS = int(
    os.getenv("AGENT_USER_TOOL_RATE_LIMIT_WINDOW")
    or os.getenv("AGENT_RATE_LIMIT_WINDOW", "60")
)
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
    "Total number of denied tool requests due to policy enforcement.",
)
agent_rate_limit_block_total = Counter(
    "agent_rate_limit_block_total",
    "Total number of chat requests rejected by the global rate limit.",
)
agent_rate_limited_total = Counter(
    "agent_rate_limited_total",
    "Total number of chat requests rejected by rate limits.",
    labelnames=("scope", "tool", "user_hash"),
)
agent_tool_latency_seconds = Histogram(
    "agent_tool_latency_seconds",
    "Latency of mocked agent tool executions.",
    labelnames=("tool", "user_hash"),
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1, 2, 5),
)

# ---------------------------------------------------------------------------
# Rate limiter implementation
# ---------------------------------------------------------------------------


class RateLimitExceededError(RuntimeError):
    """Raised when a rate limit budget is exhausted."""

    def __init__(self, message: str, *, scope: str) -> None:
        super().__init__(message)
        self.scope = scope


class PolicyDeniedError(RuntimeError):
    """Raised when the agent policy denies a tool invocation."""

    def __init__(
        self,
        message: str,
        *,
        reason: str = "policy_denied",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.reason = reason
        self.details = details or {}


class GlobalRateLimiter:
    def __init__(self, max_calls: int, window_seconds: int) -> None:
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._events: Deque[float] = deque()

    def reset(self) -> None:
        self._events.clear()

    def check(self, *, user_hash: str = "unknown", tool: Optional[str] = None) -> None:
        now = time.monotonic()
        window_start = now - self.window_seconds
        while self._events and self._events[0] < window_start:
            self._events.popleft()
        if len(self._events) >= self.max_calls:
            agent_rate_limit_block_total.inc()
            agent_rate_limited_total.labels(
                scope="global",
                tool=tool or "__global__",
                user_hash=user_hash,
            ).inc()
            raise RateLimitExceededError(
                f"Rate limit exceeded (global): {self.max_calls} calls per {self.window_seconds}s",
                scope="global",
            )
        self._events.append(now)


class UserToolRateLimiter:
    def __init__(self, max_calls: int, window_seconds: int) -> None:
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._events: Dict[Tuple[str, str], Deque[float]] = defaultdict(deque)

    def reset(self) -> None:
        self._events.clear()

    def check(self, *, user_hash: str, tool: str) -> None:
        key = (user_hash, tool)
        events = self._events[key]
        now = time.monotonic()
        window_start = now - self.window_seconds
        while events and events[0] < window_start:
            events.popleft()
        if len(events) >= self.max_calls:
            agent_rate_limited_total.labels(
                scope="user_tool",
                tool=tool,
                user_hash=user_hash,
            ).inc()
            raise RateLimitExceededError(
                (
                    "Rate limit exceeded (user/tool): "
                    f"{self.max_calls} calls per {self.window_seconds}s"
                ),
                scope="user_tool",
            )
        events.append(now)


global_rate_limiter = GlobalRateLimiter(
    max_calls=RATE_LIMIT_MAX_CALLS,
    window_seconds=RATE_LIMIT_WINDOW_SECONDS,
)
user_tool_rate_limiter = UserToolRateLimiter(
    max_calls=USER_TOOL_RATE_LIMIT_MAX_CALLS,
    window_seconds=USER_TOOL_RATE_LIMIT_WINDOW_SECONDS,
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


def compute_user_hash(identifier: str) -> str:
    """Return a short, stable hash for identifying users in metrics."""

    digest = hashlib.sha256(identifier.encode("utf-8")).hexdigest()
    return digest[:16]


def extract_user_identifier(request: Request) -> str:
    """Resolve a stable identifier for rate limiting and metrics labelling."""

    header_keys = [
        "X-User-Id",
        "X-User-Email",
        "X-Forwarded-User",
    ]
    for header in header_keys:
        value = request.headers.get(header)
        if value:
            return value
    authorization = request.headers.get("Authorization")
    if authorization:
        return authorization
    if request.client and request.client.host:
        return request.client.host
    return "anonymous"


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


def resolve_tool(
    tool: Optional[str],
    *,
    route: str,
    context: Optional[Dict[str, Any]] = None,
) -> str:
    selected = tool or "dossier.build"
    if selected not in ALLOWED_TOOLS:
        agent_policy_denied_total.inc()
        raise PolicyDeniedError(
            f"Tool '{selected}' is not registered.",
            reason="unknown_tool",
            details={"tool": selected},
        )

    decision: PolicyDecision = policy_engine.authorize(
        tool=selected,
        route=route,
        context=context or {},
    )
    if not decision.allow:
        agent_policy_denied_total.inc()
        raise PolicyDeniedError(
            decision.message or f"Tool '{selected}' blocked by policy.",
            reason=decision.reason or "policy_denied",
            details={"tool": selected, "policy": decision.raw},
        )
    return selected


def execute_tool(
    tool_name: str, params: Dict[str, Any], prompt: str, user_hash: str
) -> ToolCall:
    start_time = datetime.utcnow()
    perf_start = time.perf_counter()
    agent_tool_calls_total.labels(tool=tool_name).inc()

    # Mock execution payload keeps the demo deterministic and offline.
    result_payload = {
        "summary": f"Mocked {tool_name} run for '{prompt[:120]}'",
        "parameters": params,
        "notes": "Offline execution – replace with real integration in Wave 4b.",
    }

    finished_at = datetime.utcnow()
    latency = time.perf_counter() - perf_start
    agent_tool_latency_seconds.labels(tool=tool_name, user_hash=user_hash).observe(latency)
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


@app.exception_handler(PolicyDeniedError)
async def policy_denied_handler(_: Request, exc: PolicyDeniedError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": exc.reason,
            "message": exc.message,
            "details": exc.details,
        },
    )


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
            "user_tool": {
                "max_calls": USER_TOOL_RATE_LIMIT_MAX_CALLS,
                "window_seconds": USER_TOOL_RATE_LIMIT_WINDOW_SECONDS,
            },
        },
    }


@app.get("/tools", response_model=ToolsResponse)
async def list_tools(_: None = Depends(require_agents_enabled)) -> ToolsResponse:
    tools = [ToolModel(**tool.as_dict()) for tool in TOOL_REGISTRY.values()]
    return ToolsResponse(tools=tools)


@app.post("/chat", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    fastapi_request: Request,
    _: None = Depends(require_agents_enabled),
) -> ChatResponse:
    prompt = sanitise_message(chat_request.message)
    conversation_id = chat_request.conversation_id or str(uuid.uuid4())
    user_identifier = extract_user_identifier(fastapi_request)
    user_hash = compute_user_hash(user_identifier)

    policy_context = {
        "conversation_id": conversation_id,
        "request_id": fastapi_request.headers.get("X-Request-Id"),
        "user_hash": user_hash,
    }

    selected_tool = resolve_tool(
        chat_request.tool,
        route="chat",
        context=policy_context,
    )
    tool_definition = TOOL_REGISTRY[selected_tool]

    try:
        global_rate_limiter.check(user_hash=user_hash, tool=selected_tool)
        user_tool_rate_limiter.check(user_hash=user_hash, tool=selected_tool)
    except RateLimitExceededError as exc:
        logger.warning(
            "rate_limit_block",
            extra={
                "conversation_id": conversation_id,
                "scope": exc.scope,
                "tool": selected_tool,
                "user_hash": user_hash,
            },
        )
        raise HTTPException(status_code=429, detail=str(exc)) from exc

    # Hydrate default parameters when omitted to keep schema deterministic.
    params: Dict[str, Any] = {}
    for param_name, schema in tool_definition.parameters.items():
        if param_name in chat_request.tool_params:
            params[param_name] = chat_request.tool_params[param_name]
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

    tool_call = execute_tool(selected_tool, params, prompt, user_hash)
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
            "user_tool": {
                "max_calls": USER_TOOL_RATE_LIMIT_MAX_CALLS,
                "window_seconds": USER_TOOL_RATE_LIMIT_WINDOW_SECONDS,
            },
        },
    }


# Export utility symbols for tests
__all__ = [
    "TOOL_REGISTRY",
    "global_rate_limiter",
    "user_tool_rate_limiter",
    "agent_tool_calls_total",
    "agent_policy_denied_total",
    "agent_rate_limit_block_total",
    "agent_rate_limited_total",
    "agent_tool_latency_seconds",
    "MAX_STEPS",
    "MAX_TOKENS",
    "app",
    "compute_user_hash",
]
