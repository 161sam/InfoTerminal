"""Prometheus collectors for the media forensics video pipeline."""

from prometheus_client import Counter


VIDEO_FRAMES_PROCESSED_TOTAL = Counter(
    "video_frames_processed_total",
    "Total number of frames processed by the media pipeline",
    labelnames=("pipeline",),
)


__all__ = ["VIDEO_FRAMES_PROCESSED_TOTAL"]

