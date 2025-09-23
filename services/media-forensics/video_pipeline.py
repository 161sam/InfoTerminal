"""Simplified video processing pipeline for the media-forensics service."""

from __future__ import annotations

import asyncio
import os
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
from PIL import Image, ImageSequence

try:  # pragma: no cover - allow direct execution in tests
    from .metrics import VIDEO_FRAMES_PROCESSED_TOTAL
except ImportError:  # pragma: no cover
    from metrics import VIDEO_FRAMES_PROCESSED_TOTAL


@dataclass
class VideoPipelineConfig:
    frame_interval: int = 5
    min_area: int = 500
    max_frames: int = 240
    brightness_threshold: float = 25.0


class VideoPipeline:
    """Extract frames from GIF/animated formats and perform contour detection."""

    def __init__(self, default_config: VideoPipelineConfig | None = None) -> None:
        self.default_config = default_config or VideoPipelineConfig()

    async def process_video(
        self,
        video_bytes: bytes,
        filename: str,
        *,
        frame_interval: int | None = None,
        min_area: int | None = None,
        max_frames: int | None = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        config = VideoPipelineConfig(
            frame_interval=frame_interval or self.default_config.frame_interval,
            min_area=min_area or self.default_config.min_area,
            max_frames=max_frames or self.default_config.max_frames,
            brightness_threshold=self.default_config.brightness_threshold,
        )
        return await asyncio.to_thread(
            self._process_sync,
            video_bytes,
            filename,
            config,
        )

    def _process_sync(
        self, video_bytes: bytes, filename: str, config: VideoPipelineConfig
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix or ".gif")
        try:
            temp_file.write(video_bytes)
            temp_file.flush()
            temp_file.close()

            with Image.open(temp_file.name) as img:
                total_frames = getattr(img, "n_frames", 1)
                frame_duration_ms = img.info.get("duration", 100)
                frame_interval = max(1, int(config.frame_interval))
                max_frames = max(1, int(config.max_frames))
                fps = 1000.0 / frame_duration_ms if frame_duration_ms else 1.0

                video_id = uuid.uuid5(uuid.NAMESPACE_URL, f"{filename}-{len(video_bytes)}").hex
                scenes: List[Dict[str, Any]] = []
                graph_entities: List[Dict[str, Any]] = [
                    {
                        "type": "Video",
                        "id": video_id,
                        "properties": {
                            "filename": filename,
                            "duration_seconds": round((total_frames * frame_duration_ms) / 1000.0, 3),
                            "total_frames": total_frames,
                            "video_pipeline_enabled": True,
                        },
                    }
                ]

                processed_frames = 0
                object_count = 0
                for frame_index, frame in enumerate(ImageSequence.Iterator(img)):
                    if frame_index % frame_interval != 0:
                        continue
                    if processed_frames >= max_frames:
                        break

                    frame_rgb = frame.convert("RGB")
                    frame_array = np.asarray(frame_rgb)
                    timestamp = (frame_index * frame_duration_ms) / 1000.0
                    objects = self._detect_objects(
                        frame_array,
                        video_id,
                        len(scenes),
                        config.min_area,
                        config.brightness_threshold,
                    )
                    object_count += len(objects)

                    scene_id = f"{video_id}-scene-{len(scenes)}"
                    scenes.append(
                        {
                            "scene_id": scene_id,
                            "frame_index": frame_index,
                            "timestamp": round(float(timestamp), 3),
                            "objects": objects,
                        }
                    )

                    graph_entities.append(
                        {
                            "type": "VideoScene",
                            "id": scene_id,
                            "properties": {
                                "frame_index": frame_index,
                                "timestamp": round(float(timestamp), 3),
                            },
                            "relationships": [
                                {"target": video_id, "type": "PART_OF"}
                            ],
                        }
                    )

                    for obj in objects:
                        graph_entities.append(
                            {
                                "type": "VideoObject",
                                "id": obj["object_id"],
                                "properties": {
                                    "label": obj["label"],
                                    "confidence": obj["confidence"],
                                    **{f"bbox_{k}": v for k, v in obj["bbox"].items()},
                                },
                                "relationships": [
                                    {"target": scene_id, "type": "DETECTED_IN"}
                                ],
                            }
                        )

                    processed_frames += 1

            VIDEO_FRAMES_PROCESSED_TOTAL.labels(pipeline="media_forensics").inc(
                processed_frames
            )

            summary = {
                "total_frames": total_frames,
                "frames_processed": processed_frames,
                "objects_detected": object_count,
                "frame_interval": frame_interval,
            }

            analysis_payload = {
                "video_id": video_id,
                "filename": filename,
                "duration_seconds": graph_entities[0]["properties"]["duration_seconds"],
                "scenes": scenes,
                "summary": summary,
                "graph_entities": graph_entities,
            }

            graph_payload = {
                "video": graph_entities[0]["properties"] | {"id": video_id},
                "scenes": scenes,
                "summary": summary,
            }

            return analysis_payload, graph_payload
        finally:
            try:
                os.unlink(temp_file.name)
            except OSError:
                pass

    def _detect_objects(
        self,
        frame: np.ndarray,
        video_id: str,
        scene_index: int,
        min_area: int,
        brightness_threshold: float,
    ) -> List[Dict[str, Any]]:
        gray = frame.mean(axis=2)
        mask = gray > brightness_threshold
        components = self._extract_components(mask, min_area)

        detections: List[Dict[str, Any]] = []
        frame_area = frame.shape[0] * frame.shape[1]
        for idx, (y0, y1, x0, x1, area) in enumerate(components):
            confidence = min(1.0, float(area) / max(frame_area, 1))
            detections.append(
                {
                    "object_id": f"{video_id}-obj-{scene_index}-{idx}",
                    "label": "object",
                    "confidence": round(confidence, 3),
                    "bbox": {
                        "x": int(x0),
                        "y": int(y0),
                        "width": int(x1 - x0 + 1),
                        "height": int(y1 - y0 + 1),
                    },
                }
            )
        return detections

    def _extract_components(
        self, mask: np.ndarray, min_area: int
    ) -> List[Tuple[int, int, int, int, int]]:
        visited = np.zeros_like(mask, dtype=bool)
        components: List[Tuple[int, int, int, int, int]] = []
        height, width = mask.shape

        for y, x in np.argwhere(mask):
            if visited[y, x]:
                continue
            stack = [(y, x)]
            visited[y, x] = True
            min_y = max_y = y
            min_x = max_x = x
            area = 0

            while stack:
                cy, cx = stack.pop()
                area += 1
                min_y = min(min_y, cy)
                max_y = max(max_y, cy)
                min_x = min(min_x, cx)
                max_x = max(max_x, cx)

                for ny, nx in (
                    (cy - 1, cx),
                    (cy + 1, cx),
                    (cy, cx - 1),
                    (cy, cx + 1),
                ):
                    if 0 <= ny < height and 0 <= nx < width:
                        if mask[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            stack.append((ny, nx))

            if area >= max(10, min_area):
                components.append((min_y, max_y, min_x, max_x, area))

        return components


__all__ = ["VideoPipeline", "VideoPipelineConfig"]
