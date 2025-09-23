"""
Shared API schemas and standards for InfoTerminal services.

This module provides unified response formats, error handling, and pagination
to ensure consistency across all microservices.
"""
from typing import Any, Dict, List, Optional, Union, Generic, TypeVar
from pydantic import BaseModel, Field
from enum import Enum


# Generic type for paginated responses
T = TypeVar('T')


class APIVersion(str, Enum):
    """API version enum."""
    V1 = "v1"


class ErrorCode(str, Enum):
    """Standard error codes across all services."""
    # Client errors (4xx)
    INVALID_REQUEST = "INVALID_REQUEST"
    UNAUTHORIZED = "UNAUTHORIZED" 
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    CONFLICT = "CONFLICT"
    RATE_LIMITED = "RATE_LIMITED"
    
    # Server errors (5xx)
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    DATABASE_ERROR = "DATABASE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    TIMEOUT = "TIMEOUT"
    
    # Domain-specific errors
    SEARCH_FAILED = "SEARCH_FAILED"
    GRAPH_QUERY_ERROR = "GRAPH_QUERY_ERROR"
    NLP_PROCESSING_ERROR = "NLP_PROCESSING_ERROR"
    VERIFICATION_ERROR = "VERIFICATION_ERROR"
    DOCUMENT_PROCESSING_ERROR = "DOCUMENT_PROCESSING_ERROR"


class ErrorDetail(BaseModel):
    """Error detail information."""
    code: ErrorCode
    message: str
    details: Optional[Dict[str, Any]] = None
    field: Optional[str] = None  # For validation errors


class ErrorResponse(BaseModel):
    """Standard error response envelope."""
    error: ErrorDetail

    @classmethod
    def create(
        cls,
        code: ErrorCode,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        field: Optional[str] = None
    ) -> "ErrorResponse":
        """Create an error response."""
        return cls(
            error=ErrorDetail(
                code=code,
                message=message,
                details=details,
                field=field
            )
        )


class PaginationInfo(BaseModel):
    """Pagination metadata."""
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number (1-based)")
    size: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")

    @classmethod
    def create(cls, total: int, page: int, size: int) -> "PaginationInfo":
        """Create pagination info from total, page, and size."""
        pages = (total + size - 1) // size if total > 0 else 1
        return cls(
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1
        )


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated response."""
    items: List[T]
    pagination: PaginationInfo

    @classmethod
    def create(cls, items: List[T], total: int, page: int, size: int) -> "PaginatedResponse[T]":
        """Create a paginated response."""
        return cls(
            items=items,
            pagination=PaginationInfo.create(total, page, size)
        )


class HealthStatus(str, Enum):
    """Health check status."""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


class HealthCheck(BaseModel):
    """Individual health check result."""
    status: HealthStatus
    latency_ms: Optional[float] = None
    error: Optional[str] = None
    reason: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Service health response."""
    service: str
    version: str
    status: HealthStatus
    uptime_seconds: float
    timestamp: str
    checks: Optional[Dict[str, HealthCheck]] = None


class ReadinessResponse(BaseModel):
    """Service readiness response."""
    service: str
    version: str
    status: HealthStatus
    uptime_seconds: float
    timestamp: str
    checks: Dict[str, HealthCheck]


class JobStatus(str, Enum):
    """Job execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobInfo(BaseModel):
    """Job information."""
    id: str
    status: JobStatus
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    progress: Optional[float] = None  # 0.0 to 1.0
    message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class SortOrder(str, Enum):
    """Sort order enum."""
    ASC = "asc"
    DESC = "desc"


class SortField(BaseModel):
    """Sort field specification."""
    field: str
    order: SortOrder = SortOrder.ASC


class BaseFilter(BaseModel):
    """Base filter specification."""
    field: str
    operator: str  # eq, ne, gt, gte, lt, lte, in, not_in, contains, etc.
    value: Union[str, int, float, bool, List[Any]]


class QueryRequest(BaseModel):
    """Base query request."""
    page: int = Field(1, ge=1, description="Page number (1-based)")
    size: int = Field(20, ge=1, le=100, description="Items per page")
    sort: Optional[List[SortField]] = None
    filters: Optional[List[BaseFilter]] = None


class MetricsResponse(BaseModel):
    """Service metrics response."""
    service: str
    timestamp: str
    metrics: Dict[str, Union[int, float, str]]


# Service-specific base models

class SearchRequest(QueryRequest):
    """Search request with query and facets."""
    q: Optional[str] = Field(None, description="Search query")
    facets: Optional[List[str]] = Field(None, description="Facet fields")
    highlight: bool = Field(False, description="Enable highlighting")


class GraphRequest(BaseModel):
    """Graph query request."""
    cypher: str = Field(..., description="Cypher query")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Query parameters")
    limit: Optional[int] = Field(100, ge=1, le=10000, description="Result limit")
    timeout: Optional[int] = Field(30, ge=1, le=300, description="Timeout in seconds")


class DocumentRequest(BaseModel):
    """Document processing request."""
    content: Optional[str] = Field(None, description="Text content")
    url: Optional[str] = Field(None, description="Document URL")
    file_path: Optional[str] = Field(None, description="File path")
    language: Optional[str] = Field("auto", description="Document language")
    extract_entities: bool = Field(True, description="Extract entities")
    extract_relations: bool = Field(False, description="Extract relations")
    summarize: bool = Field(False, description="Generate summary")


# Response models

class EntityResult(BaseModel):
    """Entity extraction result."""
    text: str
    label: str
    start: int
    end: int
    confidence: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class RelationResult(BaseModel):
    """Relation extraction result."""
    subject: EntityResult
    predicate: str
    object: EntityResult
    confidence: Optional[float] = None


class DocumentResult(BaseModel):
    """Document processing result."""
    id: str
    content: str
    entities: List[EntityResult] = []
    relations: List[RelationResult] = []
    summary: Optional[str] = None
    language: Optional[str] = None
    metadata: Dict[str, Any] = {}
    processing_time_ms: Optional[float] = None


class SearchResult(BaseModel):
    """Search result item."""
    id: str
    score: float
    title: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = None
    metadata: Dict[str, Any] = {}
    entities: List[EntityResult] = []
    highlight: Optional[Dict[str, List[str]]] = None


class GraphNode(BaseModel):
    """Graph node."""
    id: str
    labels: List[str] = []
    properties: Dict[str, Any] = {}


class GraphRelationship(BaseModel):
    """Graph relationship."""
    id: str
    type: str
    start_node: str
    end_node: str
    properties: Dict[str, Any] = {}


class GraphResult(BaseModel):
    """Graph query result."""
    nodes: List[GraphNode] = []
    relationships: List[GraphRelationship] = []
    paths: List[List[Union[GraphNode, GraphRelationship]]] = []
    stats: Optional[Dict[str, Any]] = None
    execution_time_ms: Optional[float] = None
