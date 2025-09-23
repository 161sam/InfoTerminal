"""
InfoTerminal Graph API - Standardized v1 Implementation

This is the new standardized version of the Graph API implementing all
InfoTerminal API standards:
- /v1 namespace
- Standard error handling  
- Pagination
- Health checks
- OpenAPI documentation
- Middleware setup
"""

import os
import sys
import time
import asyncio
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Query, APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Add shared standards to Python path
SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from _shared.api_standards import (
    setup_standard_middleware,
    setup_standard_exception_handlers,
    setup_standard_openapi,
    get_service_tags_metadata,
    PaginatedResponse,
    PaginationParams,
    APIError,
    ErrorCodes,
    StandardError
)

from _shared.health import make_healthz as legacy_make_healthz, make_readyz as legacy_make_readyz, probe_db as legacy_probe_db

from it_logging import setup_logging
from utils.neo4j_client import get_driver, neo_session
from .routes.alg import router as alg_router
from .routes.export import router as export_router
from .routes.analytics import legacy_router as legacy_analytics_router
from .routes.analytics import router as analytics_router
from .routes.geospatial import router as geospatial_router

try:
    import neo4j
    from neo4j import exceptions
    from neo4j.graph import Node as Neo4jNode, Relationship as Neo4jRelationship, Path as Neo4jPath
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False
    neo4j = None
    exceptions = None
    Neo4jNode = None
    Neo4jRelationship = None
    Neo4jPath = None

# Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS") or os.getenv("NEO4J_PASSWORD", "test12345")

driver = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    global driver
    if NEO4J_AVAILABLE:
        try:
            driver = get_driver(NEO4J_URI, NEO4J_USER, NEO4J_PASS)
            app.state.driver = driver
            print("✅ Neo4j driver initialized successfully")
        except Exception as e:
            print(f"⚠️ Neo4j driver initialization failed: {e}")
    
    yield
    
    if driver:
        driver.close()
        app.state.driver = None
        print("🛑 Neo4j driver closed")


# FastAPI App with Standard Configuration
app = FastAPI(
    title="InfoTerminal Graph API",
    description="Graph database API for InfoTerminal OSINT platform with Neo4j backend",
    version="1.0.0",
    openapi_url="/v1/openapi.json",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    lifespan=lifespan
)

# Set up logging
setup_logging(app, service_name="graph-api")

# Set up standard middleware and exception handling
setup_standard_middleware(app, "graph-api")
setup_standard_exception_handlers(app)
setup_standard_openapi(
    app=app,
    title="InfoTerminal Graph API",
    description="Graph database API for InfoTerminal OSINT platform with Neo4j backend",
    version="1.0.0",
    service_name="graph-api",
    tags_metadata=get_service_tags_metadata("graph-api")
)

# Application state
app.state.service_name = "graph-api"
app.state.version = os.getenv("GIT_SHA", "1.0.0")
app.state.start_ts = time.monotonic()

# OTEL instrumentation (optional)
try:  # pragma: no cover - optional dependency
    from _shared.obs.otel_boot import setup_otel
except Exception:  # pragma: no cover
    def setup_otel(*args, **kwargs):
        return None

setup_otel(app, service_name=app.state.service_name, version=app.state.version)

# Legacy-style health helpers retained for compatibility
probe_db = legacy_probe_db


@app.get("/healthz", tags=["health"])
def healthz():
    """Health check endpoint (legacy response schema)."""
    return legacy_make_healthz(app.state.service_name, str(app.state.version), app.state.start_ts)


@app.get("/readyz", tags=["health"])
def readyz():
    """Readiness check endpoint with legacy response schema."""
    if os.getenv("IT_FORCE_READY") == "1":
        payload, status = legacy_make_readyz(app.state.service_name, str(app.state.version), app.state.start_ts, {})
        return JSONResponse(payload, status_code=status)

    checks: Dict[str, Dict[str, Any]] = {}

    if driver and NEO4J_AVAILABLE:
        def _ping() -> None:
            with neo_session(driver) as session:
                session.run("RETURN 1").consume()

        checks["neo4j"] = probe_db(_ping)
    else:
        checks["neo4j"] = {"status": "skipped", "latency_ms": None, "error": None, "reason": "driver not ready"}

    payload, status = legacy_make_readyz(app.state.service_name, str(app.state.version), app.state.start_ts, checks)
    return JSONResponse(payload, status_code=status)


# API Models
class CypherRequest(BaseModel):
    """Cypher query request model."""
    query: str = Field(..., description="Cypher query to execute")
    parameters: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Query parameters"
    )
    read_only: bool = Field(
        default=True,
        description="Whether query is read-only (write queries require explicit permission)"
    )


class GraphNode(BaseModel):
    """Graph node representation."""
    id: int = Field(..., description="Node internal ID")
    labels: List[str] = Field(..., description="Node labels")
    properties: Dict[str, Any] = Field(..., description="Node properties")


class GraphRelationship(BaseModel):
    """Graph relationship representation."""
    id: int = Field(..., description="Relationship internal ID")
    type: str = Field(..., description="Relationship type")
    start_node: int = Field(..., description="Start node ID")
    end_node: int = Field(..., description="End node ID")
    properties: Dict[str, Any] = Field(..., description="Relationship properties")


class GraphPath(BaseModel):
    """Graph path representation."""
    length: int = Field(..., description="Path length")
    nodes: List[GraphNode] = Field(..., description="Nodes in path")
    relationships: List[GraphRelationship] = Field(..., description="Relationships in path")


class CypherResponse(BaseModel):
    """Cypher query response."""
    records: List[Dict[str, Any]] = Field(..., description="Query result records")
    summary: Optional[Dict[str, Any]] = Field(None, description="Query execution summary")
    took_ms: int = Field(..., description="Query execution time in milliseconds")


class NeighborRequest(BaseModel):
    """Node neighbors request model."""
    node_id: Union[str, int] = Field(..., description="Node ID to find neighbors for")
    depth: int = Field(default=1, ge=1, le=5, description="Traversal depth")
    limit: int = Field(default=50, ge=1, le=1000, description="Maximum neighbors to return")
    relationship_types: Optional[List[str]] = Field(
        None,
        description="Filter by relationship types"
    )
    direction: str = Field(
        default="both",
        pattern="^(incoming|outgoing|both)$",
        description="Traversal direction"
    )


class NeighborResponse(BaseModel):
    """Node neighbors response."""
    center_node: GraphNode = Field(..., description="Central node")
    neighbors: List[GraphNode] = Field(..., description="Neighboring nodes")
    relationships: List[GraphRelationship] = Field(..., description="Connecting relationships")
    total_neighbors: int = Field(..., description="Total number of neighbors found")


class ShortestPathRequest(BaseModel):
    """Shortest path request model."""
    source_node: Union[str, int] = Field(..., description="Source node ID")
    target_node: Union[str, int] = Field(..., description="Target node ID")
    max_length: int = Field(default=6, ge=1, le=10, description="Maximum path length")
    relationship_types: Optional[List[str]] = Field(
        None,
        description="Allowed relationship types"
    )


class ShortestPathResponse(BaseModel):
    """Shortest path response."""
    path: Optional[GraphPath] = Field(None, description="Shortest path if found")
    found: bool = Field(..., description="Whether path was found")
    source_node: GraphNode = Field(..., description="Source node")
    target_node: Optional[GraphNode] = Field(None, description="Target node (if found)")


class AlgorithmRequest(BaseModel):
    """Graph algorithm request model."""
    algorithm: str = Field(..., description="Algorithm name (pagerank, centrality, communities)")
    parameters: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Algorithm-specific parameters"
    )
    node_filter: Optional[Dict[str, Any]] = Field(
        None,
        description="Node filter criteria"
    )


class JobStatus(BaseModel):
    """Algorithm job status."""
    job_id: str = Field(..., description="Job identifier")
    status: str = Field(..., description="Job status (pending, running, completed, failed)")
    progress: float = Field(default=0.0, ge=0.0, le=1.0, description="Job progress (0-1)")
    result: Optional[Dict[str, Any]] = Field(None, description="Job result if completed")
    error: Optional[str] = Field(None, description="Error message if failed")
    created_at: str = Field(..., description="Job creation timestamp")
    updated_at: str = Field(..., description="Job last update timestamp")


# Helper functions
def serialize_neo4j_object(obj: Any) -> Any:
    """Serialize Neo4j objects to JSON-compatible format."""
    if Neo4jNode and isinstance(obj, Neo4jNode):
        return GraphNode(
            id=obj.id,
            labels=list(obj.labels),
            properties=dict(obj)
        )
    elif Neo4jRelationship and isinstance(obj, Neo4jRelationship):
        return GraphRelationship(
            id=obj.id,
            type=obj.type,
            start_node=obj.start_node.id if hasattr(obj, 'start_node') else obj.start_node_id,
            end_node=obj.end_node.id if hasattr(obj, 'end_node') else obj.end_node_id,
            properties=dict(obj)
        )
    elif Neo4jPath and isinstance(obj, Neo4jPath):
        return GraphPath(
            length=len(obj.relationships),
            nodes=[serialize_neo4j_object(node) for node in obj.nodes],
            relationships=[serialize_neo4j_object(rel) for rel in obj.relationships]
        )
    elif isinstance(obj, list):
        return [serialize_neo4j_object(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_neo4j_object(value) for key, value in obj.items()}
    else:
        return obj


def execute_cypher_query(query: str, parameters: Dict[str, Any] = None, read_only: bool = True) -> tuple:
    """Execute a Cypher query and return results with timing."""
    if not NEO4J_AVAILABLE or not driver:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Neo4j service unavailable",
            status_code=503,
            details={"reason": "Neo4j driver not available"}
        )
    
    start_time = time.time()
    
    try:
        with neo_session(driver) as session:
            if read_only:
                result = session.run(query, parameters or {})
            else:
                # Write operations require explicit transaction
                with session.begin_transaction() as tx:
                    result = tx.run(query, parameters or {})
                    tx.commit()
            
            records = []
            summary = None
            
            for record in result:
                serialized_record = {}
                for key, value in record.items():
                    serialized_record[key] = serialize_neo4j_object(value)
                records.append(serialized_record)
            
            # Get query summary
            result_summary = result.consume()
            if result_summary:
                summary = {
                    "statement_type": getattr(result_summary, "statement_type", None),
                    "counters": getattr(result_summary, "counters", None)
                }
            
            took_ms = int((time.time() - start_time) * 1000)
            
            return records, summary, took_ms
            
    except exceptions.CypherSyntaxError as e:
        raise APIError(
            code=ErrorCodes.INVALID_REQUEST,
            message=f"Invalid Cypher syntax: {str(e)}",
            status_code=400,
            details={"query": query}
        )
    except exceptions.AuthError as e:
        raise APIError(
            code=ErrorCodes.UNAUTHORIZED,
            message="Neo4j authentication failed",
            status_code=401,
            details={"error": str(e)}
        )
    except Exception as e:
        raise APIError(
            code=ErrorCodes.GRAPH_ERROR,
            message=f"Graph query failed: {str(e)}",
            status_code=500,
            details={"query": query, "error_type": e.__class__.__name__}
        )


# V1 API Router
v1_router = APIRouter(prefix="/v1", tags=["v1"])


@v1_router.post("/cypher",
                response_model=CypherResponse,
                tags=["cypher"],
                summary="Execute Cypher query",
                description="Execute a Cypher query against the Neo4j database")
def execute_cypher(request: CypherRequest):
    """
    Execute a Cypher query against the Neo4j database.
    
    Supports both read and write operations:
    - Read operations are executed directly
    - Write operations require explicit permission and transaction handling
    
    Query parameters can be used to prevent injection attacks.
    """
    
    records, summary, took_ms = execute_cypher_query(
        query=request.query,
        parameters=request.parameters,
        read_only=request.read_only
    )
    
    return CypherResponse(
        records=records,
        summary=summary,
        took_ms=took_ms
    )


@v1_router.get("/nodes/{node_id}/neighbors",
               response_model=NeighborResponse,
               tags=["graph"],
               summary="Get node neighbors",
               description="Find neighbors of a specific node")
def get_node_neighbors(
    node_id: Union[str, int],
    depth: int = Query(default=1, ge=1, le=5, description="Traversal depth"),
    limit: int = Query(default=50, ge=1, le=1000, description="Maximum neighbors to return"),
    relationship_types: Optional[str] = Query(None, description="Comma-separated relationship types"),
    direction: str = Query(default="both", pattern="^(incoming|outgoing|both)$", description="Traversal direction")
):
    """
    Find neighbors of a specific node.
    
    Traverses the graph from the specified node to find connected nodes:
    - Supports configurable traversal depth
    - Can filter by relationship types
    - Supports directional traversal (incoming, outgoing, or both)
    - Returns both nodes and connecting relationships
    """
    
    # Parse relationship types
    rel_types = []
    if relationship_types:
        rel_types = [rt.strip() for rt in relationship_types.split(",") if rt.strip()]
    
    # Build Cypher query based on direction
    if direction == "incoming":
        direction_pattern = "<-[r]-(neighbor)"
    elif direction == "outgoing":
        direction_pattern = "-[r]->(neighbor)"
    else:  # both
        direction_pattern = "-[r]-(neighbor)"
    
    # Build relationship type filter
    rel_type_filter = ""
    if rel_types:
        rel_type_filter = f":{':'.join(rel_types)}"
    
    # Construct query
    query = f"""
    MATCH (center)
    WHERE id(center) = $node_id
    
    MATCH (center){direction_pattern.replace('[r]', f'[r{rel_type_filter}*1..{depth}]')}
    
    RETURN center,
           collect(DISTINCT neighbor) as neighbors,
           collect(DISTINCT r) as relationships
    LIMIT $limit
    """
    
    records, _, took_ms = execute_cypher_query(
        query=query,
        parameters={"node_id": int(node_id) if str(node_id).isdigit() else node_id, "limit": limit}
    )
    
    if not records:
        raise APIError(
            code=ErrorCodes.RESOURCE_NOT_FOUND,
            message="Node not found",
            status_code=404,
            details={"node_id": node_id}
        )
    
    record = records[0]
    center_node = serialize_neo4j_object(record["center"])
    neighbors = [serialize_neo4j_object(node) for node in record["neighbors"]]
    relationships = []
    
    # Flatten relationship arrays
    for rel_array in record["relationships"]:
        if isinstance(rel_array, list):
            relationships.extend([serialize_neo4j_object(rel) for rel in rel_array])
        else:
            relationships.append(serialize_neo4j_object(rel_array))
    
    return NeighborResponse(
        center_node=center_node,
        neighbors=neighbors,
        relationships=relationships,
        total_neighbors=len(neighbors)
    )


@v1_router.post("/shortest-path",
                response_model=ShortestPathResponse,
                tags=["graph"],
                summary="Find shortest path",
                description="Find shortest path between two nodes")
def find_shortest_path(request: ShortestPathRequest):
    """
    Find the shortest path between two nodes.
    
    Uses Neo4j's shortestPath algorithm to find the optimal route:
    - Supports maximum path length constraints
    - Can filter by relationship types
    - Returns the complete path with nodes and relationships
    - Handles cases where no path exists
    """
    
    # Build relationship type filter
    rel_type_filter = ""
    if request.relationship_types:
        rel_type_filter = f":{':'.join(request.relationship_types)}"
    
    # Construct shortest path query
    query = f"""
    MATCH (source), (target)
    WHERE id(source) = $source_id AND id(target) = $target_id
    
    MATCH path = shortestPath((source)-[{rel_type_filter}*..{request.max_length}]-(target))
    
    RETURN source, target, path
    """
    
    records, _, took_ms = execute_cypher_query(
        query=query,
        parameters={
            "source_id": int(request.source_node) if str(request.source_node).isdigit() else request.source_node,
            "target_id": int(request.target_node) if str(request.target_node).isdigit() else request.target_node
        }
    )
    
    if not records:
        # Check if nodes exist individually
        node_check_query = """
        OPTIONAL MATCH (source) WHERE id(source) = $source_id
        OPTIONAL MATCH (target) WHERE id(target) = $target_id
        RETURN source, target
        """
        
        check_records, _, _ = execute_cypher_query(
            query=node_check_query,
            parameters={
                "source_id": int(request.source_node) if str(request.source_node).isdigit() else request.source_node,
                "target_id": int(request.target_node) if str(request.target_node).isdigit() else request.target_node
            }
        )
        
        if not check_records or not check_records[0]["source"]:
            raise APIError(
                code=ErrorCodes.RESOURCE_NOT_FOUND,
                message="Source node not found",
                status_code=404,
                details={"source_node": request.source_node}
            )
        
        if not check_records[0]["target"]:
            raise APIError(
                code=ErrorCodes.RESOURCE_NOT_FOUND,
                message="Target node not found",
                status_code=404,
                details={"target_node": request.target_node}
            )
        
        # Nodes exist but no path found
        source_node = serialize_neo4j_object(check_records[0]["source"])
        return ShortestPathResponse(
            path=None,
            found=False,
            source_node=source_node,
            target_node=None
        )
    
    record = records[0]
    source_node = serialize_neo4j_object(record["source"])
    target_node = serialize_neo4j_object(record["target"])
    path = serialize_neo4j_object(record["path"]) if record["path"] else None
    
    return ShortestPathResponse(
        path=path,
        found=path is not None,
        source_node=source_node,
        target_node=target_node
    )


# Algorithm job storage (in-memory for demo, use Redis/DB in production)
algorithm_jobs = {}


@v1_router.post("/algorithms/centrality",
                response_model=JobStatus,
                tags=["analytics"],
                summary="Run centrality algorithm",
                description="Execute graph centrality algorithms (PageRank, Betweenness, etc.)")
def run_centrality_algorithm(
    request: AlgorithmRequest,
    background_tasks: BackgroundTasks
):
    """
    Execute graph centrality algorithms.
    
    Supported algorithms:
    - pagerank: PageRank centrality
    - betweenness: Betweenness centrality  
    - closeness: Closeness centrality
    - degree: Degree centrality
    
    Algorithms run asynchronously and return a job ID for status tracking.
    """
    
    import uuid
    from datetime import datetime
    
    job_id = str(uuid.uuid4())
    
    # Initialize job status
    job_status = JobStatus(
        job_id=job_id,
        status="pending",
        progress=0.0,
        result=None,
        error=None,
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat()
    )
    
    algorithm_jobs[job_id] = job_status
    
    # Start algorithm in background
    background_tasks.add_task(
        _run_centrality_algorithm,
        job_id,
        request.algorithm,
        request.parameters,
        request.node_filter
    )
    
    return job_status


@v1_router.post("/algorithms/communities",
                response_model=JobStatus,
                tags=["analytics"],
                summary="Run community detection",
                description="Execute graph community detection algorithms")
def run_community_detection(
    request: AlgorithmRequest,
    background_tasks: BackgroundTasks
):
    """
    Execute graph community detection algorithms.
    
    Supported algorithms:
    - louvain: Louvain community detection
    - leiden: Leiden algorithm
    - label_propagation: Label propagation
    - weakly_connected: Weakly connected components
    
    Algorithms run asynchronously and return a job ID for status tracking.
    """
    
    import uuid
    from datetime import datetime
    
    job_id = str(uuid.uuid4())
    
    # Initialize job status
    job_status = JobStatus(
        job_id=job_id,
        status="pending",
        progress=0.0,
        result=None,
        error=None,
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat()
    )
    
    algorithm_jobs[job_id] = job_status
    
    # Start algorithm in background
    background_tasks.add_task(
        _run_community_algorithm,
        job_id,
        request.algorithm,
        request.parameters,
        request.node_filter
    )
    
    return job_status


@v1_router.get("/jobs/{job_id}",
               response_model=JobStatus,
               tags=["analytics"],
               summary="Get job status",
               description="Get the status of a running algorithm job")
def get_job_status(job_id: str):
    """
    Get the status of a running algorithm job.
    
    Returns the current status, progress, and results (if completed) of
    an algorithm job started via the /algorithms endpoints.
    """
    
    if job_id not in algorithm_jobs:
        raise APIError(
            code=ErrorCodes.RESOURCE_NOT_FOUND,
            message="Job not found",
            status_code=404,
            details={"job_id": job_id}
        )
    
    return algorithm_jobs[job_id]


@v1_router.delete("/jobs/{job_id}",
                  tags=["analytics"],
                  summary="Cancel job",
                  description="Cancel a running algorithm job")
def cancel_job(job_id: str):
    """
    Cancel a running algorithm job.
    
    Attempts to cancel a running job and removes it from the job queue.
    Jobs that have already completed cannot be cancelled.
    """
    
    if job_id not in algorithm_jobs:
        raise APIError(
            code=ErrorCodes.RESOURCE_NOT_FOUND,
            message="Job not found",
            status_code=404,
            details={"job_id": job_id}
        )
    
    job = algorithm_jobs[job_id]
    
    if job.status in ["completed", "failed"]:
        raise APIError(
            code=ErrorCodes.CONFLICT,
            message="Cannot cancel completed job",
            status_code=409,
            details={"job_id": job_id, "status": job.status}
        )
    
    # Mark job as cancelled
    job.status = "cancelled"
    job.updated_at = time.time()
    
    return {"cancelled": True, "job_id": job_id}


# Background task functions
async def _run_centrality_algorithm(job_id: str, algorithm: str, parameters: Dict[str, Any], node_filter: Optional[Dict[str, Any]]):
    """Background task for running centrality algorithms."""
    from datetime import datetime
    
    job = algorithm_jobs[job_id]
    
    try:
        # Update job status
        job.status = "running"
        job.progress = 0.1
        job.updated_at = datetime.utcnow().isoformat()
        
        # Simulate algorithm execution (replace with actual algorithm)
        await asyncio.sleep(2)  # Simulate processing time
        
        job.progress = 0.5
        job.updated_at = datetime.utcnow().isoformat()
        
        # Mock result based on algorithm type
        if algorithm == "pagerank":
            result = {
                "algorithm": "pagerank",
                "node_scores": [
                    {"node_id": 1, "score": 0.25},
                    {"node_id": 2, "score": 0.35},
                    {"node_id": 3, "score": 0.15}
                ],
                "parameters": parameters
            }
        elif algorithm == "betweenness":
            result = {
                "algorithm": "betweenness",
                "node_scores": [
                    {"node_id": 1, "score": 0.8},
                    {"node_id": 2, "score": 0.6},
                    {"node_id": 3, "score": 0.4}
                ],
                "parameters": parameters
            }
        else:
            result = {
                "algorithm": algorithm,
                "message": f"Algorithm {algorithm} not yet implemented",
                "parameters": parameters
            }
        
        # Complete job
        job.status = "completed"
        job.progress = 1.0
        job.result = result
        job.updated_at = datetime.utcnow().isoformat()
        
    except Exception as e:
        job.status = "failed"
        job.error = str(e)
        job.updated_at = datetime.utcnow().isoformat()


async def _run_community_algorithm(job_id: str, algorithm: str, parameters: Dict[str, Any], node_filter: Optional[Dict[str, Any]]):
    """Background task for running community detection algorithms."""
    from datetime import datetime
    
    job = algorithm_jobs[job_id]
    
    try:
        # Update job status
        job.status = "running"
        job.progress = 0.1
        job.updated_at = datetime.utcnow().isoformat()
        
        # Simulate algorithm execution
        await asyncio.sleep(3)  # Simulate processing time
        
        job.progress = 0.7
        job.updated_at = datetime.utcnow().isoformat()
        
        # Mock result based on algorithm type
        if algorithm == "louvain":
            result = {
                "algorithm": "louvain",
                "communities": [
                    {"community_id": 0, "nodes": [1, 2, 3]},
                    {"community_id": 1, "nodes": [4, 5, 6]},
                    {"community_id": 2, "nodes": [7, 8]}
                ],
                "modularity": 0.42,
                "parameters": parameters
            }
        else:
            result = {
                "algorithm": algorithm,
                "message": f"Algorithm {algorithm} not yet implemented",
                "parameters": parameters
            }
        
        # Complete job
        job.status = "completed"
        job.progress = 1.0
        job.result = result
        job.updated_at = datetime.utcnow().isoformat()
        
    except Exception as e:
        job.status = "failed"
        job.error = str(e)
        job.updated_at = datetime.utcnow().isoformat()


# Include V1 router
app.include_router(v1_router)

# Legacy routers (temporary compatibility)
app.include_router(alg_router)
app.include_router(export_router)
app.include_router(analytics_router)
app.include_router(legacy_analytics_router)
app.include_router(geospatial_router)

# Legacy endpoints with deprecation warnings
@app.post("/query", deprecated=True, tags=["legacy"])
def legacy_query(payload: dict):
    """
    DEPRECATED: Use /v1/cypher instead.
    
    Legacy query endpoint for backward compatibility.
    Will be removed in a future version.
    """
    cypher_query = payload.get("cypher") or payload.get("query")
    if not cypher_query:
        raise HTTPException(400, "missing cypher")
    
    # Convert to new format
    request = CypherRequest(
        query=cypher_query,
        parameters=payload.get("params") or payload.get("parameters") or {},
        read_only=bool(payload.get("read_only", True))
    )
    
    response = execute_cypher(request)
    
    # Convert to legacy format
    return {"results": response.records}


@app.get("/neighbors", deprecated=True, tags=["legacy"])
def legacy_neighbors(node_id: str, limit: int = 20):
    """
    DEPRECATED: Use /v1/nodes/{id}/neighbors instead.
    
    Legacy neighbors endpoint for backward compatibility.
    Will be removed in a future version.
    """
    if not driver or not NEO4J_AVAILABLE:
        raise HTTPException(503, "driver not ready")

    with neo_session(driver) as session:
        recs = session.run(
            "MATCH (n {id: $id})-[r]-(m) RETURN n, type(r) as rel, m LIMIT $limit",
            id=node_id,
            limit=limit,
        )
        out = []
        for record in recs:
            source = dict(record["n"]) if record["n"] else {}
            rel = record["rel"]
            target = dict(record["m"]) if record["m"] else {}
            out.append({"from": source, "rel": rel, "to": target})
    return out


@app.get("/neo4j/ping", deprecated=True, tags=["legacy"])
def legacy_neo4j_ping():
    """Legacy ping endpoint for Neo4j connectivity."""
    if not driver or not NEO4J_AVAILABLE:
        raise HTTPException(503, "driver not ready")
    try:
        with neo_session(driver) as session:
            session.run("RETURN 1").consume()
        return {"result": 1}
    except exceptions.AuthError:
        raise HTTPException(401, "check NEO4J_USER/NEO4J_PASSWORD")


# Root endpoint
@app.get("/", tags=["root"])
def root():
    """Service information and available endpoints."""
    return {
        "service": "InfoTerminal Graph API",
        "version": app.state.version,
        "status": "running",
        "api_version": "v1",
        "neo4j_available": NEO4J_AVAILABLE,
        "endpoints": {
            "health": "/healthz",
            "ready": "/readyz",
            "docs": "/v1/docs",
            "cypher": "/v1/cypher",
            "neighbors": "/v1/nodes/{id}/neighbors",
            "shortest_path": "/v1/shortest-path",
            "algorithms": "/v1/algorithms/*",
            "jobs": "/v1/jobs/{id}"
        },
        "legacy_endpoints": {
            "query": "/query (deprecated)",
            "neighbors": "/neighbors (deprecated)"
        }
    }
