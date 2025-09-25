# Media Forensics Service for InfoTerminal
# Provides image analysis, EXIF extraction, and forensic capabilities

import hashlib
import json
import os
import tempfile
from typing import Dict, List, Optional, Any
from pathlib import Path

import imagehash
import requests
from PIL import Image
from PIL.ExifTags import TAGS
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import numpy as np

# Import shared modules
import sys
SERVICE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_DIR.parent.parent
for p in (SERVICE_DIR, REPO_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

try:
    from _shared.cors import apply_cors, get_cors_settings_from_env
    from _shared.health import make_healthz, make_readyz
    from common.request_id import RequestIdMiddleware
    from _shared.obs.metrics_boot import enable_prometheus_metrics
    from _shared.obs.otel_boot import setup_otel
except ImportError:
    # Fallback for development
    def apply_cors(app, settings): pass
    def get_cors_settings_from_env(): return {}
    def make_healthz(name, version, ts): return {"status": "ok"}
    def make_readyz(name, version, ts, checks): return {"status": "ready"}, 200
    def setup_otel(app, service_name, version): pass
    def enable_prometheus_metrics(app, **kwargs): pass
    from starlette.middleware.base import BaseHTTPMiddleware

    class RequestIdMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            return await call_next(request)


app = FastAPI(
    title="InfoTerminal Media Forensics Service",
    description="Image and video analysis for OSINT investigations",
    version="0.1.0"
)

# Setup middleware and observability
try:
    apply_cors(app, get_cors_settings_from_env())
    app.add_middleware(RequestIdMiddleware)
    setup_otel(app, service_name="media-forensics", version="0.1.0")
    
    enable_prometheus_metrics(
        app,
        service_name="media-forensics",
        service_version="0.1.0",
    )
except:
    pass  # Skip middleware setup if shared modules not available


# Configuration
MAX_FILE_SIZE = int(os.getenv("MEDIA_MAX_FILE_SIZE", 50 * 1024 * 1024))  # 50MB
SUPPORTED_IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
REVERSE_SEARCH_ENABLED = os.getenv("REVERSE_SEARCH_ENABLED", "0") == "1"
BING_SEARCH_API_KEY = os.getenv("BING_SEARCH_API_KEY")


class ImageAnalysisResult(BaseModel):
    filename: str
    file_size: int
    image_format: str
    dimensions: Dict[str, int]
    exif_data: Dict[str, Any]
    perceptual_hash: str
    forensic_analysis: Dict[str, Any]
    reverse_search_results: Optional[List[Dict[str, Any]]] = None


class ComparisonResult(BaseModel):
    similarity_score: float
    hash_distance: int
    likely_match: bool
    analysis: Dict[str, Any]


@app.get("/healthz")
def healthz():
    return make_healthz("media-forensics", "0.1.0", 0)


@app.get("/readyz")
def readyz():
    checks = {}
    return JSONResponse(*make_readyz("media-forensics", "0.1.0", 0, checks))


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


def calculate_perceptual_hash(image: Image.Image) -> str:
    """Calculate perceptual hash for similarity detection."""
    try:
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Calculate different types of hashes
        phash = imagehash.phash(image)
        dhash = imagehash.dhash(image)
        whash = imagehash.whash(image)
        
        return {
            "phash": str(phash),
            "dhash": str(dhash),
            "whash": str(whash)
        }
    except Exception as e:
        return {"error": str(e)}


def forensic_analysis(image: Image.Image, image_data: bytes) -> Dict[str, Any]:
    """Perform basic forensic analysis on the image."""
    analysis = {}
    
    try:
        # File hash
        analysis["md5_hash"] = hashlib.md5(image_data).hexdigest()
        analysis["sha256_hash"] = hashlib.sha256(image_data).hexdigest()
        
        # Basic image analysis
        analysis["color_depth"] = len(image.getbands())
        analysis["has_transparency"] = image.mode in ("RGBA", "LA") or "transparency" in image.info
        
        # Compression quality estimation (for JPEG)
        if image.format == "JPEG":
            # Simple quality estimation based on file size vs dimensions
            expected_size = image.width * image.height * 3  # 3 bytes per pixel for RGB
            compression_ratio = len(image_data) / expected_size
            analysis["estimated_jpeg_quality"] = min(100, int(compression_ratio * 200))
        
        # Check for common manipulation signs
        analysis["potential_manipulation_signs"] = []
        
        # Unusual EXIF data patterns
        exif = image.getexif()
        if exif:
            software = exif.get(305, "")  # Software tag
            if any(editor in software.lower() for editor in ["photoshop", "gimp", "paint"]):
                analysis["potential_manipulation_signs"].append("Image editor in EXIF")
        
        # Size inconsistencies  
        if hasattr(image, '_getexif') and image._getexif():
            exif_dict = image._getexif()
            if exif_dict and 40962 in exif_dict and 40963 in exif_dict:  # PixelXDimension, PixelYDimension
                exif_width = exif_dict[40962]
                exif_height = exif_dict[40963]
                if exif_width != image.width or exif_height != image.height:
                    analysis["potential_manipulation_signs"].append("EXIF dimensions mismatch")
        
    except Exception as e:
        analysis["analysis_error"] = str(e)
    
    return analysis


async def reverse_image_search(image_data: bytes) -> List[Dict[str, Any]]:
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
                                    search_results.append({
                                        "url": item.get("hostPageUrl", ""),
                                        "title": item.get("name", ""),
                                        "thumbnail": item.get("thumbnailUrl", ""),
                                        "source": "bing_visual_search"
                                    })
        
        return search_results[:10]  # Maximum 10 results
        
    except Exception as e:
        return [{"error": f"Reverse search failed: {str(e)}"}]


@app.post("/image/analyze", response_model=ImageAnalysisResult)
async def analyze_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    include_reverse_search: bool = False
):
    """Analyze an uploaded image for forensic information."""
    
    # Validate file
    if not file.filename:
        raise HTTPException(400, "No filename provided")
    
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in SUPPORTED_IMAGE_FORMATS:
        raise HTTPException(400, f"Unsupported format. Supported: {SUPPORTED_IMAGE_FORMATS}")
    
    # Read file data
    image_data = await file.read()
    
    if len(image_data) > MAX_FILE_SIZE:
        raise HTTPException(413, f"File too large. Max size: {MAX_FILE_SIZE} bytes")
    
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
                    image_format=image.format,
                    dimensions={"width": image.width, "height": image.height},
                    exif_data=exif_data,
                    perceptual_hash=perceptual_hash,
                    forensic_analysis=forensic_data
                )
                
                # Add reverse search if requested
                if include_reverse_search and REVERSE_SEARCH_ENABLED:
                    search_results = await reverse_image_search(image_data)
                    result.reverse_search_results = search_results
                
                return result
        
    except Exception as e:
        raise HTTPException(500, f"Image analysis failed: {str(e)}")


@app.post("/image/compare", response_model=ComparisonResult)
async def compare_images(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    """Compare two images for similarity."""
    
    try:
        # Read both files
        data1 = await file1.read()
        data2 = await file2.read()
        
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
                
                analysis = {
                    "hash1": str(hash1),
                    "hash2": str(hash2),
                    "dimensions1": {"width": img1.width, "height": img1.height},
                    "dimensions2": {"width": img2.width, "height": img2.height},
                    "same_dimensions": (img1.width == img2.width and img1.height == img2.height),
                    "size_difference": abs(len(data1) - len(data2)),
                    "formats": {"image1": img1.format, "image2": img2.format}
                }
                
                return ComparisonResult(
                    similarity_score=round(similarity_score, 2),
                    hash_distance=hash_distance,
                    likely_match=likely_match,
                    analysis=analysis
                )
        
    except Exception as e:
        raise HTTPException(500, f"Image comparison failed: {str(e)}")


@app.get("/image/hash/{hash_value}")
def find_similar_images(hash_value: str, threshold: int = 10):
    """Find similar images by perceptual hash (placeholder for database integration)."""
    # This would integrate with a database of known images
    return {
        "query_hash": hash_value,
        "threshold": threshold,
        "matches": [],
        "message": "Image database integration not yet implemented"
    }


@app.get("/formats")
def supported_formats():
    """Get supported image formats and limits."""
    return {
        "supported_formats": list(SUPPORTED_IMAGE_FORMATS),
        "max_file_size_bytes": MAX_FILE_SIZE,
        "max_file_size_mb": MAX_FILE_SIZE // (1024 * 1024),
        "reverse_search_enabled": REVERSE_SEARCH_ENABLED,
        "features": [
            "EXIF metadata extraction",
            "Perceptual hashing",
            "Basic forensic analysis",
            "Image comparison",
            "Reverse image search (if enabled)"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
