"""
Media Forensics v1 router for image and video analysis.
Provides EXIF extraction, perceptual hashing, forensic analysis, and comparison.
"""

import hashlib
import json
import os
import tempfile
from typing import Dict, Any, Optional, List
from pathlib import Path

import imagehash
import requests
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
from fastapi import APIRouter, UploadFile, File, HTTPException, status, BackgroundTasks, Query
from pydantic import BaseModel

# Import shared standards
import sys
SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parent.parent
for p in (SERVICE_DIR, REPO_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

try:
    from _shared.api_standards.error_schemas import raise_http_error
    from _shared.api_standards.pagination import PaginatedResponse
except ImportError:
    # Fallback for legacy compatibility
    def raise_http_error(code: str, message: str, details: Optional[Dict] = None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                          detail={"error": {"code": code, "message": message, "details": details or {}}})
    
    class PaginatedResponse(BaseModel):
        items: list
        total: int
        page: int = 1
        size: int = 10

# Import models
from ..models import (
    ImageAnalysisResult,
    ComparisonResult,
    SimilarImagesResult,
    SupportedFormatsInfo,
    ImageDimensions,
    PerceptualHashes,
    ForensicAnalysis,
    ComparisonAnalysis,
    ReverseSearchResult
)

router = APIRouter(tags=["Media Forensics"], prefix="/v1")

# Configuration
MAX_FILE_SIZE = int(os.getenv("MEDIA_MAX_FILE_SIZE", 50 * 1024 * 1024))  # 50MB
SUPPORTED_IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
REVERSE_SEARCH_ENABLED = os.getenv("REVERSE_SEARCH_ENABLED", "0") == "1"
BING_SEARCH_API_KEY = os.getenv("BING_SEARCH_API_KEY")


def extract_exif_data(image: Image.Image) -> Dict[str, Any]:
    """Extract EXIF metadata from an image."""
    exif_data = {}
    
    try:
        exif = image.getexif()
        if exif:
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                
                # Handle special EXIF values
                if isinstance(value, bytes):
                    try:
                        value = value.decode('utf-8', errors='ignore')
                    except:
                        value = str(value)
                elif isinstance(value, tuple):
                    value = list(value)
                
                exif_data[str(tag)] = value
    except Exception as e:
        exif_data["extraction_error"] = str(e)
    
    return exif_data


def calculate_perceptual_hash(image: Image.Image) -> PerceptualHashes:
    """Calculate perceptual hash for similarity detection."""
    try:
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Calculate different types of hashes
        phash = imagehash.phash(image)
        dhash = imagehash.dhash(image)
        whash = imagehash.whash(image)
        
        return PerceptualHashes(
            phash=str(phash),
            dhash=str(dhash),
            whash=str(whash)
        )
    except Exception as e:
        # Fallback hash data
        return PerceptualHashes(
            phash=f"error_{str(e)[:16]}",
            dhash=f"error_{str(e)[:16]}",
            whash=f"error_{str(e)[:16]}"
        )


def forensic_analysis(image: Image.Image, image_data: bytes) -> ForensicAnalysis:
    """Perform basic forensic analysis on the image."""
    try:
        # File hashes
        md5_hash = hashlib.md5(image_data).hexdigest()
        sha256_hash = hashlib.sha256(image_data).hexdigest()
        
        # Basic image analysis
        color_depth = len(image.getbands())
        has_transparency = image.mode in ("RGBA", "LA") or "transparency" in image.info
        
        # Compression quality estimation (for JPEG)
        estimated_jpeg_quality = None
        if image.format == "JPEG":
            # Simple quality estimation based on file size vs dimensions
            expected_size = image.width * image.height * 3  # 3 bytes per pixel for RGB
            compression_ratio = len(image_data) / expected_size
            estimated_jpeg_quality = min(100, int(compression_ratio * 200))
        
        # Check for common manipulation signs
        potential_manipulation_signs = []
        
        # Unusual EXIF data patterns
        exif = image.getexif()
        if exif:
            software = exif.get(305, "")  # Software tag
            if any(editor in str(software).lower() for editor in ["photoshop", "gimp", "paint"]):
                potential_manipulation_signs.append("Image editor in EXIF")
        
        # Size inconsistencies  
        if hasattr(image, '_getexif') and image._getexif():
            exif_dict = image._getexif()
            if exif_dict and 40962 in exif_dict and 40963 in exif_dict:  # PixelXDimension, PixelYDimension
                exif_width = exif_dict[40962]
                exif_height = exif_dict[40963]
                if exif_width != image.width or exif_height != image.height:
                    potential_manipulation_signs.append("EXIF dimensions mismatch")
        
        return ForensicAnalysis(
            md5_hash=md5_hash,
            sha256_hash=sha256_hash,
            color_depth=color_depth,
            has_transparency=has_transparency,
            estimated_jpeg_quality=estimated_jpeg_quality,
            potential_manipulation_signs=potential_manipulation_signs
        )
        
    except Exception as e:
        raise_http_error("FORENSIC_ANALYSIS_FAILED", f"Forensic analysis failed: {str(e)}")


async def reverse_image_search(image_data: bytes) -> List[ReverseSearchResult]:
    """Perform reverse image search using Bing Visual Search API."""
    if not REVERSE_SEARCH_ENABLED or not BING_SEARCH_API_KEY:
        return []
    
    try:
        # Bing Visual Search API
        search_url = "https://api.bing.microsoft.com/v7.0/images/visualsearch"
        headers = {
            "Ocp-Apim-Subscription-Key": BING_SEARCH_API_KEY,
        }
        
        files = {"image": ("image.jpg", image_data, "image/jpeg")}
        
        response = requests.post(search_url, headers=headers, files=files, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        # Extract relevant search results
        search_results = []
        if "tags" in result:
            for tag in result["tags"][:5]:  # Limit results
                if "actions" in tag:
                    for action in tag["actions"]:
                        if action.get("actionType") == "VisualSearch":
                            data = action.get("data", {})
                            if "value" in data:
                                for item in data["value"][:3]:  # Top 3 per tag
                                    search_results.append(ReverseSearchResult(
                                        url=item.get("hostPageUrl", ""),
                                        title=item.get("name", ""),
                                        thumbnail=item.get("thumbnailUrl", ""),
                                        source="bing_visual_search"
                                    ))
        
        return search_results[:10]  # Maximum 10 results
        
    except Exception as e:
        return [ReverseSearchResult(
            url="",
            title=f"Search failed: {str(e)}",
            thumbnail="",
            source="error"
        )]


# API Endpoints
@router.post("/images/analyze", response_model=ImageAnalysisResult)
async def analyze_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    include_reverse_search: bool = Query(False, description="Include reverse image search results")
):
    """
    Analyze an uploaded image for forensic information.
    
    Extracts:
    - EXIF metadata
    - Perceptual hashes for similarity detection
    - Basic forensic analysis
    - Optional reverse image search
    """
    
    # Validate file
    if not file.filename:
        raise_http_error("NO_FILENAME", "No filename provided")
    
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in SUPPORTED_IMAGE_FORMATS:
        raise_http_error("UNSUPPORTED_FORMAT", 
                        f"Unsupported format {file_ext}. Supported: {list(SUPPORTED_IMAGE_FORMATS)}")
    
    # Read file data
    try:
        image_data = await file.read()
    except Exception as e:
        raise_http_error("FILE_READ_ERROR", f"Failed to read uploaded file: {str(e)}")
    
    if len(image_data) > MAX_FILE_SIZE:
        raise_http_error("FILE_TOO_LARGE", 
                        f"File too large. Max size: {MAX_FILE_SIZE} bytes ({MAX_FILE_SIZE // (1024*1024)} MB)")
    
    try:
        # Load image
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(image_data)
            tmp.flush()
            
            with Image.open(tmp.name) as image:
                # Extract information
                exif_data = extract_exif_data(image)
                perceptual_hash = calculate_perceptual_hash(image)
                forensic_data = forensic_analysis(image, image_data)
                
                result = ImageAnalysisResult(
                    filename=file.filename,
                    file_size=len(image_data),
                    image_format=image.format or "unknown",
                    dimensions=ImageDimensions(width=image.width, height=image.height),
                    exif_data=exif_data,
                    perceptual_hash=perceptual_hash,
                    forensic_analysis=forensic_data
                )
                
                # Add reverse search if requested
                if include_reverse_search and REVERSE_SEARCH_ENABLED:
                    search_results = await reverse_image_search(image_data)
                    result.reverse_search_results = [res.dict() for res in search_results]
                
                return result
        
    except Exception as e:
        raise_http_error("IMAGE_ANALYSIS_FAILED", f"Image analysis failed: {str(e)}")


@router.post("/images/compare", response_model=ComparisonResult)
async def compare_images(
    file1: UploadFile = File(..., description="First image to compare"),
    file2: UploadFile = File(..., description="Second image to compare")
):
    """
    Compare two images for similarity using perceptual hashing.
    
    Returns similarity score and detailed analysis.
    """
    
    try:
        # Read both files
        data1 = await file1.read()
        data2 = await file2.read()
        
        # Validate sizes
        if len(data1) > MAX_FILE_SIZE or len(data2) > MAX_FILE_SIZE:
            raise_http_error("FILE_TOO_LARGE", f"One or both files exceed max size: {MAX_FILE_SIZE} bytes")
        
        # Process images
        with tempfile.NamedTemporaryFile() as tmp1, tempfile.NamedTemporaryFile() as tmp2:
            tmp1.write(data1)
            tmp1.flush()
            tmp2.write(data2) 
            tmp2.flush()
            
            with Image.open(tmp1.name) as img1, Image.open(tmp2.name) as img2:
                # Calculate hashes
                hash1 = imagehash.phash(img1)
                hash2 = imagehash.phash(img2)
                
                # Calculate distance
                hash_distance = hash1 - hash2
                
                # Calculate similarity score (0-100)
                max_distance = 64  # Maximum possible distance for pHash
                similarity_score = max(0, (max_distance - hash_distance) / max_distance * 100)
                
                # Determine if likely match
                likely_match = hash_distance <= 10  # Threshold for similar images
                
                analysis = ComparisonAnalysis(
                    hash1=str(hash1),
                    hash2=str(hash2),
                    dimensions1=ImageDimensions(width=img1.width, height=img1.height),
                    dimensions2=ImageDimensions(width=img2.width, height=img2.height),
                    same_dimensions=(img1.width == img2.width and img1.height == img2.height),
                    size_difference=abs(len(data1) - len(data2)),
                    formats={"image1": img1.format or "unknown", "image2": img2.format or "unknown"}
                )
                
                return ComparisonResult(
                    similarity_score=round(similarity_score, 2),
                    hash_distance=hash_distance,
                    likely_match=likely_match,
                    analysis=analysis
                )
        
    except Exception as e:
        raise_http_error("IMAGE_COMPARISON_FAILED", f"Image comparison failed: {str(e)}")


@router.get("/images/similar/{hash_value}", response_model=SimilarImagesResult)
def find_similar_images(
    hash_value: str,
    threshold: int = Query(10, description="Maximum hash distance for matches", ge=0, le=64)
):
    """
    Find similar images by perceptual hash.
    
    This is a placeholder for database integration.
    """
    # This would integrate with a database of known images
    return SimilarImagesResult(
        query_hash=hash_value,
        threshold=threshold,
        matches=[],
        message="Image database integration not yet implemented. Consider integrating with vector database."
    )


@router.get("/formats", response_model=SupportedFormatsInfo)
def get_supported_formats():
    """
    Get supported image formats and service capabilities.
    """
    return SupportedFormatsInfo(
        supported_formats=list(SUPPORTED_IMAGE_FORMATS),
        max_file_size_bytes=MAX_FILE_SIZE,
        max_file_size_mb=MAX_FILE_SIZE // (1024 * 1024),
        reverse_search_enabled=REVERSE_SEARCH_ENABLED,
        features=[
            "EXIF metadata extraction",
            "Perceptual hashing (pHash, dHash, wHash)",
            "Basic forensic analysis",
            "Image comparison with similarity scoring",
            "Reverse image search (if configured)",
            "Manipulation detection indicators"
        ]
    )


@router.post("/images/batch/analyze", response_model=PaginatedResponse)
async def batch_analyze_images(
    files: List[UploadFile] = File(..., description="Multiple images to analyze"),
    include_reverse_search: bool = Query(False, description="Include reverse search for all images")
):
    """
    Analyze multiple images in batch.
    
    Returns paginated results with analysis for each image.
    """
    if len(files) > 10:  # Limit batch size
        raise_http_error("BATCH_TOO_LARGE", "Maximum 10 images per batch request")
    
    results = []
    
    for file in files:
        try:
            # Reuse single image analysis logic
            result = await analyze_image(
                background_tasks=BackgroundTasks(),
                file=file,
                include_reverse_search=include_reverse_search
            )
            results.append(result.dict())
            
        except HTTPException as e:
            # Include failed analysis in results
            results.append({
                "filename": file.filename or "unknown",
                "error": e.detail,
                "status": "failed"
            })
        except Exception as e:
            results.append({
                "filename": file.filename or "unknown", 
                "error": str(e),
                "status": "failed"
            })
    
    return PaginatedResponse(
        items=results,
        total=len(results),
        page=1,
        size=len(results)
    )


@router.get("/images/{sha256}/metadata")
def get_image_metadata(sha256: str):
    """
    Get cached metadata for an image by SHA256 hash.
    
    This is a placeholder for metadata caching integration.
    """
    return {
        "sha256": sha256,
        "cached_metadata": None,
        "message": "Metadata caching not yet implemented. Consider integrating with Redis/database cache."
    }
