"""Pydantic models for verification service endpoints."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# Request Models
class ExtractClaimsRequest(BaseModel):
    """Request for extracting claims from text."""
    text: str = Field(..., description="Text to extract claims from", min_length=1)
    confidence_threshold: float = Field(0.7, ge=0.0, le=1.0, description="Minimum confidence threshold")
    max_claims: int = Field(10, ge=1, le=100, description="Maximum number of claims to extract")


class FindEvidenceRequest(BaseModel):
    """Request for finding evidence for a claim."""
    claim: str = Field(..., description="Claim to find evidence for", min_length=1)
    max_sources: int = Field(5, ge=1, le=20, description="Maximum number of evidence sources")
    source_types: List[str] = Field(
        default_factory=lambda: ["web", "wikipedia", "news"],
        description="Types of sources to search"
    )
    language: str = Field("en", description="Language for evidence search")


class ClassifyStanceRequest(BaseModel):
    """Request for classifying stance between claim and evidence."""
    claim: str = Field(..., description="Original claim", min_length=1)
    evidence: str = Field(..., description="Evidence text", min_length=1)
    context: Optional[str] = Field(None, description="Additional context")


class CredibilityRequest(BaseModel):
    """Request for assessing source credibility."""
    source_url: str = Field(..., description="URL of the source to assess")
    domain: Optional[str] = Field(None, description="Domain name if URL parsing fails")


class BatchClaimsRequest(BaseModel):
    """Request for batch claim processing."""
    texts: List[str] = Field(..., description="List of texts to process", min_items=1, max_items=50)
    confidence_threshold: float = Field(0.7, ge=0.0, le=1.0, description="Confidence threshold")
    max_claims_per_text: int = Field(5, ge=1, le=20, description="Max claims per text")


class SummarizationRequest(BaseModel):
    """Legacy request model for text summarization."""
    text: str = Field(..., description="Text to summarize", min_length=1)
    max_length: int = Field(150, ge=50, le=500, description="Maximum summary length")


# Response Models
class ClaimResponse(BaseModel):
    """Response model for extracted claims."""
    id: str = Field(..., description="Unique claim identifier")
    text: str = Field(..., description="Claim text")
    confidence: float = Field(..., description="Confidence score", ge=0.0, le=1.0)
    claim_type: str = Field(..., description="Type of claim")
    subject: str = Field(..., description="Subject of the claim")
    predicate: str = Field(..., description="Predicate/action of the claim")
    object: str = Field(..., description="Object of the claim")
    temporal: Optional[str] = Field(None, description="Temporal context")
    location: Optional[str] = Field(None, description="Location context")


class EvidenceResponse(BaseModel):
    """Response model for evidence items."""
    id: str = Field(..., description="Unique evidence identifier")
    source_url: str = Field(..., description="Source URL")
    source_title: str = Field(..., description="Source title")
    source_type: str = Field(..., description="Type of source")
    snippet: str = Field(..., description="Relevant text snippet")
    relevance_score: float = Field(..., description="Relevance to claim", ge=0.0, le=1.0)
    credibility_score: float = Field(..., description="Source credibility", ge=0.0, le=1.0)
    publication_date: Optional[str] = Field(None, description="Publication date")
    author: Optional[str] = Field(None, description="Author name")


class StanceResponse(BaseModel):
    """Response model for stance classification."""
    stance: str = Field(..., description="Stance classification", pattern="^(support|contradict|neutral|unrelated)$")
    confidence: float = Field(..., description="Classification confidence", ge=0.0, le=1.0)
    reasoning: str = Field(..., description="Explanation of the classification")
    key_phrases: List[str] = Field(..., description="Key phrases that influenced classification")


class CredibilityResponse(BaseModel):
    """Response model for credibility assessment."""
    credibility_score: float = Field(..., description="Overall credibility score", ge=0.0, le=1.0)
    bias_rating: str = Field(..., description="Bias assessment")
    factual_reporting: str = Field(..., description="Factual reporting quality")
    transparency_score: float = Field(..., description="Transparency score", ge=0.0, le=1.0)
    authority_indicators: List[str] = Field(..., description="Indicators of authority")
    red_flags: List[str] = Field(..., description="Credibility red flags")


class MediaAnalysisResponse(BaseModel):
    """Response model for media analysis."""
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes", ge=0)
    format: str = Field(..., description="Media format")
    dimensions: Dict[str, int] = Field(..., description="Media dimensions")
    has_exif: bool = Field(..., description="Whether EXIF data is present")
    exif_data: Dict[str, Any] = Field(..., description="EXIF metadata")
    hashes: Dict[str, str] = Field(..., description="Various hash values")
    manipulation_indicators: List[str] = Field(default_factory=list, description="Potential manipulation signs")
    authenticity_score: Optional[float] = Field(None, description="Authenticity assessment", ge=0.0, le=1.0)


class ImageSimilarityResponse(BaseModel):
    """Response model for image similarity comparison."""
    similarity_score: float = Field(..., description="Similarity score", ge=0.0, le=100.0)
    hash_distance: int = Field(..., description="Hamming distance between hashes", ge=0)
    likely_match: bool = Field(..., description="Whether images are likely the same")
    analysis: Dict[str, Any] = Field(..., description="Detailed comparison analysis")


class VerificationStatsResponse(BaseModel):
    """Response model for service statistics."""
    total_claims_processed: int = Field(..., description="Total claims processed", ge=0)
    total_evidence_retrieved: int = Field(..., description="Total evidence items retrieved", ge=0)
    total_images_analyzed: int = Field(..., description="Total images analyzed", ge=0)
    uptime_seconds: float = Field(..., description="Service uptime in seconds", ge=0.0)
    cache_hit_rate: Optional[float] = Field(None, description="Cache hit rate percentage", ge=0.0, le=100.0)
    processing_times: Dict[str, float] = Field(default_factory=dict, description="Average processing times")


class BatchClaimsResponse(BaseModel):
    """Response model for batch claim processing."""
    results: List[Dict[str, Any]] = Field(..., description="Results for each processed text")
    total_texts: int = Field(..., description="Total number of texts processed", ge=0)
    total_claims: int = Field(..., description="Total claims extracted", ge=0)
    processing_time_seconds: float = Field(..., description="Total processing time", ge=0.0)


class VerificationPipelineResponse(BaseModel):
    """Response model for complete verification pipeline."""
    original_text: str = Field(..., description="Original input text")
    claims: List[Dict[str, Any]] = Field(..., description="Processed claims with evidence and analysis")
    processing_summary: Dict[str, int] = Field(..., description="Summary of processing counts")
    confidence_assessment: Optional[str] = Field(None, description="Overall confidence assessment")


class SourceInfo(BaseModel):
    """Information about an evidence source."""
    name: str = Field(..., description="Source name")
    type: str = Field(..., description="Source type")
    status: str = Field(..., description="Availability status")
    description: str = Field(..., description="Source description")


class SourcesResponse(BaseModel):
    """Response model for available sources."""
    sources: List[SourceInfo] = Field(..., description="Available evidence sources")
    total_sources: int = Field(..., description="Total number of sources", ge=0)
    message: str = Field(..., description="Additional information about source availability")


# Error Models
class VerificationError(BaseModel):
    """Error model for verification operations."""
    operation: str = Field(..., description="Operation that failed")
    error_code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
