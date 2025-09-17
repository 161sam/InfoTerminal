"""
Media Forensics module for InfoTerminal verification service.
Provides image analysis including EXIF extraction, perceptual hashing, and reverse image search.
"""

import hashlib
import io
import json
import os
import requests
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import imagehash
import cv2
import numpy as np
import aiohttp
import aiofiles
from pathlib import Path

class MediaForensics:
    """Handles media forensics analysis for images and videos."""
    
    def __init__(self):
        self.reverse_search_enabled = os.getenv("REVERSE_IMAGE_SEARCH", "0") == "1"
        self.bing_api_key = os.getenv("BING_SEARCH_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        self.google_cx_id = os.getenv("GOOGLE_CUSTOM_SEARCH_CX")
        
    async def analyze_image(self, image_data: bytes, filename: str = "image") -> Dict[str, Any]:
        """Comprehensive image analysis including EXIF, hashing, and forensics."""
        
        try:
            # Create PIL Image from bytes
            image = Image.open(io.BytesIO(image_data))
            
            # Perform all analysis
            analysis_results = {
                "filename": filename,
                "file_size": len(image_data),
                "format": image.format,
                "dimensions": {
                    "width": image.width,
                    "height": image.height
                },
                "mode": image.mode,
                "has_transparency": self._has_transparency(image),
                "exif_data": await self._extract_exif_data(image),
                "hashes": await self._compute_hashes(image, image_data),
                "forensics": await self._perform_forensics_analysis(image, image_data),
                "reverse_search": None  # Will be populated if enabled
            }
            
            # Perform reverse image search if enabled
            if self.reverse_search_enabled:
                analysis_results["reverse_search"] = await self._reverse_image_search(image_data)
            
            # Generate overall assessment
            analysis_results["assessment"] = self._generate_assessment(analysis_results)
            
            return analysis_results
            
        except Exception as e:
            return {
                "error": f"Image analysis failed: {str(e)}",
                "filename": filename,
                "file_size": len(image_data)
            }
    
    def _has_transparency(self, image: Image.Image) -> bool:
        """Check if image has transparency."""
        return (
            image.mode in ("RGBA", "LA") or 
            (image.mode == "P" and "transparency" in image.info)
        )
    
    async def _extract_exif_data(self, image: Image.Image) -> Dict[str, Any]:
        """Extract and parse EXIF metadata from image."""
        exif_data = {
            "has_exif": False,
            "camera_info": {},
            "settings": {},
            "location": {},
            "timestamps": {},
            "software": {},
            "raw_tags": {}
        }
        
        try:
            # Get raw EXIF data
            exif_dict = image.getexif()
            if not exif_dict:
                return exif_data
            
            exif_data["has_exif"] = True
            
            # Parse standard EXIF tags
            for tag_id, value in exif_dict.items():
                tag_name = TAGS.get(tag_id, tag_id)
                exif_data["raw_tags"][tag_name] = str(value)
                
                # Categorize important tags
                if tag_name in ["Make", "Model"]:
                    exif_data["camera_info"][tag_name.lower()] = value
                elif tag_name in ["DateTime", "DateTimeOriginal", "DateTimeDigitized"]:
                    try:
                        dt = datetime.strptime(str(value), "%Y:%m:%d %H:%M:%S")
                        exif_data["timestamps"][tag_name.lower()] = dt.isoformat()
                    except:
                        exif_data["timestamps"][tag_name.lower()] = str(value)
                elif tag_name in ["Software", "ProcessingSoftware"]:
                    exif_data["software"][tag_name.lower()] = value
                elif tag_name in ["FNumber", "ExposureTime", "ISOSpeedRatings", "FocalLength"]:
                    exif_data["settings"][tag_name.lower()] = value
            
            # Parse GPS information
            gps_info = exif_dict.get_ifd(0x8825)  # GPS IFD
            if gps_info:
                gps_data = {}
                for key, value in gps_info.items():
                    gps_tag = GPSTAGS.get(key, key)
                    gps_data[gps_tag] = value
                
                # Convert GPS coordinates if available
                if "GPSLatitude" in gps_data and "GPSLongitude" in gps_data:
                    lat = self._convert_gps_coordinate(
                        gps_data["GPSLatitude"], 
                        gps_data.get("GPSLatitudeRef", "N")
                    )
                    lon = self._convert_gps_coordinate(
                        gps_data["GPSLongitude"], 
                        gps_data.get("GPSLongitudeRef", "E")
                    )
                    exif_data["location"] = {
                        "latitude": lat,
                        "longitude": lon,
                        "altitude": gps_data.get("GPSAltitude"),
                        "timestamp": gps_data.get("GPSTimeStamp")
                    }
        
        except Exception as e:
            exif_data["error"] = f"EXIF extraction failed: {str(e)}"
        
        return exif_data
    
    def _convert_gps_coordinate(self, coordinate_tuple, reference):
        """Convert GPS coordinates from EXIF format to decimal degrees."""
        try:
            degrees, minutes, seconds = coordinate_tuple
            decimal = degrees + (minutes / 60) + (seconds / 3600)
            if reference in ["S", "W"]:
                decimal = -decimal
            return round(decimal, 6)
        except:
            return None
    
    async def _compute_hashes(self, image: Image.Image, image_data: bytes) -> Dict[str, str]:
        """Compute various hashes for image comparison and identification."""
        hashes = {}
        
        try:
            # File hash (MD5 and SHA256)
            hashes["md5"] = hashlib.md5(image_data).hexdigest()
            hashes["sha256"] = hashlib.sha256(image_data).hexdigest()
            
            # Perceptual hashes for similarity detection
            hashes["phash"] = str(imagehash.phash(image))
            hashes["dhash"] = str(imagehash.dhash(image))
            hashes["whash"] = str(imagehash.whash(image))
            hashes["average_hash"] = str(imagehash.average_hash(image))
            
            # Color histogram hash (custom implementation)
            hashes["color_hash"] = self._compute_color_hash(image)
            
        except Exception as e:
            hashes["error"] = f"Hash computation failed: {str(e)}"
        
        return hashes
    
    def _compute_color_hash(self, image: Image.Image) -> str:
        """Compute a hash based on color distribution."""
        try:
            # Convert to RGB if necessary
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            # Resize to standard size for consistent hashing
            image = image.resize((16, 16), Image.Resampling.LANCZOS)
            
            # Get color histogram
            hist = image.histogram()
            
            # Create hash from histogram bins
            hash_input = "".join([str(h) for h in hist[::8]])  # Sample every 8th bin
            return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
        
        except:
            return "unknown"
    
    async def _perform_forensics_analysis(self, image: Image.Image, image_data: bytes) -> Dict[str, Any]:
        """Perform forensic analysis to detect potential manipulation."""
        forensics = {
            "manipulation_indicators": [],
            "quality_analysis": {},
            "compression_analysis": {},
            "statistical_analysis": {}
        }
        
        try:
            # Convert to OpenCV format for analysis
            cv_image = self._pil_to_cv2(image)
            
            # Error Level Analysis (ELA) indicators
            ela_result = self._perform_ela_analysis(image_data)
            if ela_result["suspicious_areas"] > 0:
                forensics["manipulation_indicators"].append({
                    "type": "ELA_anomalies",
                    "confidence": ela_result["confidence"],
                    "details": f"Found {ela_result['suspicious_areas']} suspicious areas"
                })
            
            # JPEG compression analysis
            if image.format == "JPEG":
                compression_analysis = self._analyze_jpeg_compression(image_data)
                forensics["compression_analysis"] = compression_analysis
                
                # Check for re-compression indicators
                if compression_analysis.get("recompression_detected"):
                    forensics["manipulation_indicators"].append({
                        "type": "recompression",
                        "confidence": 0.7,
                        "details": "Multiple compression cycles detected"
                    })
            
            # Statistical analysis
            stats = self._compute_statistical_features(cv_image)
            forensics["statistical_analysis"] = stats
            
            # Check for statistical anomalies
            if stats.get("entropy") and stats["entropy"] < 6.0:
                forensics["manipulation_indicators"].append({
                    "type": "low_entropy",
                    "confidence": 0.6,
                    "details": f"Unusually low entropy: {stats['entropy']:.2f}"
                })
            
            # Noise analysis
            noise_level = self._analyze_noise_patterns(cv_image)
            forensics["quality_analysis"]["noise_level"] = noise_level
            
            if noise_level < 0.01:  # Very low noise might indicate heavy processing
                forensics["manipulation_indicators"].append({
                    "type": "artificial_smoothing",
                    "confidence": 0.5,
                    "details": "Unusually low noise levels detected"
                })
        
        except Exception as e:
            forensics["error"] = f"Forensics analysis failed: {str(e)}"
        
        return forensics
    
    def _pil_to_cv2(self, image: Image.Image):
        """Convert PIL Image to OpenCV format."""
        if image.mode != "RGB":
            image = image.convert("RGB")
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    def _perform_ela_analysis(self, image_data: bytes) -> Dict[str, Any]:
        """Perform Error Level Analysis to detect tampering."""
        try:
            # Create temporary files for ELA analysis
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_orig:
                temp_orig.write(image_data)
                temp_orig_path = temp_orig.name
            
            # Re-compress at different quality and compare
            image = Image.open(io.BytesIO(image_data))
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_recomp:
                image.save(temp_recomp.name, "JPEG", quality=90)
                temp_recomp_path = temp_recomp.name
            
            # Load both images and compute difference
            orig = cv2.imread(temp_orig_path)
            recomp = cv2.imread(temp_recomp_path)
            
            if orig is not None and recomp is not None:
                # Resize to match if needed
                if orig.shape != recomp.shape:
                    recomp = cv2.resize(recomp, (orig.shape[1], orig.shape[0]))
                
                # Compute absolute difference
                diff = cv2.absdiff(orig, recomp)
                
                # Analyze difference for suspicious areas
                gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                suspicious_pixels = np.sum(gray_diff > 15)  # Threshold for suspicious differences
                total_pixels = gray_diff.shape[0] * gray_diff.shape[1]
                
                suspicious_ratio = suspicious_pixels / total_pixels
                
                # Cleanup temp files
                os.unlink(temp_orig_path)
                os.unlink(temp_recomp_path)
                
                return {
                    "suspicious_areas": suspicious_pixels,
                    "suspicious_ratio": suspicious_ratio,
                    "confidence": min(suspicious_ratio * 2, 1.0)  # Scale to confidence
                }
        
        except Exception as e:
            return {"error": f"ELA analysis failed: {str(e)}", "suspicious_areas": 0}
        
        return {"suspicious_areas": 0, "confidence": 0.0}
    
    def _analyze_jpeg_compression(self, image_data: bytes) -> Dict[str, Any]:
        """Analyze JPEG compression characteristics."""
        analysis = {
            "quality_estimate": None,
            "quantization_tables": [],
            "recompression_detected": False
        }
        
        try:
            # Simple quality estimation based on file size vs dimensions
            image = Image.open(io.BytesIO(image_data))
            pixels = image.width * image.height
            bits_per_pixel = (len(image_data) * 8) / pixels
            
            # Rough quality estimation (very simplified)
            if bits_per_pixel > 8:
                analysis["quality_estimate"] = "high"
            elif bits_per_pixel > 4:
                analysis["quality_estimate"] = "medium"
            else:
                analysis["quality_estimate"] = "low"
            
            # Check for potential recompression indicators
            # (This is a simplified check - real implementation would be more complex)
            if bits_per_pixel < 2 and pixels > 100000:  # Large image with very low bpp
                analysis["recompression_detected"] = True
        
        except Exception as e:
            analysis["error"] = f"JPEG analysis failed: {str(e)}"
        
        return analysis
    
    def _compute_statistical_features(self, image) -> Dict[str, float]:
        """Compute statistical features of the image."""
        stats = {}
        
        try:
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Basic statistics
            stats["mean"] = float(np.mean(gray))
            stats["std"] = float(np.std(gray))
            stats["min"] = float(np.min(gray))
            stats["max"] = float(np.max(gray))
            
            # Entropy (measure of randomness)
            hist, _ = np.histogram(gray, bins=256, range=(0, 256))
            hist = hist / hist.sum()  # Normalize
            hist = hist[hist > 0]  # Remove zero probabilities
            entropy = -np.sum(hist * np.log2(hist))
            stats["entropy"] = float(entropy)
            
            # Contrast metrics
            stats["rms_contrast"] = float(np.std(gray))
            
        except Exception as e:
            stats["error"] = f"Statistical analysis failed: {str(e)}"
        
        return stats
    
    def _analyze_noise_patterns(self, image) -> float:
        """Analyze noise patterns in the image."""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply Laplacian filter to detect noise
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            noise_level = np.var(laplacian) / 10000  # Normalize
            
            return float(noise_level)
        
        except:
            return 0.0
    
    async def _reverse_image_search(self, image_data: bytes) -> Dict[str, Any]:
        """Perform reverse image search using available APIs."""
        results = {
            "enabled": True,
            "sources": [],
            "similar_images": [],
            "error": None
        }
        
        try:
            # Try Google reverse image search if API keys available
            if self.google_api_key and self.google_cx_id:
                google_results = await self._google_reverse_search(image_data)
                if google_results:
                    results["sources"].append("google")
                    results["similar_images"].extend(google_results)
            
            # Try Bing reverse image search if API key available
            if self.bing_api_key:
                bing_results = await self._bing_reverse_search(image_data)
                if bing_results:
                    results["sources"].append("bing")
                    results["similar_images"].extend(bing_results)
            
            # If no API keys available, return placeholder
            if not results["sources"]:
                results["error"] = "No reverse search APIs configured"
        
        except Exception as e:
            results["error"] = f"Reverse search failed: {str(e)}"
        
        return results
    
    async def _google_reverse_search(self, image_data: bytes) -> List[Dict[str, Any]]:
        """Perform reverse image search using Google Custom Search API."""
        # This would require implementing Google's reverse image search
        # For now, return placeholder
        return []
    
    async def _bing_reverse_search(self, image_data: bytes) -> List[Dict[str, Any]]:
        """Perform reverse image search using Bing Visual Search API."""
        if not self.bing_api_key:
            return []
        
        try:
            url = "https://api.bing.microsoft.com/v7.0/images/visualsearch"
            headers = {
                "Ocp-Apim-Subscription-Key": self.bing_api_key,
                "Content-Type": "multipart/form-data"
            }
            
            # Prepare multipart form data
            files = {"image": ("image.jpg", io.BytesIO(image_data), "image/jpeg")}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=files) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_bing_results(data)
            
        except Exception as e:
            print(f"Bing reverse search error: {e}")
        
        return []
    
    def _parse_bing_results(self, data: Dict) -> List[Dict[str, Any]]:
        """Parse Bing Visual Search API results."""
        results = []
        
        try:
            tags = data.get("tags", [])
            for tag in tags:
                actions = tag.get("actions", [])
                for action in actions:
                    if action.get("actionType") == "VisualSearch":
                        search_data = action.get("data", {})
                        value = search_data.get("value", [])
                        
                        for item in value[:5]:  # Limit to top 5 results
                            result = {
                                "source": "bing",
                                "title": item.get("name", ""),
                                "url": item.get("contentUrl", ""),
                                "thumbnail": item.get("thumbnailUrl", ""),
                                "size": item.get("contentSize", ""),
                                "similarity_score": 0.8  # Placeholder - Bing doesn't provide this
                            }
                            results.append(result)
        
        except Exception as e:
            print(f"Error parsing Bing results: {e}")
        
        return results
    
    def _generate_assessment(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall assessment of the image based on all analyses."""
        assessment = {
            "authenticity_score": 1.0,  # Start with assumption of authenticity
            "risk_factors": [],
            "recommendations": [],
            "summary": ""
        }
        
        try:
            # Check manipulation indicators
            manipulation_indicators = analysis.get("forensics", {}).get("manipulation_indicators", [])
            if manipulation_indicators:
                # Reduce authenticity score based on indicators
                confidence_sum = sum(indicator.get("confidence", 0) for indicator in manipulation_indicators)
                assessment["authenticity_score"] = max(0.1, 1.0 - (confidence_sum / 2))
                
                for indicator in manipulation_indicators:
                    assessment["risk_factors"].append({
                        "type": "manipulation",
                        "details": indicator.get("details", ""),
                        "confidence": indicator.get("confidence", 0)
                    })
            
            # Check EXIF data authenticity
            exif_data = analysis.get("exif_data", {})
            if not exif_data.get("has_exif"):
                assessment["risk_factors"].append({
                    "type": "missing_metadata",
                    "details": "No EXIF data found - may indicate processing or intentional removal",
                    "confidence": 0.3
                })
                assessment["authenticity_score"] *= 0.9
            
            # Check for software processing indicators
            software_info = exif_data.get("software", {})
            if software_info:
                for software_key, software_value in software_info.items():
                    if any(editor in str(software_value).lower() 
                           for editor in ["photoshop", "gimp", "paint.net", "canva"]):
                        assessment["risk_factors"].append({
                            "type": "editing_software",
                            "details": f"Edited with {software_value}",
                            "confidence": 0.4
                        })
                        assessment["authenticity_score"] *= 0.8
            
            # Check reverse search results
            reverse_search = analysis.get("reverse_search", {})
            if reverse_search and reverse_search.get("similar_images"):
                num_matches = len(reverse_search["similar_images"])
                if num_matches > 0:
                    assessment["risk_factors"].append({
                        "type": "found_elsewhere",
                        "details": f"Found {num_matches} similar images online",
                        "confidence": 0.6
                    })
                    # Don't reduce authenticity score as this might be legitimate sharing
            
            # Generate recommendations
            if assessment["authenticity_score"] < 0.7:
                assessment["recommendations"].append("Further forensic analysis recommended")
                assessment["recommendations"].append("Cross-reference with original source if possible")
            
            if not exif_data.get("has_exif"):
                assessment["recommendations"].append("Verify image provenance through alternative means")
            
            # Generate summary
            if assessment["authenticity_score"] > 0.8:
                assessment["summary"] = "Image appears authentic with minimal manipulation indicators"
            elif assessment["authenticity_score"] > 0.5:
                assessment["summary"] = "Image shows some manipulation indicators - moderate verification recommended"
            else:
                assessment["summary"] = "Image shows significant manipulation indicators - thorough verification required"
        
        except Exception as e:
            assessment["error"] = f"Assessment generation failed: {str(e)}"
        
        return assessment

# Global instance
media_forensics = MediaForensics()
