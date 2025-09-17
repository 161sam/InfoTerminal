# Analytics routes for graph algorithms and statistics

from typing import Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

# Import analytics from parent directory
import sys
from pathlib import Path
SERVICE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SERVICE_DIR))
from analytics import GraphAnalytics, CentralityRequest, CommunityRequest
from utils.neo4j_client import neo_session

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/centrality/degree")
def get_degree_centrality(
    request: Request,
    node_type: Optional[str] = None, 
    limit: int = 100
):
    """Get degree centrality for nodes."""
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")
    
    try:
        analytics = GraphAnalytics(driver)
        result = analytics.degree_centrality(node_type, limit)
        return {
            "centrality_type": "degree", 
            "nodes": result,
            "total_nodes": len(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")


@router.get("/centrality/betweenness") 
def get_betweenness_centrality(
    request: Request,
    node_type: Optional[str] = None, 
    limit: int = 100
):
    """Get betweenness centrality for nodes."""
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")
    
    try:
        analytics = GraphAnalytics(driver)
        result = analytics.betweenness_centrality(node_type, limit)
        return {
            "centrality_type": "betweenness", 
            "nodes": result,
            "total_nodes": len(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")


@router.post("/communities")
def detect_communities(request: Request, community_request: CommunityRequest):
    """Detect communities in the graph."""
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")
    
    try:
        analytics = GraphAnalytics(driver)
        
        if community_request.algorithm == "louvain":
            result = analytics.louvain_communities(community_request.min_community_size or 3)
        else:
            raise HTTPException(400, f"Unsupported algorithm: {community_request.algorithm}")
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")


@router.get("/summary")
def graph_summary(request: Request):
    """Get overall graph statistics."""
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")
    
    try:
        analytics = GraphAnalytics(driver)
        return analytics.graph_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")


@router.get("/embeddings/node2vec")
def node2vec_embeddings(
    request: Request,
    dimensions: int = 32,
    walk_length: int = 80,
    walks_per_node: int = 10,
    window_size: int = 10,
):
    """Compute Node2Vec embeddings via Neo4j GDS (limited set)."""
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")

    try:
        analytics = GraphAnalytics(driver)
        return analytics.node2vec_embeddings(dimensions, walk_length, walks_per_node, window_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")


@router.get("/pagerank")
def pagerank(request: Request, node_type: str | None = None, limit: int = 100):
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")
    try:
        analytics = GraphAnalytics(driver)
        return {"algorithm": "pagerank", "nodes": analytics.pagerank(node_type, limit)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")


class PathRequest(BaseModel):
    start_node_id: str
    end_node_id: str
    max_length: Optional[int] = 6


@router.post("/paths/shortest")
def shortest_path(request: Request, path_request: PathRequest):
    """Find shortest path between two nodes."""
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")
    
    try:
        with neo_session(driver) as session:
            query = """
            MATCH (start {id: $start}), (end {id: $end})
            MATCH path = shortestPath((start)-[*..%d]-(end))
            RETURN [n in nodes(path) | {
                id: n.id,
                name: n.name,
                labels: labels(n)
            }] as nodes,
            [r in relationships(path) | type(r)] as relationships,
            length(path) as path_length
            """ % (path_request.max_length or 6)
            
            result = session.run(query, 
                               start=path_request.start_node_id, 
                               end=path_request.end_node_id).single()
            
            if not result:
                return {"path_found": False, "message": "No path found"}
            
            return {
                "path_found": True,
                "nodes": result["nodes"],
                "relationships": result["relationships"], 
                "length": result["path_length"]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Path analysis error: {str(e)}")


@router.get("/node/{node_id}/influence")
def node_influence(request: Request, node_id: str, depth: int = 2):
    """Analyze a node's influence in its neighborhood."""
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")
    
    try:
        with neo_session(driver) as session:
            # Get node's direct and indirect connections
            query = """
            MATCH (n {id: $node_id})
            OPTIONAL MATCH (n)-[*1..%d]-(connected)
            WITH n, collect(DISTINCT connected) as neighborhood
            RETURN {
                node: {id: n.id, name: n.name, labels: labels(n)},
                direct_connections: size([(n)--() | 1]),
                neighborhood_size: size(neighborhood),
                influence_score: size(neighborhood) * 1.0 / $depth
            } as result
            """ % depth
            
            result = session.run(query, node_id=node_id, depth=depth).single()
            
            if not result:
                raise HTTPException(404, "Node not found")
                
            return result["result"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Influence analysis error: {str(e)}")
