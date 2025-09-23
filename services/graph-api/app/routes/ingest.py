"""Lightweight ingestion endpoints used by plugin runner and video pipeline."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field


class PluginEntity(BaseModel):
    type: str = Field(..., description="Graph entity label")
    id: Optional[str] = Field(None, description="Stable identifier")
    properties: Dict[str, Any] = Field(
        default_factory=dict, description="Node properties"
    )


class PluginRunIngest(BaseModel):
    job_id: str = Field(..., description="Plugin job identifier")
    plugin_name: str = Field(..., description="Name of the plugin")
    status: str = Field(..., description="Final job status")
    completed_at: Optional[str] = Field(
        None, description="Completion timestamp ISO8601"
    )
    execution_time: Optional[float] = Field(
        None, description="Execution duration in seconds"
    )
    graph_entities: List[PluginEntity] = Field(
        default_factory=list, description="Extracted graph entities"
    )
    search_documents: List[Dict[str, Any]] = Field(
        default_factory=list, description="Documents to forward to search"
    )


class DetectedObject(BaseModel):
    object_id: str = Field(..., description="Object identifier")
    label: str = Field(..., description="Detected label")
    confidence: float = Field(..., ge=0.0, le=1.0)
    bbox: Dict[str, Any] = Field(..., description="Bounding box properties")


class VideoScene(BaseModel):
    scene_id: str = Field(..., description="Scene identifier")
    frame_index: int = Field(..., ge=0)
    timestamp: float = Field(..., ge=0.0)
    objects: List[DetectedObject] = Field(default_factory=list)


class VideoIngest(BaseModel):
    video: Dict[str, Any] = Field(..., description="Video metadata")
    scenes: List[VideoScene] = Field(..., description="Detected scenes")
    summary: Dict[str, Any] = Field(
        default_factory=dict, description="Aggregated summary"
    )


router = APIRouter(prefix="/v1", tags=["Ingest"])


@router.post("/ingest/plugin-run")
async def ingest_plugin_run(payload: PluginRunIngest, request: Request) -> Dict[str, Any]:
    """Persist plugin execution artefacts for graph exploration."""

    app = request.app
    log = getattr(app.state, "plugin_runs", [])
    entry = payload.model_dump()
    entry["ingested_at"] = datetime.utcnow().isoformat()
    log.append(entry)
    app.state.plugin_runs = log

    # Flag last plugin name for quick access in status endpoints
    app.state.last_plugin_ingest = payload.plugin_name

    return {"status": "ok", "ingested_entities": len(payload.graph_entities)}


@router.post("/ingest/video")
async def ingest_video(payload: VideoIngest, request: Request) -> Dict[str, Any]:
    """Store simplified video pipeline metadata for downstream analysis."""

    app = request.app
    entries = getattr(app.state, "video_analyses", [])
    entry = payload.model_dump()
    entry["ingested_at"] = datetime.utcnow().isoformat()
    entries.append(entry)
    app.state.video_analyses = entries
    app.state.video_pipeline_enabled = True

    return {
        "status": "ok",
        "scenes": len(payload.scenes),
        "objects": sum(len(scene.objects) for scene in payload.scenes),
    }


__all__ = ["router"]

