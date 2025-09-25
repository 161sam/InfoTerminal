"""
Verification v1 router for claim verification and fact-checking.
Provides claim extraction, evidence retrieval, stance classification, and credibility assessment.
"""

import os
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, status, BackgroundTasks, Query
from pydantic import BaseModel

# Import shared standards
import sys
from pathlib import Path
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

# Import models (use existing models and extend as needed)
try:
    from ..models.api_models import (
        ExtractClaimsRequest,
        ClaimResponse,
        FindEvidenceRequest,
        EvidenceResponse,
        ClassifyStanceRequest,
        StanceResponse,
        CredibilityRequest,
        CredibilityResponse,
        MediaAnalysisResponse,
    )
except ImportError:
    from models.api_models import (  # type: ignore
        ExtractClaimsRequest,
        ClaimResponse,
        FindEvidenceRequest,
        EvidenceResponse,
        ClassifyStanceRequest,
        StanceResponse,
        CredibilityRequest,
        CredibilityResponse,
        MediaAnalysisResponse,
    )

router = APIRouter(tags=["Verification"], prefix="/v1")

# Import service components
try:
    from ..service import VerificationService
    from ..claim_extractor import ClaimExtractor
    from ..stance_classifier import StanceClassifier
    from ..evidence_retrieval import EvidenceRetriever
    from ..media_forensics import MediaForensics
except ImportError:
    try:  # Fallback to absolute imports when package context is missing
        from service import VerificationService  # type: ignore
        from claim_extractor import ClaimExtractor  # type: ignore
        from stance_classifier import StanceClassifier  # type: ignore
        from evidence_retrieval import EvidenceRetriever  # type: ignore
        from media_forensics import MediaForensics  # type: ignore
    except ImportError:
        # Handle missing service components
        VerificationService = None
        ClaimExtractor = None
        StanceClassifier = None
        EvidenceRetriever = None
        MediaForensics = None


# Additional response models
class ImageSimilarityResponse(BaseModel):
    """Response for image similarity comparison."""
    similarity_score: float
    hash_distance: int
    likely_match: bool
    analysis: Dict[str, Any]


class VerificationStatsResponse(BaseModel):
    """Service statistics and performance metrics."""
    total_claims_processed: int
    total_evidence_retrieved: int
    total_images_analyzed: int
    uptime_seconds: float
    cache_hit_rate: Optional[float] = None


class BatchClaimsRequest(BaseModel):
    """Request for batch claim processing."""
    texts: List[str]
    confidence_threshold: float = 0.7
    max_claims_per_text: int = 5


class BatchClaimsResponse(BaseModel):
    """Response for batch claim processing."""
    results: List[Dict[str, Any]]
    total_texts: int
    total_claims: int
    processing_time_seconds: float


# Initialize service (singleton pattern)
_verification_service = None

def get_verification_service():
    """Get or create verification service instance."""
    global _verification_service
    if _verification_service is None and VerificationService is not None:
        _verification_service = VerificationService()
    return _verification_service


# API Endpoints
@router.post("/claims/extract", response_model=List[ClaimResponse])
async def extract_claims(
    request: ExtractClaimsRequest,
    background_tasks: BackgroundTasks
):
    """
    Extract verifiable claims from text.
    
    Analyzes text to identify factual claims that can be verified,
    including subject-predicate-object relationships and temporal/spatial context.
    """
    try:
        service = get_verification_service()
        if not service:
            raise_http_error("SERVICE_UNAVAILABLE", "Verification service not available")
        
        claims = await service.extract_claims(request, background_tasks)
        return claims
        
    except Exception as e:
        raise_http_error("CLAIM_EXTRACTION_FAILED", f"Failed to extract claims: {str(e)}")


@router.post("/claims/batch", response_model=BatchClaimsResponse)
async def extract_claims_batch(
    request: BatchClaimsRequest,
    background_tasks: BackgroundTasks
):
    """
    Extract claims from multiple texts in batch.
    
    Efficiently processes multiple documents for claim extraction.
    """
    try:
        import time
        start_time = time.time()
        
        service = get_verification_service()
        if not service:
            raise_http_error("SERVICE_UNAVAILABLE", "Verification service not available")
        
        results = []
        total_claims = 0
        
        for i, text in enumerate(request.texts):
            try:
                claims_request = ExtractClaimsRequest(
                    text=text,
                    confidence_threshold=request.confidence_threshold,
                    max_claims=request.max_claims_per_text
                )
                claims = await service.extract_claims(claims_request, background_tasks)
                results.append({
                    "text_index": i,
                    "claims": [claim.dict() for claim in claims],
                    "status": "success"
                })
                total_claims += len(claims)
                
            except Exception as e:
                results.append({
                    "text_index": i,
                    "error": str(e),
                    "status": "failed"
                })
        
        processing_time = time.time() - start_time
        
        return BatchClaimsResponse(
            results=results,
            total_texts=len(request.texts),
            total_claims=total_claims,
            processing_time_seconds=round(processing_time, 3)
        )
        
    except Exception as e:
        raise_http_error("BATCH_EXTRACTION_FAILED", f"Batch claim extraction failed: {str(e)}")


@router.post("/evidence/find", response_model=List[EvidenceResponse])
async def find_evidence(request: FindEvidenceRequest):
    """
    Find evidence for a claim from multiple sources.
    
    Searches web, news, and reference sources for supporting or contradicting evidence.
    """
    try:
        service = get_verification_service()
        if not service:
            raise_http_error("SERVICE_UNAVAILABLE", "Verification service not available")
        
        evidence = await service.find_evidence(request)
        return evidence
        
    except Exception as e:
        raise_http_error("EVIDENCE_SEARCH_FAILED", f"Evidence search failed: {str(e)}")


@router.post("/stance/classify", response_model=StanceResponse)
async def classify_stance(request: ClassifyStanceRequest):
    """
    Classify stance between a claim and evidence.
    
    Determines if evidence supports, contradicts, or is neutral toward a claim.
    """
    try:
        service = get_verification_service()
        if not service:
            raise_http_error("SERVICE_UNAVAILABLE", "Verification service not available")
        
        stance = await service.classify_stance(request)
        return stance
        
    except Exception as e:
        raise_http_error("STANCE_CLASSIFICATION_FAILED", f"Stance classification failed: {str(e)}")


@router.post("/credibility/assess", response_model=CredibilityResponse)
async def assess_credibility(request: CredibilityRequest):
    """
    Assess the credibility of a source.
    
    Evaluates source reliability, bias, and factual reporting quality.
    """
    try:
        service = get_verification_service()
        if not service:
            raise_http_error("SERVICE_UNAVAILABLE", "Verification service not available")
        
        credibility = await service.assess_credibility(request)
        return credibility
        
    except Exception as e:
        raise_http_error("CREDIBILITY_ASSESSMENT_FAILED", f"Credibility assessment failed: {str(e)}")


@router.post("/media/analyze", response_model=MediaAnalysisResponse)
async def analyze_media(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Media file to analyze")
):
    """
    Analyze media for forensic information.
    
    Extracts metadata, performs integrity checks, and detects potential manipulation.
    """
    try:
        service = get_verification_service()
        if not service:
            raise_http_error("SERVICE_UNAVAILABLE", "Verification service not available")
        
        # Validate file
        if not file.filename:
            raise_http_error("NO_FILENAME", "No filename provided")
        
        max_size = 50 * 1024 * 1024  # 50MB
        content = await file.read()
        if len(content) > max_size:
            raise_http_error("FILE_TOO_LARGE", f"File too large. Maximum size: {max_size} bytes")
        
        # Reset file pointer for service processing
        await file.seek(0)
        
        analysis = await service.analyze_image(file, background_tasks)
        return analysis
        
    except Exception as e:
        raise_http_error("MEDIA_ANALYSIS_FAILED", f"Media analysis failed: {str(e)}")


@router.post("/media/compare", response_model=ImageSimilarityResponse)
async def compare_media(
    file1: UploadFile = File(..., description="First media file"),
    file2: UploadFile = File(..., description="Second media file")
):
    """
    Compare two media files for similarity.
    
    Uses perceptual hashing to detect duplicate or manipulated content.
    """
    try:
        service = get_verification_service()
        if not service:
            raise_http_error("SERVICE_UNAVAILABLE", "Verification service not available")
        
        # Validate files
        max_size = 50 * 1024 * 1024  # 50MB
        for file in [file1, file2]:
            if not file.filename:
                raise_http_error("NO_FILENAME", f"No filename provided for {file}")
            
            content = await file.read()
            if len(content) > max_size:
                raise_http_error("FILE_TOO_LARGE", f"File {file.filename} too large")
            await file.seek(0)  # Reset for processing
        
        comparison = await service.compare_images(file1, file2)
        return comparison
        
    except Exception as e:
        raise_http_error("MEDIA_COMPARISON_FAILED", f"Media comparison failed: {str(e)}")


@router.get("/stats", response_model=VerificationStatsResponse)
def get_stats():
    """
    Get verification service statistics.
    
    Returns performance metrics and processing counts.
    """
    try:
        service = get_verification_service()
        if not service:
            raise_http_error("SERVICE_UNAVAILABLE", "Verification service not available")
        
        return service.stats()
        
    except Exception as e:
        raise_http_error("STATS_FAILED", f"Failed to get statistics: {str(e)}")


@router.post("/pipeline/verify", response_model=Dict[str, Any])
async def verification_pipeline(
    text: str = Query(..., description="Text to verify"),
    include_evidence: bool = Query(True, description="Include evidence search"),
    include_credibility: bool = Query(True, description="Include credibility assessment"),
    max_claims: int = Query(5, ge=1, le=20, description="Maximum claims to extract"),
    max_evidence: int = Query(3, ge=1, le=10, description="Maximum evidence per claim")
):
    """
    Complete verification pipeline for text.
    
    Extracts claims, finds evidence, classifies stance, and assesses credibility in one call.
    """
    try:
        service = get_verification_service()
        if not service:
            raise_http_error("SERVICE_UNAVAILABLE", "Verification service not available")
        
        # Extract claims
        claims_request = ExtractClaimsRequest(
            text=text,
            max_claims=max_claims
        )
        claims = await service.extract_claims(claims_request, BackgroundTasks())
        
        results = {
            "original_text": text,
            "claims": [],
            "processing_summary": {
                "total_claims": len(claims),
                "total_evidence": 0,
                "total_assessments": 0
            }
        }
        
        # Process each claim
        for claim in claims:
            claim_result = {
                "claim": claim.dict(),
                "evidence": [],
                "stance_classifications": [],
                "credibility_assessments": []
            }
            
            if include_evidence:
                # Find evidence
                evidence_request = FindEvidenceRequest(
                    claim=claim.text,
                    max_sources=max_evidence
                )
                evidence = await service.find_evidence(evidence_request)
                claim_result["evidence"] = [e.dict() for e in evidence]
                results["processing_summary"]["total_evidence"] += len(evidence)
                
                # Classify stance for each evidence
                for evidence_item in evidence:
                    stance_request = ClassifyStanceRequest(
                        claim=claim.text,
                        evidence=evidence_item.snippet
                    )
                    stance = await service.classify_stance(stance_request)
                    claim_result["stance_classifications"].append(stance.dict())
                    
                    # Assess credibility if requested
                    if include_credibility:
                        cred_request = CredibilityRequest(source_url=evidence_item.source_url)
                        credibility = await service.assess_credibility(cred_request)
                        claim_result["credibility_assessments"].append(credibility.dict())
                        results["processing_summary"]["total_assessments"] += 1
            
            results["claims"].append(claim_result)
        
        return results
        
    except Exception as e:
        raise_http_error("PIPELINE_FAILED", f"Verification pipeline failed: {str(e)}")


@router.get("/sources", response_model=Dict[str, Any])
def get_available_sources():
    """
    Get available evidence sources and their status.
    
    Returns information about configured search engines and databases.
    """
    return {
        "sources": [
            {
                "name": "web_search", 
                "type": "search_engine",
                "status": "available",
                "description": "General web search"
            },
            {
                "name": "wikipedia",
                "type": "encyclopedia", 
                "status": "available",
                "description": "Wikipedia articles"
            },
            {
                "name": "news_sources",
                "type": "news",
                "status": "available", 
                "description": "News articles and reports"
            },
            {
                "name": "academic",
                "type": "scholarly",
                "status": "optional",
                "description": "Academic papers and journals"
            }
        ],
        "total_sources": 4,
        "message": "Source availability may vary based on configuration and API keys"
    }
