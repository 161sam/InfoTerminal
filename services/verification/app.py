"""
InfoTerminal Verification Service
Provides claim extraction, evidence retrieval, and stance classification.
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
import logging

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import structlog

from claim_extractor import ClaimExtractor
from evidence_retrieval import EvidenceRetriever
from stance_classifier import StanceClassifier

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer()
    ],
    logger_factory=structlog.WriteLoggerFactory(),
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

app = FastAPI(
    title="InfoTerminal Verification Service",
    description="Claim extraction, evidence retrieval, and fact-checking",
    version="0.2.0"
)

# Global instances
claim_extractor = None
evidence_retriever = None
stance_classifier = None

class ExtractClaimsRequest(BaseModel):
    text: str
    confidence_threshold: float = 0.7
    max_claims: int = 10

class ClaimResponse(BaseModel):
    id: str
    text: str
    confidence: float
    claim_type: str
    subject: str
    predicate: str
    object: str
    temporal: Optional[str] = None
    location: Optional[str] = None

class FindEvidenceRequest(BaseModel):
    claim: str
    max_sources: int = 5
    source_types: List[str] = ["web", "wikipedia", "news"]
    language: str = "en"

class EvidenceResponse(BaseModel):
    id: str
    source_url: str
    source_title: str
    source_type: str
    snippet: str
    relevance_score: float
    credibility_score: float
    publication_date: Optional[str] = None
    author: Optional[str] = None

class ClassifyStanceRequest(BaseModel):
    claim: str
    evidence: str
    context: Optional[str] = None

class StanceResponse(BaseModel):
    stance: str  # "support", "contradict", "neutral", "unrelated"
    confidence: float
    reasoning: str
    key_phrases: List[str]

class CredibilityRequest(BaseModel):
    source_url: str
    domain: Optional[str] = None

class CredibilityResponse(BaseModel):
    credibility_score: float
    bias_rating: str
    factual_reporting: str
    transparency_score: float
    authority_indicators: List[str]
    red_flags: List[str]

@app.on_event("startup")
async def startup_event():
    """Initialize verification components on startup."""
    global claim_extractor, evidence_retriever, stance_classifier
    
    logger.info("Starting InfoTerminal Verification Service")
    
    # Initialize claim extractor
    claim_extractor = ClaimExtractor()
    await claim_extractor.initialize()
    
    # Initialize evidence retriever
    evidence_retriever = EvidenceRetriever()
    await evidence_retriever.initialize()
    
    # Initialize stance classifier
    stance_classifier = StanceClassifier()
    await stance_classifier.initialize()
    
    logger.info("Verification Service started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Verification Service")
    
    if claim_extractor:
        await claim_extractor.cleanup()
    
    if evidence_retriever:
        await evidence_retriever.cleanup()
    
    if stance_classifier:
        await stance_classifier.cleanup()

@app.get("/healthz")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "verification",
        "version": "0.2.0",
        "components": {
            "claim_extractor": claim_extractor is not None,
            "evidence_retriever": evidence_retriever is not None,
            "stance_classifier": stance_classifier is not None
        }
    }

@app.post("/verify/extract-claims", response_model=List[ClaimResponse])
async def extract_claims(
    request: ExtractClaimsRequest,
    background_tasks: BackgroundTasks
):
    """Extract verifiable claims from text."""
    
    logger.info(
        "Extracting claims from text",
        text_length=len(request.text),
        confidence_threshold=request.confidence_threshold,
        max_claims=request.max_claims
    )
    
    try:
        if not claim_extractor:
            raise HTTPException(status_code=503, detail="Claim extractor not available")
        
        claims = await claim_extractor.extract_claims(
            text=request.text,
            confidence_threshold=request.confidence_threshold,
            max_claims=request.max_claims
        )
        
        # Convert to response format
        claim_responses = []
        for claim in claims:
            claim_response = ClaimResponse(
                id=claim.id,
                text=claim.text,
                confidence=claim.confidence,
                claim_type=claim.claim_type,
                subject=claim.subject,
                predicate=claim.predicate,
                object=claim.object_,
                temporal=claim.temporal,
                location=claim.location
            )
            claim_responses.append(claim_response)
        
        # Log for analytics (background task)
        background_tasks.add_task(
            log_claim_extraction,
            text_length=len(request.text),
            claims_found=len(claims),
            confidence_threshold=request.confidence_threshold
        )
        
        logger.info(
            "Claims extracted successfully",
            claims_count=len(claims),
            average_confidence=sum(c.confidence for c in claims) / len(claims) if claims else 0
        )
        
        return claim_responses
        
    except Exception as e:
        logger.error("Failed to extract claims", error=str(e))
        raise HTTPException(status_code=500, detail=f"Claim extraction failed: {str(e)}")

@app.post("/verify/find-evidence", response_model=List[EvidenceResponse])
async def find_evidence(
    request: FindEvidenceRequest,
    background_tasks: BackgroundTasks
):
    """Find supporting evidence for a claim."""
    
    logger.info(
        "Finding evidence for claim",
        claim=request.claim[:100] + "..." if len(request.claim) > 100 else request.claim,
        max_sources=request.max_sources,
        source_types=request.source_types
    )
    
    try:
        if not evidence_retriever:
            raise HTTPException(status_code=503, detail="Evidence retriever not available")
        
        evidence_list = await evidence_retriever.find_evidence(
            claim=request.claim,
            max_sources=request.max_sources,
            source_types=request.source_types,
            language=request.language
        )
        
        # Convert to response format
        evidence_responses = []
        for evidence in evidence_list:
            evidence_response = EvidenceResponse(
                id=evidence.id,
                source_url=evidence.source_url,
                source_title=evidence.source_title,
                source_type=evidence.source_type,
                snippet=evidence.snippet,
                relevance_score=evidence.relevance_score,
                credibility_score=evidence.credibility_score,
                publication_date=evidence.publication_date,
                author=evidence.author
            )
            evidence_responses.append(evidence_response)
        
        # Log for analytics
        background_tasks.add_task(
            log_evidence_retrieval,
            claim=request.claim,
            evidence_found=len(evidence_list),
            source_types=request.source_types
        )
        
        logger.info(
            "Evidence retrieved successfully",
            evidence_count=len(evidence_list),
            average_relevance=sum(e.relevance_score for e in evidence_list) / len(evidence_list) if evidence_list else 0
        )
        
        return evidence_responses
        
    except Exception as e:
        logger.error("Failed to find evidence", error=str(e))
        raise HTTPException(status_code=500, detail=f"Evidence retrieval failed: {str(e)}")

@app.post("/verify/classify-stance", response_model=StanceResponse)
async def classify_stance(
    request: ClassifyStanceRequest,
    background_tasks: BackgroundTasks
):
    """Classify the stance of evidence toward a claim."""
    
    logger.info(
        "Classifying stance",
        claim=request.claim[:50] + "..." if len(request.claim) > 50 else request.claim,
        evidence_length=len(request.evidence)
    )
    
    try:
        if not stance_classifier:
            raise HTTPException(status_code=503, detail="Stance classifier not available")
        
        stance_result = await stance_classifier.classify_stance(
            claim=request.claim,
            evidence=request.evidence,
            context=request.context
        )
        
        stance_response = StanceResponse(
            stance=stance_result.stance,
            confidence=stance_result.confidence,
            reasoning=stance_result.reasoning,
            key_phrases=stance_result.key_phrases
        )
        
        # Log for analytics
        background_tasks.add_task(
            log_stance_classification,
            stance=stance_result.stance,
            confidence=stance_result.confidence
        )
        
        logger.info(
            "Stance classified successfully",
            stance=stance_result.stance,
            confidence=stance_result.confidence
        )
        
        return stance_response
        
    except Exception as e:
        logger.error("Failed to classify stance", error=str(e))
        raise HTTPException(status_code=500, detail=f"Stance classification failed: {str(e)}")

@app.get("/verify/credibility/{source_url:path}", response_model=CredibilityResponse)
async def assess_credibility(
    source_url: str,
    background_tasks: BackgroundTasks
):
    """Assess the credibility of a source."""
    
    logger.info("Assessing source credibility", source_url=source_url)
    
    try:
        if not evidence_retriever:
            raise HTTPException(status_code=503, detail="Evidence retriever not available")
        
        credibility = await evidence_retriever.assess_credibility(source_url)
        
        credibility_response = CredibilityResponse(
            credibility_score=credibility.credibility_score,
            bias_rating=credibility.bias_rating,
            factual_reporting=credibility.factual_reporting,
            transparency_score=credibility.transparency_score,
            authority_indicators=credibility.authority_indicators,
            red_flags=credibility.red_flags
        )
        
        # Log for analytics
        background_tasks.add_task(
            log_credibility_assessment,
            source_url=source_url,
            credibility_score=credibility.credibility_score,
            bias_rating=credibility.bias_rating
        )
        
        logger.info(
            "Credibility assessed successfully",
            source_url=source_url,
            credibility_score=credibility.credibility_score
        )
        
        return credibility_response
        
    except Exception as e:
        logger.error("Failed to assess credibility", error=str(e))
        raise HTTPException(status_code=500, detail=f"Credibility assessment failed: {str(e)}")

@app.get("/verify/stats")
async def get_verification_stats():
    """Get verification service statistics."""
    
    stats = {
        "service": "verification",
        "version": "0.2.0",
        "uptime": time.time(),
        "components": {
            "claim_extractor": {
                "status": "ready" if claim_extractor else "not_ready",
                "model_loaded": claim_extractor.is_model_loaded() if claim_extractor else False
            },
            "evidence_retriever": {
                "status": "ready" if evidence_retriever else "not_ready",
                "sources_available": len(evidence_retriever.get_available_sources()) if evidence_retriever else 0
            },
            "stance_classifier": {
                "status": "ready" if stance_classifier else "not_ready",
                "model_loaded": stance_classifier.is_model_loaded() if stance_classifier else False
            }
        }
    }
    
    return stats

# Background task functions for logging
async def log_claim_extraction(text_length: int, claims_found: int, confidence_threshold: float):
    """Log claim extraction for analytics."""
    logger.info(
        "Claim extraction analytics",
        text_length=text_length,
        claims_found=claims_found,
        confidence_threshold=confidence_threshold,
        claims_per_char=claims_found / text_length if text_length > 0 else 0
    )

async def log_evidence_retrieval(claim: str, evidence_found: int, source_types: List[str]):
    """Log evidence retrieval for analytics."""
    logger.info(
        "Evidence retrieval analytics",
        claim_length=len(claim),
        evidence_found=evidence_found,
        source_types=source_types
    )

async def log_stance_classification(stance: str, confidence: float):
    """Log stance classification for analytics."""
    logger.info(
        "Stance classification analytics",
        stance=stance,
        confidence=confidence
    )

async def log_credibility_assessment(source_url: str, credibility_score: float, bias_rating: str):
    """Log credibility assessment for analytics."""
    logger.info(
        "Credibility assessment analytics",
        source_domain=source_url.split('/')[2] if '/' in source_url else source_url,
        credibility_score=credibility_score,
        bias_rating=bias_rating
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8617,
        reload=True,
        log_level="info"
    )
