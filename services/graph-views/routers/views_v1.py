"""Domain router for graph view endpoints."""
from __future__ import annotations

from typing import Callable

from fastapi import APIRouter

from ..models.view_models import EgoNetworkResponse, PathViewResponse


def build_views_router(
    *,
    get_ego_handler: Callable,
    shortest_path_handler: Callable,
    export_handler: Callable,
) -> APIRouter:
    """Create router exposing v1 graph view endpoints using provided handlers."""
    router = APIRouter(prefix="/v1")

    router.get(
        "/views/ego",
        response_model=EgoNetworkResponse,
        tags=["views"],
        summary="Get ego network view",
        description="Generate ego network visualization data",
    )(get_ego_handler)

    router.post(
        "/views/shortest-path",
        response_model=PathViewResponse,
        tags=["views"],
        summary="Find shortest path",
        description="Find shortest path between two nodes",
    )(shortest_path_handler)

    router.get(
        "/export/dossier",
        response_model=dict,
        tags=["export"],
        summary="Export dossier data",
        description="Export graph data in dossier format",
    )(export_handler)

    return router
