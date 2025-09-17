import os
import math
from typing import Dict, List, Any
from collections import defaultdict, deque
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from neo4j import GraphDatabase

router = APIRouter(prefix="/alg", tags=["algorithms"])

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://it-neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASSWORD", "test12345")
USE_GDS = os.getenv("IT_NEO4J_GDS", "0") == "1"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

# Input Models
class DegreeIn(BaseModel):
    nodeLabel: str | None = None
    direction: str | None = None  # "IN" | "OUT" | "BOTH"

class CentralityIn(BaseModel):
    nodeLabel: str | None = None
    limit: int = 100

class CommunityIn(BaseModel):
    nodeLabel: str | None = None
    relationshipType: str | None = None
    limit: int = 100

class ShortestIn(BaseModel):
    sourceId: int
    targetId: int
    weightProp: str | None = None

class PageRankIn(BaseModel):
    nodeLabel: str | None = None
    iterations: int = 20
    dampingFactor: float = 0.85
    limit: int = 100

# Utility Functions
def get_graph_data(session, node_label: str = None, relationship_type: str = None):
    """Retrieve graph data for in-memory algorithms"""
    nodes_query = "MATCH (n) RETURN id(n) as id, labels(n) as labels"
    if node_label:
        nodes_query = f"MATCH (n:`{node_label}`) RETURN id(n) as id, labels(n) as labels"
    
    edges_query = "MATCH (n)-[r]->(m) RETURN id(n) as source, id(m) as target, type(r) as type"
    if relationship_type:
        edges_query = f"MATCH (n)-[r:`{relationship_type}`]->(m) RETURN id(n) as source, id(m) as target, type(r) as type"
    
    nodes = list(session.run(nodes_query))
    edges = list(session.run(edges_query))
    
    return nodes, edges

def build_adjacency_list(edges):
    """Build adjacency list from edges for in-memory algorithms"""
    adj_list = defaultdict(list)
    for edge in edges:
        adj_list[edge['source']].append(edge['target'])
        adj_list[edge['target']].append(edge['source'])  # Undirected
    return adj_list

def cypher_betweenness_centrality(session, node_label: str = None, limit: int = 100):
    """Approximate betweenness centrality using Cypher queries"""
    # Use a sampling approach for performance on large graphs
    sample_query = """
    MATCH (n)
    {} 
    WITH n, rand() as r
    ORDER BY r
    LIMIT 50
    RETURN id(n) as node_id
    """.format(f"WHERE '{node_label}' IN labels(n)" if node_label else "")
    
    sample_nodes = [record['node_id'] for record in session.run(sample_query)]
    betweenness_scores = defaultdict(float)
    
    # For each pair of sample nodes, find shortest paths and count path intersections
    for i, source in enumerate(sample_nodes):
        for target in sample_nodes[i+1:]:
            # Find all shortest paths between source and target
            path_query = """
            MATCH (s), (t) WHERE id(s) = $source AND id(t) = $target
            MATCH paths = allShortestPaths((s)-[*..6]-(t))
            UNWIND nodes(paths) as n
            RETURN id(n) as node_id, count(*) as path_count
            """
            
            try:
                results = session.run(path_query, source=source, target=target)
                for record in results:
                    if record['node_id'] not in [source, target]:
                        betweenness_scores[record['node_id']] += record['path_count']
            except Exception:
                continue  # Skip if paths are too complex
    
    # Normalize scores
    n = len(sample_nodes)
    if n > 2:
        normalization_factor = 2.0 / ((n - 1) * (n - 2))
        for node_id in betweenness_scores:
            betweenness_scores[node_id] *= normalization_factor
    
    # Convert to sorted list
    results = [{'id': node_id, 'score': score} 
               for node_id, score in sorted(betweenness_scores.items(), 
                                          key=lambda x: x[1], reverse=True)[:limit]]
    
    return results

def cypher_louvain_clustering(session, node_label: str = None, limit: int = 100):
    """Simple community detection using label propagation algorithm in Cypher"""
    
    # Initialize: each node is its own community
    init_query = """
    MATCH (n)
    {}
    SET n.community = id(n)
    RETURN count(n) as initialized
    """.format(f"WHERE '{node_label}' IN labels(n)" if node_label else "")
    
    session.run(init_query)
    
    # Iterative label propagation (simplified Louvain-like approach)
    for iteration in range(10):  # Max 10 iterations
        update_query = """
        MATCH (n)-[r]-(neighbor)
        {}
        WITH n, neighbor.community as neighbor_community, count(r) as weight
        ORDER BY weight DESC
        WITH n, collect(neighbor_community)[0] as most_frequent_community
        WHERE n.community <> most_frequent_community
        SET n.community = most_frequent_community
        RETURN count(n) as updated
        """.format(f"WHERE '{node_label}' IN labels(n)" if node_label else "")
        
        result = session.run(update_query).single()
        if not result or result['updated'] == 0:
            break  # Converged
    
    # Get final communities
    result_query = """
    MATCH (n)
    {}
    RETURN id(n) as id, n.community as communityId
    ORDER BY n.community, id(n)
    LIMIT $limit
    """.format(f"WHERE '{node_label}' IN labels(n)" if node_label else "")
    
    results = list(session.run(result_query, limit=limit))
    
    # Clean up temporary property
    cleanup_query = f"MATCH (n) REMOVE n.community"
    session.run(cleanup_query)
    
    return results

def cypher_pagerank(session, node_label: str = None, iterations: int = 20, 
                   damping_factor: float = 0.85, limit: int = 100):
    """PageRank implementation using iterative Cypher queries"""
    
    # Initialize PageRank values
    init_query = """
    MATCH (n)
    {}
    SET n.pagerank = 1.0
    RETURN count(n) as initialized
    """.format(f"WHERE '{node_label}' IN labels(n)" if node_label else "")
    
    session.run(init_query)
    
    # Get total node count for normalization
    count_query = """
    MATCH (n)
    {}
    RETURN count(n) as total_nodes
    """.format(f"WHERE '{node_label}' IN labels(n)" if node_label else "")
    
    total_nodes = session.run(count_query).single()['total_nodes']
    
    # Iterative PageRank computation
    for iteration in range(iterations):
        update_query = """
        MATCH (n)
        {}
        OPTIONAL MATCH (n)<-[r]-(inbound)
        OPTIONAL MATCH (inbound)-[r2]->()
        WITH n, inbound, count(r2) as outbound_count
        WITH n, sum(CASE WHEN inbound IS NOT NULL THEN inbound.pagerank / outbound_count ELSE 0 END) as incoming_rank
        SET n.pagerank_new = (1.0 - $damping) / $total_nodes + $damping * incoming_rank
        """.format(f"WHERE '{node_label}' IN labels(n)" if node_label else "")
        
        session.run(update_query, damping=damping_factor, total_nodes=total_nodes)
        
        # Update pagerank values
        session.run("MATCH (n) SET n.pagerank = n.pagerank_new REMOVE n.pagerank_new")
    
    # Get final results
    result_query = """
    MATCH (n)
    {}
    RETURN id(n) as id, n.pagerank as score
    ORDER BY n.pagerank DESC
    LIMIT $limit
    """.format(f"WHERE '{node_label}' IN labels(n)" if node_label else "")
    
    results = list(session.run(result_query, limit=limit))
    
    # Clean up
    session.run("MATCH (n) REMOVE n.pagerank")
    
    return results

# API Endpoints
@router.post("/degree")
def degree(inp: DegreeIn):
    """Compute degree centrality for nodes"""
    with driver.session() as s:
        if USE_GDS:
            # GDS implementation
            direction_param = inp.direction or "BOTH"
            q = """
            CALL gds.degree.stream({
                nodeProjection: $label,
                relationshipProjection: '*',
                orientation: $direction
            }) YIELD nodeId, score 
            RETURN gds.util.asNode(nodeId).id AS id, score
            ORDER BY score DESC
            LIMIT 100
            """
            return {"items": s.run(q, label=inp.nodeLabel or "*", direction=direction_param).data()}
        else:
            # Cypher fallback
            direction_clause = ""
            if inp.direction == "IN":
                direction_clause = "<-[r]-"
            elif inp.direction == "OUT":
                direction_clause = "-[r]->"
            else:
                direction_clause = "-[r]-"
            
            if inp.nodeLabel:
                q = f"""
                MATCH (n:`{inp.nodeLabel}`)
                OPTIONAL MATCH (n){direction_clause}()
                RETURN id(n) AS id, count(r) AS degree
                ORDER BY degree DESC
                LIMIT 100
                """
            else:
                q = f"""
                MATCH (n)
                OPTIONAL MATCH (n){direction_clause}()
                RETURN id(n) AS id, count(r) AS degree
                ORDER BY degree DESC
                LIMIT 100
                """
            return {"items": s.run(q).data()}

@router.post("/betweenness")
def betweenness(inp: CentralityIn):
    """Compute betweenness centrality for nodes"""
    with driver.session() as s:
        if USE_GDS:
            q = """
            CALL gds.betweenness.stream({
                nodeProjection: $label,
                relationshipProjection: '*'
            }) 
            YIELD nodeId, score 
            RETURN gds.util.asNode(nodeId).id AS id, score
            ORDER BY score DESC
            LIMIT $limit
            """
            return {"items": s.run(q, label=inp.nodeLabel or "*", limit=inp.limit).data()}
        else:
            # Cypher fallback - approximation for performance
            results = cypher_betweenness_centrality(s, inp.nodeLabel, inp.limit)
            return {"items": results}

@router.post("/closeness")
def closeness(inp: CentralityIn):
    """Compute closeness centrality for nodes"""
    with driver.session() as s:
        if USE_GDS:
            q = """
            CALL gds.closeness.stream({
                nodeProjection: $label,
                relationshipProjection: '*'
            })
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId).id AS id, score
            ORDER BY score DESC
            LIMIT $limit
            """
            return {"items": s.run(q, label=inp.nodeLabel or "*", limit=inp.limit).data()}
        else:
            # Cypher approximation - average shortest path length
            q = """
            MATCH (n)
            {}
            CALL {{
                WITH n
                MATCH (n)-[*1..4]-(other)
                WHERE n <> other
                RETURN avg(length(shortestPath((n)-[*]-(other)))) as avg_distance
            }}
            WITH n, avg_distance
            WHERE avg_distance > 0
            RETURN id(n) as id, 1.0/avg_distance as score
            ORDER BY score DESC
            LIMIT $limit
            """.format(f"WHERE '{inp.nodeLabel}' IN labels(n)" if inp.nodeLabel else "")
            
            return {"items": s.run(q, limit=inp.limit).data()}

@router.post("/pagerank")
def pagerank(inp: PageRankIn):
    """Compute PageRank centrality for nodes"""
    with driver.session() as s:
        if USE_GDS:
            q = """
            CALL gds.pageRank.stream({
                nodeProjection: $label,
                relationshipProjection: '*',
                maxIterations: $iterations,
                dampingFactor: $damping
            })
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId).id AS id, score
            ORDER BY score DESC
            LIMIT $limit
            """
            return {"items": s.run(q, 
                                 label=inp.nodeLabel or "*", 
                                 iterations=inp.iterations,
                                 damping=inp.dampingFactor,
                                 limit=inp.limit).data()}
        else:
            # Cypher implementation
            results = cypher_pagerank(s, inp.nodeLabel, inp.iterations, inp.dampingFactor, inp.limit)
            return {"items": results}

@router.post("/louvain")
def louvain(inp: CommunityIn):
    """Compute Louvain community detection"""
    with driver.session() as s:
        if USE_GDS:
            q = """
            CALL gds.louvain.stream({
                nodeProjection: $label, 
                relationshipProjection: $relType
            }) 
            YIELD nodeId, communityId 
            RETURN id(gds.util.asNode(nodeId)) AS id, communityId
            ORDER BY communityId, id
            LIMIT $limit
            """
            return {"items": s.run(q, 
                                 label=inp.nodeLabel or "*", 
                                 relType=inp.relationshipType or "*",
                                 limit=inp.limit).data()}
        else:
            # Cypher fallback using label propagation
            results = cypher_louvain_clustering(s, inp.nodeLabel, inp.limit)
            return {"items": results}

@router.post("/label-propagation")
def label_propagation(inp: CommunityIn):
    """Compute Label Propagation community detection"""
    with driver.session() as s:
        if USE_GDS:
            q = """
            CALL gds.labelPropagation.stream({
                nodeProjection: $label,
                relationshipProjection: $relType
            })
            YIELD nodeId, communityId
            RETURN id(gds.util.asNode(nodeId)) AS id, communityId
            ORDER BY communityId, id
            LIMIT $limit
            """
            return {"items": s.run(q, 
                                 label=inp.nodeLabel or "*", 
                                 relType=inp.relationshipType or "*",
                                 limit=inp.limit).data()}
        else:
            # Use the same implementation as Louvain fallback
            results = cypher_louvain_clustering(s, inp.nodeLabel, inp.limit)
            return {"items": results}

@router.post("/shortest")
def shortest(inp: ShortestIn):
    """Find shortest path between two nodes"""
    with driver.session() as s:
        if USE_GDS and inp.weightProp:
            # For weighted shortest path, we'd need a projected graph
            # This is more complex with GDS, so we'll use Cypher even with GDS enabled
            pass
            
        # Cypher implementation (works with or without weights)
        if inp.weightProp:
            q = """
            MATCH (s), (t) WHERE id(s) = $sid AND id(t) = $tid
            CALL apoc.algo.dijkstra(s, t, $weightProp) YIELD path, weight
            RETURN path, weight
            """
            try:
                result = s.run(q, sid=inp.sourceId, tid=inp.targetId, weightProp=inp.weightProp).single()
                if result:
                    return {"path": result["path"], "weight": result["weight"]}
            except Exception:
                # APOC not available, fall back to unweighted
                pass
        
        # Unweighted shortest path
        q = """
        MATCH (s), (t) WHERE id(s) = $sid AND id(t) = $tid
        MATCH p = shortestPath((s)-[*..10]-(t))
        RETURN p as path, length(p) as length
        """
        result = s.run(q, sid=inp.sourceId, tid=inp.targetId).single()
        return {"path": result["path"] if result else None, 
                "length": result["length"] if result else None}

@router.get("/centrality-summary/{node_id}")
def centrality_summary(node_id: int):
    """Get a summary of all centrality measures for a specific node"""
    with driver.session() as s:
        # Get basic node info
        node_query = "MATCH (n) WHERE id(n) = $node_id RETURN n, labels(n) as labels"
        node_result = s.run(node_query, node_id=node_id).single()
        
        if not node_result:
            raise HTTPException(404, f"Node {node_id} not found")
        
        # Calculate different centrality measures
        centralities = {}
        
        # Degree centrality
        degree_query = "MATCH (n)-[r]-() WHERE id(n) = $node_id RETURN count(r) as degree"
        degree_result = s.run(degree_query, node_id=node_id).single()
        centralities['degree'] = degree_result['degree'] if degree_result else 0
        
        # Local clustering coefficient
        clustering_query = """
        MATCH (n) WHERE id(n) = $node_id
        OPTIONAL MATCH (n)-[r1]-(neighbor1)-[r2]-(neighbor2)-[r3]-(n)
        WHERE neighbor1 <> neighbor2
        WITH n, count(DISTINCT neighbor1) as neighbors, count(r2)/2 as triangles
        RETURN CASE WHEN neighbors > 1 THEN (triangles * 2.0) / (neighbors * (neighbors - 1)) ELSE 0 END as clustering
        """
        clustering_result = s.run(clustering_query, node_id=node_id).single()
        centralities['clustering'] = clustering_result['clustering'] if clustering_result else 0
        
        return {
            "node_id": node_id,
            "labels": node_result["labels"],
            "centralities": centralities
        }

@router.get("/community-stats")
def community_stats():
    """Get overall community statistics"""
    with driver.session() as s:
        # Basic graph stats
        stats_query = """
        MATCH (n)
        OPTIONAL MATCH (n)-[r]->()
        RETURN count(DISTINCT n) as nodes, count(r) as edges
        """
        stats = s.run(stats_query).single()
        
        # Density calculation
        nodes = stats['nodes']
        edges = stats['edges']
        max_edges = nodes * (nodes - 1)  # for directed graph
        density = (edges / max_edges) if max_edges > 0 else 0
        
        return {
            "nodes": nodes,
            "edges": edges,
            "density": density,
            "avg_degree": (edges * 2 / nodes) if nodes > 0 else 0
        }
