import sys
from pathlib import Path

import numpy as np
import pytest
from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
SERVICE_DIR = ROOT / "services" / "media-forensics"
if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))
if str(ROOT / "services") not in sys.path:
    sys.path.insert(0, str(ROOT / "services"))

from video_pipeline import VideoPipeline  # type: ignore  # noqa: E402


@pytest.mark.asyncio
async def test_video_pipeline_detects_objects(tmp_path):
    frames = []
    for idx in range(6):
        frame = np.zeros((64, 64, 3), dtype=np.uint8)
        frame[10 + idx : 30 + idx, 10:30] = 255
        frames.append(Image.fromarray(frame))

    video_path = tmp_path / "demo.gif"
    frames[0].save(video_path, save_all=True, append_images=frames[1:], duration=100, loop=0)
    video_bytes = video_path.read_bytes()

    pipeline = VideoPipeline()
    analysis, graph_payload = await pipeline.process_video(
        video_bytes,
        "demo.gif",
        frame_interval=1,
        min_area=50,
        max_frames=10,
    )

    assert analysis["summary"]["frames_processed"] > 0
    assert analysis["graph_entities"][0]["type"] == "Video"
    assert graph_payload["summary"]["frames_processed"] == analysis["summary"]["frames_processed"]
