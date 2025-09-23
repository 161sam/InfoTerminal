"""
Pydantic models for Media Forensics Service v1.
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class ImageDimensions(BaseModel):
    """Image dimensions."""
    width: int = Field(..., description="Image width in pixels", ge=1)
    height: int = Field(..., description="Image height in pixels", ge=1)


class PerceptualHashes(BaseModel):
    """Perceptual hashes for similarity detection."""
    phash: str = Field(..., description="Perceptual hash")
    dhash: str = Field(..., description="Difference hash") 
    whash: str = Field(..., description="Wavelet hash")


class ForensicAnalysis(BaseModel):
    """Forensic analysis results."""
    md5_hash: str = Field(..., description="MD5 hash of the image file")
    sha256_hash: str = Field(..., description="SHA256 hash of the image file")
    color_depth: int = Field(..., description="Number of color channels")
    has_transparency: bool = Field(..., description="Whether image has transparency")
    estimated_jpeg_quality: Optional[int] = Field(None, description="Estimated JPEG quality (0-100)")
    potential_manipulation_signs: List[str] = Field(default_factory=list, description="Detected manipulation indicators")


class ImageAnalysisRequest(BaseModel):
    """Request parameters for image analysis."""
    include_reverse_search: bool = Field(False, description="Whether to include reverse image search results")


class ImageAnalysisResult(BaseModel):
    """Complete image analysis result."""
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes", ge=0)
    image_format: str = Field(..., description="Image format (JPEG, PNG, etc.)")
    dimensions: ImageDimensions = Field(..., description="Image dimensions")
    exif_data: Dict[str, Any] = Field(default_factory=dict, description="EXIF metadata")
    perceptual_hash: Union[PerceptualHashes, Dict[str, str]] = Field(..., description="Perceptual hashes for similarity")
    forensic_analysis: ForensicAnalysis = Field(..., description="Forensic analysis results")
    reverse_search_results: Optional[List[Dict[str, Any]]] = Field(None, description="Reverse image search results")


class ComparisonAnalysis(BaseModel):
    """Detailed comparison analysis between two images."""
    hash1: str = Field(..., description="Hash of first image")
    hash2: str = Field(..., description="Hash of second image")
    dimensions1: ImageDimensions = Field(..., description="Dimensions of first image")
    dimensions2: ImageDimensions = Field(..., description="Dimensions of second image") 
    same_dimensions: bool = Field(..., description="Whether images have same dimensions")
    size_difference: int = Field(..., description="Difference in file sizes (bytes)", ge=0)
    formats: Dict[str, str] = Field(..., description="Image formats")


class ComparisonResult(BaseModel):
    """Image comparison result."""
    similarity_score: float = Field(..., description="Similarity score (0-100)", ge=0, le=100)
    hash_distance: int = Field(..., description="Hamming distance between hashes", ge=0)
    likely_match: bool = Field(..., description="Whether images are likely the same")
    analysis: ComparisonAnalysis = Field(..., description="Detailed comparison analysis")


class SimilarImageQuery(BaseModel):
    """Query for finding similar images."""
    hash_value: str = Field(..., description="Perceptual hash to search for", min_length=1)
    threshold: int = Field(10, description="Maximum hash distance for matches", ge=0, le=64)


class SimilarImagesResult(BaseModel):
    """Result of similar image search."""
    query_hash: str = Field(..., description="Queried hash value")
    threshold: int = Field(..., description="Search threshold used")
    matches: List[Dict[str, Any]] = Field(default_factory=list, description="Matching images")
    message: str = Field(..., description="Status message")


class ReverseSearchResult(BaseModel):
    """Single reverse search result."""
    url: str = Field(..., description="URL of the found image")
    title: str = Field(..., description="Title or description")
    thumbnail: str = Field(..., description="Thumbnail URL")
    source: str = Field(..., description="Search engine source")


class SupportedFormatsInfo(BaseModel):
    """Information about supported formats and capabilities."""
    supported_formats: List[str] = Field(..., description="List of supported image formats")
    max_file_size_bytes: int = Field(..., description="Maximum file size in bytes", ge=0)
    max_file_size_mb: int = Field(..., description="Maximum file size in megabytes", ge=0)
    reverse_search_enabled: bool = Field(..., description="Whether reverse search is enabled")
    features: List[str] = Field(..., description="Available features")


class ErrorDetails(BaseModel):
    """Error details for media forensics operations."""
    operation: str = Field(..., description="Operation that failed")
    error_code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class VideoAnalysisRequest(BaseModel):
    """Options for the video analysis pipeline."""

    frame_interval: int = Field(5, ge=1, le=120, description="Process every n-th frame")
    min_area: int = Field(500, ge=50, le=50000, description="Minimum contour area")
    max_frames: int = Field(240, ge=1, le=2000, description="Maximum frames to analyse")


class BoundingBox(BaseModel):
    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)
    width: int = Field(..., ge=1)
    height: int = Field(..., ge=1)


class VideoObject(BaseModel):
    object_id: str = Field(..., description="Object identifier")
    label: str = Field(..., description="Detected label")
    confidence: float = Field(..., ge=0.0, le=1.0)
    bbox: BoundingBox = Field(..., description="Bounding box of the detection")


class VideoSceneResult(BaseModel):
    scene_id: str = Field(..., description="Scene identifier")
    frame_index: int = Field(..., ge=0)
    timestamp: float = Field(..., ge=0.0)
    objects: List[VideoObject] = Field(default_factory=list)


class VideoAnalysisSummary(BaseModel):
    total_frames: int = Field(..., ge=0)
    frames_processed: int = Field(..., ge=0)
    objects_detected: int = Field(..., ge=0)
    frame_interval: int = Field(..., ge=1)


class VideoAnalysisResponse(BaseModel):
    video_id: str = Field(..., description="Identifier of the processed video")
    filename: str = Field(..., description="Original filename")
    duration_seconds: float = Field(..., ge=0.0, description="Video duration")
    scenes: List[VideoSceneResult] = Field(default_factory=list)
    summary: VideoAnalysisSummary = Field(...)
    graph_entities: List[Dict[str, Any]] = Field(default_factory=list)
