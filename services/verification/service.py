"""Application service layer for verification API."""
from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import redis.asyncio as redis
import structlog
from fastapi import BackgroundTasks, HTTPException, UploadFile

from claim_extractor import ClaimExtractor
from evidence_retrieval import EvidenceRetriever
from media_forensics import media_forensics
from stance_classifier import StanceClassifier

from .models.api_models import (
    ClaimResponse,
    ClassifyStanceRequest,
    CredibilityRequest,
    CredibilityResponse,
    ExtractClaimsRequest,
    ImageSimilarityResponse,
    MediaAnalysisResponse,
    StanceResponse,
    VerificationStatsResponse,
)

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
structlog.configure(
    processors=[structlog.processors.TimeStamper(fmt="iso"), structlog.dev.ConsoleRenderer()],
    logger_factory=structlog.WriteLoggerFactory(),
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    cache_logger_on_first_use=True,
)
logger = structlog.get_logger()


# ---------------------------------------------------------------------------
# Cache Manager
# ---------------------------------------------------------------------------


class CacheManager:
    """Redis cache manager for verification service."""

    def __init__(self, redis_client: Optional[redis.Redis], ttl_seconds: int = 300):
        self.redis = redis_client
        self.ttl_seconds = ttl_seconds
        self.prefix = "verification:"

    def _key(self, namespace: str, payload: str) -> str:
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
        return f"{self.prefix}{namespace}:{digest}"

    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        if not self.redis:
            return None
        try:
            cached = await self.redis.get(key)
            if cached:
                logger.info("cache.hit", key=key)
                return json.loads(cached)
            return None
        except Exception as exc:  # pragma: no cover - cache errors should not break service
            logger.warning("cache.get_error", key=key, error=str(exc))
            return None

    async def set(self, key: str, data: Dict[str, Any]) -> None:
        if not self.redis:
            return
        try:
            await self.redis.setex(key, self.ttl_seconds, json.dumps(data))
            logger.debug("cache.set", key=key)
        except Exception as exc:  # pragma: no cover
            logger.warning("cache.set_error", key=key, error=str(exc))


# ---------------------------------------------------------------------------
# Service implementation
# ---------------------------------------------------------------------------


@dataclass
class VerificationService:
    """Encapsulates verification domain logic and dependencies."""

    redis_host: str = "redis"
    redis_port: int = 6379
    cache_enabled: bool = True

    claim_extractor: Optional[ClaimExtractor] = None
    evidence_retriever: Optional[EvidenceRetriever] = None
    stance_classifier: Optional[StanceClassifier] = None
    redis_client: Optional[redis.Redis] = None
    cache_manager: Optional[CacheManager] = None

    async def startup(self) -> None:
        logger.info("verification.startup")
        await self._init_redis()
        await self._init_components()
        logger.info("verification.ready")

    async def shutdown(self) -> None:
        logger.info("verification.shutdown")
        if self.claim_extractor:
            await self.claim_extractor.cleanup()
        if self.evidence_retriever:
            await self.evidence_retriever.cleanup()
        if self.stance_classifier:
            await self.stance_classifier.cleanup()
        if self.redis_client:
            await self.redis_client.close()
            logger.info("verification.redis_closed")

    async def _init_redis(self) -> None:
        if not self.cache_enabled:
            self.cache_manager = CacheManager(None)
            return
        try:
            self.redis_client = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                decode_responses=True,
                retry_on_timeout=True,
                socket_connect_timeout=5,
            )
            await self.redis_client.ping()
            self.cache_manager = CacheManager(self.redis_client)
            logger.info("verification.redis_connected")
        except Exception as exc:
            logger.warning("verification.redis_unavailable", error=str(exc))
            self.redis_client = None
            self.cache_manager = CacheManager(None)

    async def _init_components(self) -> None:
        self.claim_extractor = ClaimExtractor()
        await self.claim_extractor.initialize()

        self.evidence_retriever = EvidenceRetriever()
        await self.evidence_retriever.initialize()

        self.stance_classifier = StanceClassifier()
        await self.stance_classifier.initialize()

    # ------------------------------------------------------------------
    # Public API methods
    # ------------------------------------------------------------------
    async def extract_claims(
        self,
        request: ExtractClaimsRequest,
        background_tasks: Optional[BackgroundTasks] = None,
    ) -> List[ClaimResponse]:
        if not self.claim_extractor:
            raise HTTPException(status_code=503, detail="Claim extractor not available")
        claims = await self.claim_extractor.extract_claims(
            text=request.text,
            confidence_threshold=request.confidence_threshold,
            max_claims=request.max_claims,
        )
        responses = [
            ClaimResponse(
                id=claim.id,
                text=claim.text,
                confidence=claim.confidence,
                claim_type=claim.claim_type,
                subject=claim.subject,
                predicate=claim.predicate,
                object=claim.object_,
                temporal=claim.temporal,
                location=claim.location,
            )
            for claim in claims
        ]
        if background_tasks is not None:
            background_tasks.add_task(
                self._log_claim_extraction,
                len(request.text),
                len(claims),
                request.confidence_threshold,
            )
        logger.info(
            "claims.extracted",
            count=len(claims),
            avg_confidence=sum((c.confidence for c in claims)) / len(claims) if claims else 0,
        )
        return responses

    async def analyze_image(
        self,
        file: UploadFile,
        background_tasks: BackgroundTasks,
    ) -> MediaAnalysisResponse:
        allowed_types = {
            "image/jpeg",
            "image/jpg",
            "image/png",
            "image/gif",
            "image/bmp",
            "image/tiff",
        }
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file.content_type}. Allowed: {', '.join(sorted(allowed_types))}",
            )
        data = await file.read()
        if len(data) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Maximum size: 10MB")

        analysis = await media_forensics.analyze_image(data, file.filename)
        if "error" in analysis:
            raise HTTPException(status_code=500, detail=analysis["error"])

        background_tasks.add_task(
            self._log_image_analysis,
            file.filename,
            len(data),
            analysis.get("assessment", {}).get("authenticity_score", 0.0),
            len(analysis.get("forensics", {}).get("manipulation_indicators", [])),
        )
        logger.info(
            "media.image_analyzed",
            filename=file.filename,
            authenticity=analysis.get("assessment", {}).get("authenticity_score", 0.0),
        )
        return MediaAnalysisResponse(
            filename=analysis["filename"],
            file_size=analysis["file_size"],
            format=analysis["format"],
            dimensions=analysis["dimensions"],
            has_exif=analysis["exif_data"]["has_exif"],
            exif_data=analysis["exif_data"],
            hashes=analysis["hashes"],
            forensics=analysis["forensics"],
            reverse_search=analysis.get("reverse_search"),
            assessment=analysis["assessment"],
        )

    async def compare_images(
        self,
        file1: UploadFile,
        file2: UploadFile,
    ) -> ImageSimilarityResponse:
        data1, data2 = await asyncio.gather(file1.read(), file2.read())
        analysis1, analysis2 = await asyncio.gather(
            media_forensics.analyze_image(data1, file1.filename),
            media_forensics.analyze_image(data2, file2.filename),
        )

        similarity_details: Dict[str, Any] = {}
        if "hashes" in analysis1 and "hashes" in analysis2:
            hash_types = ["phash", "dhash", "whash", "average_hash"]
            for hash_type in hash_types:
                if hash_type in analysis1["hashes"] and hash_type in analysis2["hashes"]:
                    hash1_int = int(analysis1["hashes"][hash_type], 16)
                    hash2_int = int(analysis2["hashes"][hash_type], 16)
                    hamming_distance = bin(hash1_int ^ hash2_int).count("1")
                    similarity = 1 - (hamming_distance / 64)
                    similarity_details[hash_type] = {
                        "similarity_score": max(0.0, similarity),
                        "hamming_distance": hamming_distance,
                    }
            similarity_details["exact_match"] = (
                analysis1["hashes"].get("sha256") == analysis2["hashes"].get("sha256")
            )

        perceptual_scores = [
            detail["similarity_score"]
            for detail in similarity_details.values()
            if isinstance(detail, dict) and "similarity_score" in detail
        ]
        avg_similarity = sum(perceptual_scores) / len(perceptual_scores) if perceptual_scores else 0.0

        assessment = {
            "likely_same_image": avg_similarity > 0.9,
            "likely_edited_version": 0.7 < avg_similarity <= 0.9,
            "likely_different_images": avg_similarity <= 0.7,
        }

        return ImageSimilarityResponse(
            file1=file1.filename,
            file2=file2.filename,
            exact_match=similarity_details.get("exact_match", False),
            average_similarity=avg_similarity,
            similarity_details=similarity_details,
            assessment=assessment,
        )

    def stats(self) -> VerificationStatsResponse:
        return VerificationStatsResponse(
            service="verification",
            version="0.2.0",
            uptime=time.time(),
            components={
                "claim_extractor": {
                    "status": "ready" if self.claim_extractor else "not_ready",
                    "model_loaded": self.claim_extractor.is_model_loaded() if self.claim_extractor else False,
                },
                "evidence_retriever": {
                    "status": "ready" if self.evidence_retriever else "not_ready",
                    "sources_available": self.evidence_retriever.get_available_sources()
                    if self.evidence_retriever
                    else [],
                },
                "stance_classifier": {
                    "status": "ready" if self.stance_classifier else "not_ready",
                    "model_loaded": self.stance_classifier.is_model_loaded() if self.stance_classifier else False,
                },
                "media_forensics": {
                    "status": "ready",
                    "reverse_search_enabled": media_forensics.reverse_search_enabled,
                    "apis_configured": {
                        "bing": bool(media_forensics.bing_api_key),
                        "google": bool(media_forensics.google_api_key and media_forensics.google_cx_id),
                    },
                },
            },
        )

    # ------------------------------------------------------------------
    # Background logging helpers
    # ------------------------------------------------------------------
    async def _log_image_analysis(
        self,
        filename: str,
        file_size: int,
        authenticity_score: float,
        manipulation_indicators: int,
    ) -> None:
        logger.info(
            "media.image_analysis_log",
            filename=filename,
            file_size=file_size,
            authenticity_score=authenticity_score,
            manipulation_indicators=manipulation_indicators,
        )

    async def _log_claim_extraction(
        self, text_length: int, claims_found: int, confidence_threshold: float
    ) -> None:
        logger.info(
            "claims.extraction_log",
            text_length=text_length,
            claims_found=claims_found,
            confidence_threshold=confidence_threshold,
            claims_per_char=claims_found / text_length if text_length else 0,
        )


__all__ = ["VerificationService", "CacheManager"]
