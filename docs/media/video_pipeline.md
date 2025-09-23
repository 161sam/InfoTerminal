# Video Pipeline Quickstart (Wave 3)

This document explains how to run the media-forensics video pipeline shipped in Wave 3. The pipeline extracts frames from animated formats (GIF/MP4 via Pillow), performs lightweight object detection with NumPy, and ingests scene metadata into the graph service while keeping everything offline-friendly.

## 1. Enable the Feature Flag

The video endpoint is feature-flagged off by default. Enable it per environment:

```bash
export VIDEO_PIPELINE_ENABLED=1
export MEDIA_MAX_FILE_SIZE=$((75 * 1024 * 1024))   # optional override
export MEDIA_GRAPH_FALLBACK_DIR="$(pwd)/tmp/video-graph"
```

The service exposes `/v1/videos/analyze` only when the flag is set. Upload size validation and frame sampling options are guarded by `VideoAnalysisRequest` (frame interval, min contour area, max frames).

## 2. Submit a Video for Analysis

```bash
# create a tiny demo GIF (optional)
python - <<'PY'
import numpy as np
from PIL import Image
frames = []
for i in range(6):
    frame = np.zeros((64, 64, 3), dtype=np.uint8)
    frame[10 + i : 30 + i, 10:30] = 255
    frames.append(Image.fromarray(frame))
frames[0].save("demo.gif", save_all=True, append_images=frames[1:], duration=120, loop=0)
PY

curl -X POST http://localhost:8631/v1/videos/analyze \
  -F "file=@demo.gif" \
  -F "frame_interval=2" \
  -F "min_area=120" \
  -F "max_frames=120"
```

Response payload:

```json
{
  "video_id": "<hash>",
  "filename": "demo.avi",
  "duration_seconds": 3.2,
  "scenes": [
    {
      "scene_id": "<video>-scene-0",
      "frame_index": 0,
      "timestamp": 0.0,
      "objects": [
        {"object_id": "<video>-obj-0-0", "label": "object", "confidence": 0.84, "bbox": {"x": 10, "y": 8, "width": 20, "height": 20}}
      ]
    }
  ],
  "summary": {
    "total_frames": 96,
    "frames_processed": 48,
    "objects_detected": 12,
    "frame_interval": 2
  },
  "graph_entities": [ ... ]
}
```

## 3. Under the Hood

- `video_pipeline.VideoPipeline` writes the upload to a temp file, samples every *n*-th frame, and detects bright contours via NumPy BFS. Each detection becomes a `VideoObject` with bounding box metadata. 【F:services/media-forensics/video_pipeline.py†L1-L200】
- `video_frames_processed_total{pipeline="media_forensics"}` increments with every processed frame. 【F:services/media-forensics/metrics.py†L1-L11】
- Parsed scenes, objects, and summary data are forwarded to the graph service via `_shared.clients.graph_ingest.GraphIngestClient`. Payloads are stored under `MEDIA_GRAPH_FALLBACK_DIR` when `GRAPH_API_URL` is not set. 【F:services/_shared/clients/graph_ingest.py†L1-L120】
- The Graph API exposes `/v1/ingest/video`, recording the latest analyses and flipping `video_pipeline_enabled` for status endpoints. 【F:services/graph-api/app/routes/ingest.py†L1-L120】

## 4. Observability & Dashboards

- Prometheus metrics:
  - `video_frames_processed_total{pipeline="media_forensics"}` — frames processed.
  - `plugin_run_total{plugin="nmap"}` — plugin executions (displayed alongside video stats for Wave 3 dashboards).
- Grafana “Video Frames Processed Rate” panel visualises `rate(video_frames_processed_total[5m])`. 【F:monitoring/grafana-dashboards/infoterminal-overview.json†L560-L660】

## 5. Tests & Offline Demo

- `services/media-forensics/tests/test_video_pipeline.py` synthesises a dummy video with OpenCV, processes it, and asserts object detection plus summary metrics. 【F:services/media-forensics/tests/test_video_pipeline.py†L1-L60】
- `services/plugin-runner/tests/test_nmap_ingest.py` complements the media pipeline by verifying plugin runs produce graph ingest payloads (used together in the README demo script).

## 6. Next Steps

- Integrate NiFi ingestion templates to orchestrate uploads.
- Extend the detection stage with ML models (YOLO/Detectron) once GPU resources are available.
- Build a verification UI that consumes the scenes/objects stored via `/v1/ingest/video`.
