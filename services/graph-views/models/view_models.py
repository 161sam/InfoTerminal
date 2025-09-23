"""Pydantic models for graph views responses."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class ViewNode(BaseModel):
    """Graph view node representation."""

    id: Union[str, int] = Field(..., description="Node identifier")
    labels: List[str] = Field(..., description="Node labels")
    properties: Dict[str, Any] = Field(..., description="Node properties")
    x: Optional[float] = Field(None, description="X coordinate for visualization")
    y: Optional[float] = Field(None, description="Y coordinate for visualization")
    size: Optional[float] = Field(None, description="Node size for visualization")
    color: Optional[str] = Field(None, description="Node color for visualization")


class ViewRelationship(BaseModel):
    """Graph view relationship representation."""

    id: Union[str, int] = Field(..., description="Relationship identifier")
    type: str = Field(..., description="Relationship type")
    source: Union[str, int] = Field(..., description="Source node ID")
    target: Union[str, int] = Field(..., description="Target node ID")
    properties: Dict[str, Any] = Field(..., description="Relationship properties")
    weight: Optional[float] = Field(None, description="Relationship weight for visualization")
    color: Optional[str] = Field(None, description="Relationship color for visualization")


class EgoNetworkResponse(BaseModel):
    """Ego network view response."""

    center_node: ViewNode = Field(..., description="Central node")
    nodes: List[ViewNode] = Field(..., description="Network nodes")
    relationships: List[ViewRelationship] = Field(..., description="Network relationships")
    metadata: Dict[str, Any] = Field(..., description="View metadata")


class PathViewResponse(BaseModel):
    """Path view response."""

    source_node: ViewNode = Field(..., description="Source node")
    target_node: Optional[ViewNode] = Field(None, description="Target node (if found)")
    path_found: bool = Field(..., description="Whether path was found")
    nodes: List[ViewNode] = Field(..., description="All nodes in path")
    relationships: List[ViewRelationship] = Field(..., description="All relationships in path")
    metadata: Dict[str, Any] = Field(..., description="Path finding metadata")
