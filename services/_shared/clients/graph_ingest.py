"""Async client for pushing structured artefacts into the graph service.

The client prefers talking to the graph-api over HTTP but gracefully falls
back to writing JSON payloads to disk when the API is unreachable. This keeps
smoke tests and offline demos deterministic while still exercising the
ingestion contract used in production deployments.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger(__name__)


class GraphIngestClient:
    """Small helper that pushes plugin/video artefacts into graph-api.

    Parameters
    ----------
    base_url:
        Optional override for the graph-api base URL. When omitted the client
        honours the ``GRAPH_API_URL`` environment variable.
    fallback_dir:
        Directory used to persist payloads when HTTP ingestion is disabled or
        fails. Defaults to ``/tmp/graph_ingest`` to keep artefacts accessible
        during local development.
    timeout:
        Request timeout in seconds when calling graph-api.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        *,
        fallback_dir: Optional[Path] = None,
        timeout: float = 5.0,
    ) -> None:
        self.base_url = base_url or os.getenv("GRAPH_API_URL")
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
        self._lock = asyncio.Lock()
        self.fallback_dir = Path(
            fallback_dir
            or os.getenv("GRAPH_INGEST_FALLBACK_DIR", "/tmp/graph_ingest")
        )

    async def _ensure_client(self) -> Optional[httpx.AsyncClient]:
        if not self.base_url:
            return None

        async with self._lock:
            if self._client is None:
                self._client = httpx.AsyncClient(
                    base_url=self.base_url,
                    timeout=self.timeout,
                    headers={"User-Agent": "InfoTerminal-GraphIngest/1.0"},
                )
        return self._client

    async def close(self) -> None:
        async with self._lock:
            if self._client is not None:
                await self._client.aclose()
                self._client = None

    async def ingest_plugin_run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send plugin execution artefacts to the graph service."""

        filename = f"plugin_run_{payload.get('job_id', 'unknown')}.json"
        return await self._submit("/v1/ingest/plugin-run", payload, filename)

    async def ingest_video_analysis(
        self, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send processed video metadata to the graph service."""

        video_id = payload.get("video", {}).get("id", "unknown")
        filename = f"video_analysis_{video_id}.json"
        return await self._submit("/v1/ingest/video", payload, filename)

    async def _submit(
        self, endpoint: str, payload: Dict[str, Any], fallback_filename: str
    ) -> Dict[str, Any]:
        client = await self._ensure_client()
        if client:
            try:
                response = await client.post(endpoint, json=payload)
                response.raise_for_status()
                logger.debug(
                    "graph ingest succeeded for %s with status %s",
                    endpoint,
                    response.status_code,
                )
                return response.json()
            except Exception as exc:  # pragma: no cover - network failure path
                logger.warning(
                    "graph ingest failed for %s, using fallback: %s",
                    endpoint,
                    exc,
                )

        # Fall back to writing the payload locally for offline demos/tests
        self.fallback_dir.mkdir(parents=True, exist_ok=True)
        path = self.fallback_dir / fallback_filename
        path.write_text(json.dumps(payload, indent=2, default=str))
        logger.info("graph ingest stored locally %s", path)
        return {"status": "stored", "path": str(path)}


__all__ = ["GraphIngestClient"]

