"""
InfoTerminal Graph Views API - Standardized v1 Implementation

This is the new standardized version of the Graph Views API implementing all
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
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from fastapi import FastAPI, Query

# Add shared standards to Python path
SERVICE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

# Import existing modules
import neo  # noqa: E402
from _shared.api_standards import (  # noqa: E402
    APIError,
    ErrorCodes,
    HealthChecker,
    check_database_connection,
    check_http_endpoint,
    get_service_tags_metadata,
    setup_standard_exception_handlers,
    setup_standard_middleware,
    setup_standard_openapi,
)
from it_logging import setup_logging  # noqa: E402

from .models.view_models import (  # noqa: E402
    EgoNetworkResponse,
    PathViewResponse,
    ViewNode,
    ViewRelationship,
)
from .routers.core_v1 import build_core_router  # noqa: E402
from .routers.views_v1 import build_views_router  # noqa: E402

try:
    import neo4j
    from neo4j.graph import Node as Neo4jNode
    from neo4j.graph import Path as Neo4jPath
    from neo4j.graph import Relationship as Neo4jRelationship
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False
    neo4j = None
    Neo4jNode = None
    Neo4jRelationship = None 
    Neo4jPath = None

# Configuration
GRAPH_API_URL = os.getenv("GRAPH_API_URL", "http://localhost:8402")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    if NEO4J_AVAILABLE:
        try:
            neo.get_driver()
            print("✅ Neo4j driver connection verified")
        except Exception as e:
            print(f"⚠️ Neo4j connection warning: {e}")
    
    yield
    
    if NEO4J_AVAILABLE:
        try:
            driver = neo.get_driver()
            if driver:
                driver.close()
            print("🛑 Neo4j driver closed")
        except Exception:
            pass


# FastAPI App with Standard Configuration
app = FastAPI(
    title="InfoTerminal Graph Views API",
    description="Graph visualization and view API for InfoTerminal OSINT platform",
    version="1.0.0",
    openapi_url="/v1/openapi.json",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    lifespan=lifespan
)

# Set up logging
setup_logging(app, service_name="graph-views")

# Set up standard middleware and exception handling
setup_standard_middleware(app, "graph-views")
setup_standard_exception_handlers(app)
setup_standard_openapi(
    app=app,
    title="InfoTerminal Graph Views API",
    description="Graph visualization and view API for InfoTerminal OSINT platform",
    version="1.0.0",
    service_name="graph-views",
    tags_metadata=get_service_tags_metadata("graph-views")
)

# Application state
app.state.service_name = "graph-views"
app.state.version = os.getenv("GIT_SHA", "1.0.0")
app.state.start_ts = time.monotonic()

# Health Checker Setup
health_checker = HealthChecker("graph-views", app.state.version)

def check_neo4j():
    """Check Neo4j connectivity."""
    if not NEO4J_AVAILABLE:
        raise Exception("Neo4j driver not available")
    
    driver = neo.get_driver()
    if not driver:
        raise Exception("Neo4j driver not initialized")
    
    # Simple connectivity check
    with neo.get_session() as session:
        session.run("RETURN 1").consume()

if NEO4J_AVAILABLE:
    health_checker.add_dependency("neo4j", lambda: check_database_connection(check_neo4j))

try:  # optional dependency
    import requests  # noqa: F401
    health_checker.add_dependency("graph_api", lambda: check_http_endpoint(f"{GRAPH_API_URL}/healthz"))
except ImportError:  # pragma: no cover
    pass

app.include_router(
    build_core_router(
        health_check=lambda: health_checker.health_check(),
        ready_check=lambda: health_checker.ready_check(),
        service_name=app.state.service_name,
        version=str(app.state.version),
        start_ts=app.state.start_ts,
    )
)

# Core router (healthz/readyz/info)
app.include_router(
    build_core_router(
        health_check=health_checker.health_check,
        ready_check=health_checker.ready_check,
        service_name=app.state.service_name,
        version=str(app.state.version),
        start_ts=app.state.start_ts,
    )
)


# API Models
# Helper functions
def _serialize_neo4j(value: Any) -> Any:
    """Serialize Neo4j objects to JSON-compatible format."""
    if Neo4jNode and isinstance(value, Neo4jNode):
        return {
            "__type": "node",
            "id": getattr(value, "id", None),
            "labels": list(getattr(value, "labels", []) or []),
            "properties": dict(value),
        }
    elif Neo4jRelationship and isinstance(value, Neo4jRelationship):
        start_id = getattr(value, "start_node_id", None) or getattr(value, "start", None)
        end_id = getattr(value, "end_node_id", None) or getattr(value, "end", None)
        return {
            "__type": "relationship",
            "id": getattr(value, "id", None),
            "type": getattr(value, "type", None),
            "start": start_id,
            "end": end_id,
            "properties": dict(value),
        }
    elif Neo4jPath and isinstance(value, Neo4jPath):
        nodes = [_serialize_neo4j(n) for n in getattr(value, "nodes", [])]
        rels = [_serialize_neo4j(r) for r in getattr(value, "relationships", [])]
        length = getattr(value, "length", None)
        if length is None:
            try:
                length = len(getattr(value, "relationships", []))
            except Exception:
                length = None
        return {"__type": "path", "nodes": nodes, "relationships": rels, "length": length}
    elif isinstance(value, list):
        return [_serialize_neo4j(v) for v in value]
    elif isinstance(value, tuple):
        return [_serialize_neo4j(v) for v in value]
    elif isinstance(value, dict):
        return {k: _serialize_neo4j(v) for k, v in value.items()}
    else:
        return value


def _run_cypher(query: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Execute Cypher query and return serialized results."""
    if not NEO4J_AVAILABLE:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Neo4j service unavailable",
            status_code=503,
            details={"reason": "Neo4j driver not available"}
        )
    
    try:
        with neo.get_session() as session:
            result = neo.run_with_retries(session, query, params)
            return [_serialize_neo4j(r.data()) for r in result]
    except Exception as e:
        raise APIError(
            code=ErrorCodes.GRAPH_ERROR,
            message=f"Graph query failed: {str(e)}",
            status_code=500,
            details={"query": query, "error_type": e.__class__.__name__}
        )


def get_ego_network_view(
    node_id: Union[str, int] = Query(..., description="Central node ID"),
    radius: int = Query(default=2, ge=1, le=5, description="Network radius"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum nodes to return"),
    relationship_types: Optional[str] = Query(None, description="Comma-separated relationship types")
):
    """
    Generate ego network visualization data.
    
    Creates a view of the local network around a central node:
    - Configurable radius (number of hops)
    - Relationship type filtering
    - Node limit for performance
    - Automatic layout positioning
    
    Returns positioned nodes and relationships ready for visualization.
    """
    
    # Parse relationship types
    rel_types = []
    if relationship_types:
        rel_types = [rt.strip() for rt in relationship_types.split(",") if rt.strip()]
    
    # Build relationship type filter
    rel_type_filter = ""
    if rel_types:
        rel_type_filter = f":{':'.join(rel_types)}"
    
    # Build Cypher query for ego network
    cypher = f"""
    MATCH (n) WHERE id(n) = $node_id
    OPTIONAL MATCH p = (n)-[r{rel_type_filter}*1..{radius}]-(m)
    RETURN n, collect(p) AS paths
    LIMIT $limit
    """
    
    records = _run_cypher(cypher, {"node_id": int(node_id) if str(node_id).isdigit() else node_id, "limit": limit})
    
    if not records:
        raise APIError(
            code=ErrorCodes.RESOURCE_NOT_FOUND,
            message="Central node not found",
            status_code=404,
            details={"node_id": node_id}
        )
    
    # Process results
    nodes = {}
    rels = {}
    
    def add_node(nd: Dict[str, Any]):
        if isinstance(nd, dict) and nd.get("__type") == "node":
            nid = nd.get("id")
            if nid not in nodes:
                nodes[nid] = ViewNode(
                    id=nid,
                    labels=nd.get("labels", []),
                    properties=nd.get("properties", {})
                )
    
    def add_rel(rr: Dict[str, Any]):
        if isinstance(rr, dict) and rr.get("__type") == "relationship":
            rid = rr.get("id")
            if rid not in rels:
                rels[rid] = ViewRelationship(
                    id=rid,
                    type=rr.get("type", ""),
                    source=rr.get("start"),
                    target=rr.get("end"),
                    properties=rr.get("properties", {})
                )
    
    for rec in records:
        # Add center node
        n_ser = rec.get("n")
        if n_ser:
            add_node(n_ser)
        
        # Process paths
        paths = rec.get("paths") or []
        for p in paths:
            if isinstance(p, dict) and p.get("__type") == "path":
                for nd in p.get("nodes", []):
                    add_node(nd)
                for rr in p.get("relationships", []):
                    add_rel(rr)
    
    # Get center node
    center_node = next(iter(nodes.values())) if nodes else ViewNode(id=node_id, labels=[], properties={})
    
    # Simple circular layout
    import math
    node_list = list(nodes.values())
    if len(node_list) > 1:
        for i, node in enumerate(node_list):
            if node.id == center_node.id:
                node.x, node.y = 0, 0
            else:
                angle = 2 * math.pi * (i - 1) / (len(node_list) - 1)
                radius = 100
                node.x = radius * math.cos(angle)
                node.y = radius * math.sin(angle)
    else:
        center_node.x, center_node.y = 0, 0
    
    metadata = {
        "center_node_id": node_id,
        "radius": radius,
        "total_nodes": len(nodes),
        "total_relationships": len(rels)
    }
    
    return EgoNetworkResponse(
        center_node=center_node,
        nodes=node_list,
        relationships=list(rels.values()),
        metadata=metadata
    )


def get_shortest_path_view(
    source_node: Union[str, int] = Query(..., description="Source node ID"),
    target_node: Union[str, int] = Query(..., description="Target node ID"),
    max_length: int = Query(default=6, ge=1, le=10, description="Maximum path length"),
    relationship_types: Optional[str] = Query(None, description="Comma-separated relationship types")
):
    """
    Generate shortest path visualization data.
    
    Finds and visualizes the shortest path between two nodes:
    - Configurable maximum path length
    - Relationship type filtering
    - Automatic layout for path visualization
    
    Returns positioned path data ready for visualization.
    """
    
    # Parse relationship types
    rel_types = []
    if relationship_types:
        rel_types = [rt.strip() for rt in relationship_types.split(",") if rt.strip()]
    
    # Build relationship type filter
    rel_type_filter = ""
    if rel_types:
        rel_type_filter = f":{':'.join(rel_types)}"
    
    # Build Cypher query for shortest path
    cypher = f"""
    MATCH (a), (b)
    WHERE id(a) = $source_id AND id(b) = $target_id
    MATCH p = shortestPath((a)-[{rel_type_filter}*..{max_length}]-(b))
    RETURN a, b, p
    LIMIT 1
    """
    
    records = _run_cypher(cypher, {
        "source_id": int(source_node) if str(source_node).isdigit() else source_node,
        "target_id": int(target_node) if str(target_node).isdigit() else target_node,
    })
    
    # Check if nodes exist
    if not records:
        # Try to find individual nodes
        node_check = """
        OPTIONAL MATCH (a) WHERE id(a) = $source_id
        OPTIONAL MATCH (b) WHERE id(b) = $target_id
        RETURN a, b
        """
        
        check_records = _run_cypher(node_check, {
            "source_id": int(source_node) if str(source_node).isdigit() else source_node,
            "target_id": int(target_node) if str(target_node).isdigit() else target_node,
        })
        
        if not check_records or not check_records[0].get("a"):
            raise APIError(
                code=ErrorCodes.RESOURCE_NOT_FOUND,
                message="Source node not found",
                status_code=404,
                details={"source_node": source_node}
            )
        
        if not check_records[0].get("b"):
            raise APIError(
                code=ErrorCodes.RESOURCE_NOT_FOUND,
                message="Target node not found",
                status_code=404,
                details={"target_node": target_node}
            )
        
        # Nodes exist but no path found
        source_data = check_records[0]["a"]
        source_view = ViewNode(
            id=source_data.get("id"),
            labels=source_data.get("labels", []),
            properties=source_data.get("properties", {}),
            x=-100, y=0
        )
        
        return PathViewResponse(
            source_node=source_view,
            target_node=None,
            path_found=False,
            nodes=[source_view],
            relationships=[],
            metadata={
                "source_node_id": source_node,
                "target_node_id": target_node,
                "path_found": False,
                "max_length": max_length
            }
        )
    
    record = records[0]
    
    # Extract path data
    source_data = record["a"]
    target_data = record["b"]
    path_data = record["p"]
    
    # Create view nodes
    source_view = ViewNode(
        id=source_data.get("id"),
        labels=source_data.get("labels", []),
        properties=source_data.get("properties", {}),
        x=-100, y=0
    )
    
    target_view = ViewNode(
        id=target_data.get("id"),
        labels=target_data.get("labels", []),
        properties=target_data.get("properties", {}),
        x=100, y=0
    )
    
    # Process path
    path_nodes = {source_view.id: source_view, target_view.id: target_view}
    path_rels = []
    
    if path_data and isinstance(path_data, dict) and path_data.get("__type") == "path":
        # Add intermediate nodes
        for i, node_data in enumerate(path_data.get("nodes", [])[1:-1], 1):
            if node_data and isinstance(node_data, dict):
                node_view = ViewNode(
                    id=node_data.get("id"),
                    labels=node_data.get("labels", []),
                    properties=node_data.get("properties", {}),
                    x=-100 + (200 * i) / (len(path_data.get("nodes", [])) - 1),
                    y=0
                )
                path_nodes[node_view.id] = node_view
        
        # Add relationships
        for rel_data in path_data.get("relationships", []):
            if rel_data and isinstance(rel_data, dict):
                rel_view = ViewRelationship(
                    id=rel_data.get("id"),
                    type=rel_data.get("type", ""),
                    source=rel_data.get("start"),
                    target=rel_data.get("end"),
                    properties=rel_data.get("properties", {})
                )
                path_rels.append(rel_view)
    
    metadata = {
        "source_node_id": source_node,
        "target_node_id": target_node,
        "path_found": True,
        "path_length": len(path_rels),
        "max_length": max_length
    }
    
    return PathViewResponse(
        source_node=source_view,
        target_node=target_view,
        path_found=True,
        nodes=list(path_nodes.values()),
        relationships=path_rels,
        metadata=metadata
    )


def export_dossier_data(
    node_id: Union[str, int] = Query(..., description="Central node ID"),
    radius: int = Query(default=2, ge=1, le=5, description="Export radius"),
    format: str = Query(default="dossier", regex="^(dossier|json)$", description="Export format")
):
    """
    Export graph data in dossier format for external analysis.
    
    Creates structured export data suitable for:
    - InfoTerminal dossier generation
    - External analysis tools
    - Data interchange
    
    Returns comprehensive graph data with metadata.
    """
    
    # Get ego network data
    ego_response = get_ego_network_view(node_id=node_id, radius=radius)
    
    if format == "dossier":
        return {
            "format": "infoterminal_dossier",
            "version": "1.0",
            "center_entity": {
                "id": ego_response.center_node.id,
                "labels": ego_response.center_node.labels,
                "properties": ego_response.center_node.properties
            },
            "entities": [
                {
                    "id": node.id,
                    "labels": node.labels,
                    "properties": node.properties,
                    "position": {"x": node.x, "y": node.y}
                }
                for node in ego_response.nodes
            ],
            "relationships": [
                {
                    "id": rel.id,
                    "type": rel.type,
                    "source": rel.source,
                    "target": rel.target,
                    "properties": rel.properties
                }
                for rel in ego_response.relationships
            ],
            "metadata": ego_response.metadata,
            "export_timestamp": time.time()
        }
    else:  # json format
        return {
            "format": "json",
            "data": ego_response.dict(),
            "export_timestamp": time.time()
        }


# Include V1 routers
app.include_router(
    build_views_router(
        get_ego_handler=get_ego_network_view,
        shortest_path_handler=get_shortest_path_view,
        export_handler=export_dossier_data,
    )
)

# Include existing routers for backward compatibility
try:
    from dossier.api import router as dossier_router
    from geo import router as geo_router
    from ontology.api import router as ontology_router
    
    app.include_router(ontology_router)
    app.include_router(dossier_router)
    app.include_router(geo_router)
except ImportError:
    pass

# Legacy endpoints with deprecation warnings
@app.get("/graphs/view/ego", deprecated=True, tags=["legacy"])
def legacy_ego_view(
    label: str = Query(...),
    key: str = Query(...),
    value: str = Query(...),
    depth: int = Query(1),
    limit: int = Query(1000)
):
    """
    DEPRECATED: Use /v1/views/ego instead.
    
    Legacy ego network endpoint for backward compatibility.
    Will be removed in a future version.
    """
    # This is a simplified conversion - in practice you'd need proper label/key/value lookup
    try:
        response = get_ego_network_view(
            node_id=value,  # Simplified - would need proper node lookup
            radius=depth,
            limit=limit
        )
        
        # Convert to legacy format
        return {
            "nodes": [node.dict() for node in response.nodes],
            "relationships": [rel.dict() for rel in response.relationships],
            "meta": response.metadata
        }
    except Exception as e:
        return {"error": str(e), "nodes": [], "relationships": []}


@app.get("/graphs/view/shortest-path", deprecated=True, tags=["legacy"])
def legacy_shortest_path_view(
    srcLabel: str = Query(...),
    srcKey: str = Query(...),
    srcValue: str = Query(...),
    dstLabel: str = Query(...),
    dstKey: str = Query(...),
    dstValue: str = Query(...),
    maxLen: int = Query(6)
):
    """
    DEPRECATED: Use /v1/views/shortest-path instead.
    
    Legacy shortest path endpoint for backward compatibility.
    Will be removed in a future version.
    """
    try:
        response = get_shortest_path_view(
            source_node=srcValue,  # Simplified - would need proper lookup
            target_node=dstValue,  # Simplified - would need proper lookup
            max_length=maxLen
        )
        
        # Convert to legacy format
        if response.path_found:
            return {
                "path": {
                    "nodes": [node.dict() for node in response.nodes],
                    "relationships": [rel.dict() for rel in response.relationships]
                },
                "found": True
            }
        else:
            return {"path": None, "found": False}
            
    except Exception as e:
        return {"error": str(e), "path": None, "found": False}


# Root endpoint
@app.get("/", tags=["root"])
def root():
    """Service information and available endpoints."""
    return {
        "service": "InfoTerminal Graph Views API",
        "version": app.state.version,
        "status": "running",
        "api_version": "v1",
        "neo4j_available": NEO4J_AVAILABLE,
        "endpoints": {
            "health": "/healthz",
            "ready": "/readyz",
            "docs": "/v1/docs",
            "ego_view": "/v1/views/ego",
            "path_view": "/v1/views/shortest-path",
            "export": "/v1/export/dossier"
        },
        "legacy_endpoints": {
            "ego_view": "/graphs/view/ego (deprecated)",
            "shortest_path": "/graphs/view/shortest-path (deprecated)"
        }
    }
