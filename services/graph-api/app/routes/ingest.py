"""Lightweight ingestion endpoints used by plugin runner and video pipeline."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from utils.neo4j_client import neo_session


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


class ThreatIndicator(BaseModel):
    indicator: str = Field(..., description="Indicator value (IP, domain, hash, …)")
    type: str = Field(..., description="Indicator type as reported by the feed")
    source: str = Field(..., description="Source pulse or feed identifier")
    first_seen: Optional[str] = Field(
        None, description="First seen timestamp as ISO8601 string"
    )
    tags: List[str] = Field(
        default_factory=list, description="Associated threat tags"
    )


class ThreatIndicatorBatch(BaseModel):
    items: List[ThreatIndicator] = Field(
        default_factory=list, description="Normalised threat indicators"
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


@router.post("/ingest/threat-indicators")
async def ingest_threat_indicators(
    payload: ThreatIndicatorBatch, request: Request
) -> Dict[str, Any]:
    """Upsert AlienVault OTX style indicators into the graph."""

    app = request.app
    driver = getattr(app.state, "driver", None)
    processed = len(payload.items)
    ingested = 0

    if not payload.items:
        return {"status": "ok", "processed": 0, "ingested": 0}

    if driver is not None:
        with neo_session(driver) as session:
            for item in payload.items:
                tags = item.tags or []
                result = session.run(
                    """
                    MERGE (feed:ThreatFeed {name: $source})
                    ON CREATE SET feed.created_at = timestamp()
                    SET feed.updated_at = timestamp()
                    MERGE (indicator:ThreatIndicator {source: $source, value: $indicator})
                    ON CREATE SET
                        indicator.type = $type,
                        indicator.first_seen = $first_seen,
                        indicator.created_at = timestamp(),
                        indicator.updated_at = timestamp()
                    ON MATCH SET
                        indicator.type = $type,
                        indicator.first_seen = $first_seen,
                        indicator.updated_at = timestamp()
                    WITH feed, indicator, CASE WHEN indicator.updated_at = indicator.created_at THEN true ELSE false END AS created
                    MERGE (feed)-[:PROVIDES]->(indicator)
                    FOREACH (tag IN $tags |
                        MERGE (t:ThreatTag {name: tag})
                        MERGE (indicator)-[:TAGGED_AS]->(t)
                    )
                    RETURN created
                    """,
                    {
                        "indicator": item.indicator,
                        "type": item.type,
                        "source": item.source,
                        "first_seen": item.first_seen,
                        "tags": tags,
                    },
                )
                record = result.single()
                if record and record.get("created"):
                    ingested += 1
    else:
        cache: Dict[str, Dict[str, Any]] = getattr(
            app.state, "threat_indicator_store", {}
        )
        seen: Set[str] = getattr(app.state, "threat_indicator_seen", set())
        for item in payload.items:
            key = f"{item.source}:{item.indicator}"
            if key in seen:
                continue
            seen.add(key)
            cache[key] = item.model_dump()
            ingested += 1
        app.state.threat_indicator_store = cache
        app.state.threat_indicator_seen = seen

    app.state.last_threat_ingest = {
        "processed": processed,
        "ingested": ingested,
    }

    return {"status": "ok", "processed": processed, "ingested": ingested}


__all__ = ["router"]

