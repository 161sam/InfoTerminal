# Graph Analytics Module for InfoTerminal

from typing import Dict, List, Optional, Any
from fastapi import HTTPException
import os
from neo4j import GraphDatabase
from pydantic import BaseModel


class CentralityRequest(BaseModel):
    node_type: Optional[str] = None
    limit: Optional[int] = 100


class CommunityRequest(BaseModel):
    algorithm: str = "louvain"  # louvain, label_propagation, weakly_connected
    min_community_size: Optional[int] = 3


class GraphAnalytics:
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver
    
    def degree_centrality(self, node_type: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Calculate degree centrality for nodes."""
        with self.driver.session() as session:
            # Use Neo4j's built-in degree calculation
            query = """
            MATCH (n)
            WHERE ($nodeType IS NULL OR $nodeType IN labels(n))
            WITH n, size((n)--()) as degree
            RETURN n.name as name, labels(n) as labels, degree, id(n) as node_id
            ORDER BY degree DESC
            LIMIT $limit
            """
            
            result = session.run(query, nodeType=node_type, limit=limit)
            return [
                {
                    "node_id": record["node_id"],
                    "name": record["name"],
                    "labels": record["labels"],
                    "degree": record["degree"],
                    "centrality_score": record["degree"]  # Normalized later
                }
                for record in result
            ]
    
    def betweenness_centrality(self, node_type: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Calculate betweenness centrality using Neo4j GDS."""
        with self.driver.session() as session:
            try:
                # Create graph projection if not exists
                session.run("""
                CALL gds.graph.exists('analytics') YIELD exists
                WITH exists
                WHERE NOT exists
                CALL gds.graph.project('analytics', '*', '*')
                YIELD graphName
                RETURN graphName
                """)
                
                # Run betweenness centrality
                query = """
                CALL gds.betweenness.stream('analytics')
                YIELD nodeId, score
                WITH gds.util.asNode(nodeId) AS n, score
                WHERE ($nodeType IS NULL OR $nodeType IN labels(n))
                RETURN n.name as name, labels(n) as labels, score, id(n) as node_id
                ORDER BY score DESC
                LIMIT $limit
                """
                
                result = session.run(query, nodeType=node_type, limit=limit)
                return [
                    {
                        "node_id": record["node_id"],
                        "name": record["name"],
                        "labels": record["labels"], 
                        "centrality_score": record["score"]
                    }
                    for record in result
                ]
            
            except Exception as e:
                # Fallback to simple path counting if GDS not available
                return self._simple_betweenness(node_type, limit)
    
    def louvain_communities(self, min_size: int = 3) -> Dict[str, Any]:
        """Detect communities using Louvain algorithm."""
        with self.driver.session() as session:
            try:
                # Ensure graph projection exists
                session.run("""
                CALL gds.graph.exists('analytics') YIELD exists
                WITH exists
                WHERE NOT exists
                CALL gds.graph.project('analytics', '*', '*')
                YIELD graphName
                RETURN graphName
                """)
                
                # Run Louvain community detection
                query = """
                CALL gds.louvain.stream('analytics')
                YIELD nodeId, communityId
                WITH communityId, collect(gds.util.asNode(nodeId)) AS members
                WHERE size(members) >= $minSize
                RETURN communityId, 
                       [n IN members | {
                           node_id: id(n),
                           name: n.name, 
                           labels: labels(n)
                       }] AS members,
                       size(members) AS size
                ORDER BY size DESC
                """
                
                result = session.run(query, minSize=min_size)
                communities = []
                
                for record in result:
                    communities.append({
                        "id": record["communityId"],
                        "size": record["size"],
                        "members": record["members"]
                    })
                
                return {
                    "algorithm": "louvain",
                    "community_count": len(communities),
                    "communities": communities
                }
                
            except Exception as e:
                # Fallback to connected components
                return self._simple_communities(min_size)
    
    def _simple_betweenness(self, node_type: str, limit: int) -> List[Dict[str, Any]]:
        """Simplified betweenness calculation without GDS."""
        with self.driver.session() as session:
            query = """
            MATCH (n)
            WHERE ($nodeType IS NULL OR $nodeType IN labels(n))
            WITH n, size((n)--()) as connections
            RETURN n.name as name, labels(n) as labels, 
                   connections * 0.5 as centrality_score, id(n) as node_id
            ORDER BY centrality_score DESC
            LIMIT $limit
            """
            
            result = session.run(query, nodeType=node_type, limit=limit)
            return [
                {
                    "node_id": record["node_id"],
                    "name": record["name"],
                    "labels": record["labels"],
                    "centrality_score": record["centrality_score"]
                }
                for record in result
            ]
    
    def _simple_communities(self, min_size: int) -> Dict[str, Any]:
        """Simple community detection using connected components."""
        with self.driver.session() as session:
            # Find connected components
            query = """
            MATCH (n)
            OPTIONAL MATCH (n)-[*]-(connected)
            WITH n, collect(DISTINCT connected) + [n] as component
            WHERE size(component) >= $minSize
            RETURN DISTINCT component,
                   [node IN component | {
                       node_id: id(node),
                       name: node.name, 
                       labels: labels(node)
                   }] as members,
                   size(component) as size
            ORDER BY size DESC
            LIMIT 20
            """
            
            result = session.run(query, minSize=min_size)
            communities = []
            
            for i, record in enumerate(result):
                communities.append({
                    "id": i,
                    "size": record["size"],
                    "members": record["members"]
                })
            
            return {
                "algorithm": "connected_components",
                "community_count": len(communities),
                "communities": communities
            }
    
    def graph_summary(self) -> Dict[str, Any]:
        """Get overall graph statistics."""
        with self.driver.session() as session:
            # Get node counts by label
            node_stats = session.run("""
            MATCH (n)
            UNWIND labels(n) as label
            RETURN label, count(*) as count
            ORDER BY count DESC
            """)
            
            # Get relationship counts by type
            rel_stats = session.run("""
            MATCH ()-[r]->()
            RETURN type(r) as rel_type, count(r) as count
            ORDER BY count DESC
            """)
            
            # Get total counts
            totals = session.run("""
            MATCH (n)
            WITH count(n) as node_count
            MATCH ()-[r]->()
            RETURN node_count, count(r) as relationship_count
            """).single()
            
            return {
                "total_nodes": totals["node_count"] if totals else 0,
                "total_relationships": totals["relationship_count"] if totals else 0,
                "node_types": [{"label": record["label"], "count": record["count"]} 
                              for record in node_stats],
                "relationship_types": [{"type": record["rel_type"], "count": record["count"]} 
                                     for record in rel_stats]
            }

    def node2vec_embeddings(self, dimensions: int = 32, walk_length: int = 80, walks_per_node: int = 10, window_size: int = 10) -> Dict[str, Any]:
        """Compute Node2Vec embeddings via Neo4j GDS if available; otherwise return error payload."""
        with self.driver.session() as session:
            try:
                session.run("""
                CALL gds.graph.exists('n2v') YIELD exists
                WITH exists
                WHERE NOT exists
                CALL gds.graph.project('n2v', '*', '*') YIELD graphName
                RETURN graphName
                """)
                records = session.run(
                    "CALL gds.node2vec.stream('n2v', {embeddingDimension: $dim, walkLength: $wl, walksPerNode: $w, windowSize: $ws}) "
                    "YIELD nodeId, embedding RETURN gds.util.asNode(nodeId).name AS name, embedding LIMIT 500",
                    dim=dimensions, wl=walk_length, w=walks_per_node, ws=window_size
                )
                items = [{"name": r["name"], "embedding": r["embedding"]} for r in records]
                return {"algorithm": "node2vec", "dimension": dimensions, "items": items}
            except Exception as e:
                return {"error": "gds_unavailable_or_failed", "detail": str(e)}

    def pagerank(self, node_type: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        with self.driver.session() as session:
            try:
                session.run("""
                CALL gds.graph.exists('pr') YIELD exists
                WITH exists
                WHERE NOT exists
                CALL gds.graph.project('pr', '*', '*') YIELD graphName
                RETURN graphName
                """)
                query = """
                CALL gds.pageRank.stream('pr')
                YIELD nodeId, score
                WITH gds.util.asNode(nodeId) AS n, score
                WHERE ($nodeType IS NULL OR $nodeType IN labels(n))
                RETURN n.name as name, labels(n) as labels, score, id(n) as node_id
                ORDER BY score DESC
                LIMIT $limit
                """
                result = session.run(query, nodeType=node_type, limit=limit)
                return [
                    {"node_id": r["node_id"], "name": r["name"], "labels": r["labels"], "score": r["score"]}
                    for r in result
                ]
            except Exception as e:
                # fallback to degree based proxy
                return self.degree_centrality(node_type, limit)
