# Graph Analytics Module for InfoTerminal

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from pydantic import BaseModel


class CentralityRequest(BaseModel):
    node_type: Optional[str] = None
    limit: Optional[int] = 100
    offset: int = 0
    timeout_ms: Optional[int] = None


class CommunityRequest(BaseModel):
    algorithm: str = "louvain"  # louvain, label_propagation, weakly_connected
    min_community_size: Optional[int] = 3
    offset: int = 0
    limit: int = 20
    timeout_ms: Optional[int] = None


class GraphAnalytics:
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver
    
    def degree_centrality(
        self,
        node_type: str | None = None,
        limit: int = 100,
        offset: int = 0,
        timeout_ms: int | None = None,
    ) -> List[Dict[str, Any]]:
        """Calculate degree centrality for nodes."""
        with self.driver.session() as session:
            # Use Neo4j's built-in degree calculation
            query = """
            MATCH (n)
            WHERE ($nodeType IS NULL OR $nodeType IN labels(n))
            WITH n, size((n)--()) as degree
            RETURN n.name as name, labels(n) as labels, degree, id(n) as node_id
            ORDER BY degree DESC
            SKIP $offset
            LIMIT $limit
            """

            params = {"nodeType": node_type, "limit": limit, "offset": offset}
            run_kwargs: Dict[str, Any] = {}
            if timeout_ms:
                run_kwargs["timeout"] = timeout_ms / 1000

            result = session.run(query, parameters=params, **run_kwargs)
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
    
    def betweenness_centrality(
        self,
        node_type: str | None = None,
        limit: int = 100,
        offset: int = 0,
        timeout_ms: int | None = None,
    ) -> List[Dict[str, Any]]:
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
                SKIP $offset
                LIMIT $limit
                """

                params = {"nodeType": node_type, "limit": limit, "offset": offset}
                run_kwargs: Dict[str, Any] = {}
                if timeout_ms:
                    run_kwargs["timeout"] = timeout_ms / 1000

                result = session.run(query, parameters=params, **run_kwargs)
                return [
                    {
                        "node_id": record["node_id"],
                        "name": record["name"],
                        "labels": record["labels"], 
                        "centrality_score": record["score"]
                    }
                    for record in result
                ]
            
            except Exception:
                # Fallback to simple path counting if GDS not available
                return self._simple_betweenness(node_type, limit, offset)
    
    def louvain_communities(
        self,
        min_size: int = 3,
        offset: int = 0,
        limit: int = 20,
        timeout_ms: int | None = None,
    ) -> Dict[str, Any]:
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
                
                run_kwargs: Dict[str, Any] = {}
                if timeout_ms:
                    run_kwargs["timeout"] = timeout_ms / 1000

                result = session.run(query, parameters={"minSize": min_size}, **run_kwargs)
                communities = []

                for record in result:
                    communities.append({
                        "id": record["communityId"],
                        "size": record["size"],
                        "members": record["members"]
                    })

                communities = communities[offset: offset + limit]

                return {
                    "algorithm": "louvain",
                    "community_count": len(communities),
                    "communities": communities
                }

            except Exception:
                # Fallback to connected components
                return self._simple_communities(min_size, offset, limit)
    
    def _simple_betweenness(self, node_type: str, limit: int, offset: int = 0) -> List[Dict[str, Any]]:
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
            
            result = session.run(query, nodeType=node_type, limit=limit + offset)
            items = [
                {
                    "node_id": record["node_id"],
                    "name": record["name"],
                    "labels": record["labels"],
                    "centrality_score": record["centrality_score"]
                }
                for record in result
            ]
            return items[offset: offset + limit]

    def _simple_communities(self, min_size: int, offset: int = 0, limit: int = 20) -> Dict[str, Any]:
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

            communities = communities[offset: offset + limit]

            return {
                "algorithm": "connected_components",
                "community_count": len(communities),
                "communities": communities
            }

    def subgraph_export(
        self,
        center_id: str,
        radius: int = 2,
        limit: int = 200,
        relationship_types: Optional[List[str]] = None,
        timeout_ms: int | None = None,
    ) -> Dict[str, Any]:
        """Export a bounded subgraph around a center node."""

        rel_filter = ""
        if relationship_types:
            rel_types = [f"`{rel}`" for rel in relationship_types]
            rel_filter = " WHERE type(r) IN $relTypes"

        query = f"""
        MATCH (center {{id: $center_id}})
        WITH center
        CALL {{
            WITH center
            MATCH path = (center)-[*..$radius]-(neighbor)
            WITH collect(nodes(path)) AS node_paths, center
            UNWIND node_paths AS np
            UNWIND np AS node
            WITH DISTINCT node, center
            RETURN collect(node)[0..$limit] AS nodes
        }}
        WITH center, nodes
        UNWIND nodes AS node
        WITH center, collect(DISTINCT node) AS nodes
        CALL {{
            WITH nodes
            MATCH (n)-[r]-(m)
            WHERE n IN nodes AND m IN nodes
            {rel_filter}
            RETURN collect(DISTINCT r)[0..$limit] AS relationships
        }}
        RETURN center, nodes, relationships
        """

        params: Dict[str, Any] = {
            "center_id": center_id,
            "radius": radius,
            "limit": limit,
        }
        if relationship_types:
            params["relTypes"] = relationship_types

        run_kwargs: Dict[str, Any] = {}
        if timeout_ms:
            run_kwargs["timeout"] = timeout_ms / 1000

        with self.driver.session() as session:
            record = session.run(query, parameters=params, **run_kwargs).single()
            if not record:
                raise HTTPException(404, f"No node found with id {center_id}")

            center_node = record["center"]
            nodes = record["nodes"]
            relationships = record["relationships"]

            def _node_payload(node: Any) -> Dict[str, Any]:
                props = dict(node)
                return {
                    "id": node.id,
                    "labels": list(node.labels),
                    "properties": props,
                }

            def _rel_payload(rel: Any) -> Dict[str, Any]:
                props = dict(rel)
                return {
                    "id": rel.id,
                    "type": rel.type,
                    "source": rel.start_node.id,
                    "target": rel.end_node.id,
                    "properties": props,
                }

            payload_nodes = [_node_payload(node) for node in nodes]
            payload_relationships = [_rel_payload(rel) for rel in relationships]

            # Compose Markdown summary
            lines = [f"### Subgraph Export for `{center_id}`", ""]
            lines.append("#### Nodes")
            for node in payload_nodes:
                name = node["properties"].get("name") or node["properties"].get("title")
                node_title = name or node["id"]
                labels = ", ".join(node["labels"])
                lines.append(f"- **{node_title}** (`{labels}`) – id `{node['id']}`")
            if not payload_nodes:
                lines.append("- _No nodes discovered within radius._")

            lines.append("")
            lines.append("#### Relationships")
            for rel in payload_relationships:
                lines.append(
                    f"- `{rel['type']}`: {rel['source']} → {rel['target']}"
                )
            if not payload_relationships:
                lines.append("- _No relationships within constraints._")

            markdown = "\n".join(lines)

            return {
                "center": _node_payload(center_node),
                "nodes": payload_nodes,
                "relationships": payload_relationships,
                "markdown": markdown,
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
