"""Graph analysis endpoints used by the dossier pipeline."""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field

from analytics import GraphAnalytics
from metrics import (
    GRAPH_ANALYSIS_DURATION,
    GRAPH_ANALYSIS_QUERIES,
    GRAPH_SUBGRAPH_EXPORTS,
    GRAPH_SUBGRAPH_EXPORT_DURATION,
)
from utils.neo4j_client import neo_session


router = APIRouter(prefix="/graphs/analysis", tags=["graph-analysis"])
legacy_router = APIRouter(prefix="/analytics", tags=["analytics"], deprecated=True)


class ShortestPathRequest(BaseModel):
    start_node_id: str
    end_node_id: str
    max_length: int = Field(default=6, ge=1, le=16)
    timeout_ms: Optional[int] = Field(default=None, ge=100, le=30000)


def _record_analysis_metric(algorithm: str, status: str, duration: float) -> None:
    GRAPH_ANALYSIS_QUERIES.labels(algorithm=algorithm, status=status).inc()
    GRAPH_ANALYSIS_DURATION.labels(algorithm=algorithm, status=status).observe(duration)


def _pagination(offset: int, limit: int, returned: int) -> Dict[str, Any]:
    next_offset = offset + returned if returned == limit else None
    previous_offset = max(offset - limit, 0) if offset > 0 else None
    return {
        "limit": limit,
        "offset": offset,
        "returned": returned,
        "next_offset": next_offset,
        "previous_offset": previous_offset,
    }


@router.get("/degree")
def degree_centrality(
    request: Request,
    node_type: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0, le=1000),
    timeout_ms: int | None = Query(default=None, ge=100, le=30000),
) -> Dict[str, Any]:
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")

    started = time.perf_counter()
    try:
        analytics = GraphAnalytics(driver)
        items = analytics.degree_centrality(
            node_type=node_type,
            limit=limit,
            offset=offset,
            timeout_ms=timeout_ms,
        )
        duration = time.perf_counter() - started
        _record_analysis_metric("degree", "success", duration)
        return {
            "algorithm": "degree",
            "node_type": node_type,
            "results": items,
            "pagination": _pagination(offset, limit, len(items)),
        }
    except HTTPException:
        duration = time.perf_counter() - started
        _record_analysis_metric("degree", "error", duration)
        raise
    except Exception as exc:  # pragma: no cover - defensive guard
        duration = time.perf_counter() - started
        _record_analysis_metric("degree", "error", duration)
        raise HTTPException(status_code=500, detail=f"Analytics error: {exc}") from exc


@router.get("/communities")
def louvain_communities(
    request: Request,
    min_size: int = Query(default=3, ge=1, le=50),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0, le=1000),
    timeout_ms: int | None = Query(default=None, ge=100, le=30000),
) -> Dict[str, Any]:
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")

    started = time.perf_counter()
    try:
        analytics = GraphAnalytics(driver)
        payload = analytics.louvain_communities(
            min_size=min_size,
            offset=offset,
            limit=limit,
            timeout_ms=timeout_ms,
        )
        duration = time.perf_counter() - started
        _record_analysis_metric("louvain", "success", duration)
        payload["pagination"] = _pagination(offset, limit, len(payload.get("communities", [])))
        return payload
    except HTTPException:
        duration = time.perf_counter() - started
        _record_analysis_metric("louvain", "error", duration)
        raise
    except Exception as exc:  # pragma: no cover
        duration = time.perf_counter() - started
        _record_analysis_metric("louvain", "error", duration)
        raise HTTPException(status_code=500, detail=f"Analytics error: {exc}") from exc


@router.post("/shortest-path")
def shortest_path(request: Request, payload: ShortestPathRequest) -> Dict[str, Any]:
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")

    algorithm = "shortest_path"
    started = time.perf_counter()
    try:
        timeout = payload.timeout_ms / 1000 if payload.timeout_ms else None
        with neo_session(driver) as session:
            query = """
            MATCH (start {id: $start}), (end {id: $end})
            MATCH path = shortestPath((start)-[*..$max_len]-(end))
            RETURN [n in nodes(path) | {
                id: n.id,
                name: n.name,
                labels: labels(n)
            }] as nodes,
            [r in relationships(path) | type(r)] as relationships,
            length(path) as path_length
            """

            params = {
                "start": payload.start_node_id,
                "end": payload.end_node_id,
                "max_len": payload.max_length,
            }
            run_kwargs: Dict[str, Any] = {}
            if timeout:
                run_kwargs["timeout"] = timeout

            result = session.run(query, parameters=params, **run_kwargs).single()

        duration = time.perf_counter() - started
        _record_analysis_metric(algorithm, "success", duration)

        if not result:
            return {
                "path_found": False,
                "message": "No path found",
                "nodes": [],
                "relationships": [],
            }

        return {
            "path_found": True,
            "nodes": result["nodes"],
            "relationships": result["relationships"],
            "length": result["path_length"],
        }
    except HTTPException:
        duration = time.perf_counter() - started
        _record_analysis_metric(algorithm, "error", duration)
        raise
    except Exception as exc:  # pragma: no cover
        duration = time.perf_counter() - started
        _record_analysis_metric(algorithm, "error", duration)
        raise HTTPException(status_code=500, detail=f"Path analysis error: {exc}") from exc


@router.get("/subgraph-export")
def subgraph_export(
    request: Request,
    center_id: str = Query(..., description="Center node identifier"),
    radius: int = Query(default=2, ge=1, le=5),
    limit: int = Query(default=200, ge=1, le=1000),
    relationship_type: list[str] | None = Query(default=None),
    timeout_ms: int | None = Query(default=None, ge=100, le=30000),
    format: str = Query(default="json", pattern="^(json|markdown)$"),
) -> Dict[str, Any]:
    driver = getattr(request.app.state, "driver", None)
    if not driver:
        raise HTTPException(status_code=503, detail="Neo4j driver not ready")

    started = time.perf_counter()
    try:
        analytics = GraphAnalytics(driver)
        result = analytics.subgraph_export(
            center_id=center_id,
            radius=radius,
            limit=limit,
            relationship_types=relationship_type,
            timeout_ms=timeout_ms,
        )

        duration = time.perf_counter() - started
        GRAPH_SUBGRAPH_EXPORTS.labels(format=format, status="success").inc()
        GRAPH_SUBGRAPH_EXPORT_DURATION.labels(format=format, status="success").observe(duration)

        if format == "markdown":
            return {"markdown": result["markdown"], "center": result["center"]}

        return result
    except HTTPException:
        duration = time.perf_counter() - started
        GRAPH_SUBGRAPH_EXPORTS.labels(format=format, status="error").inc()
        GRAPH_SUBGRAPH_EXPORT_DURATION.labels(format=format, status="error").observe(duration)
        raise
    except Exception as exc:  # pragma: no cover
        duration = time.perf_counter() - started
        GRAPH_SUBGRAPH_EXPORTS.labels(format=format, status="error").inc()
        GRAPH_SUBGRAPH_EXPORT_DURATION.labels(format=format, status="error").observe(duration)
        raise HTTPException(status_code=500, detail=f"Export failed: {exc}") from exc


# Legacy compatibility routes
legacy_router.add_api_route("/centrality/degree", degree_centrality, methods=["GET"])
legacy_router.add_api_route("/communities", louvain_communities, methods=["GET"])
legacy_router.add_api_route("/paths/shortest", shortest_path, methods=["POST"])
