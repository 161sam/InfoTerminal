"""
XAI v1 router for explainable AI and model interpretability.
Provides text explanation, model transparency, and attention visualization.
"""

import re
import time
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, status, Query
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

# Import models
from ..models import (
    ExplainTextRequest,
    ExplainModelRequest,
    CompareExplanationsRequest,
    TokenHighlight,
    ExplanationMetadata,
    TextExplanationResponse,
    ModelCard,
    ExplanationComparison,
    ModelExplanationResponse,
    ExplanationStats,
    ServiceCapabilities
)

router = APIRouter(tags=["XAI"], prefix="/v1")

# Service statistics (in-memory for demo)
_stats = {
    "total_explanations": 0,
    "explanations_by_method": {},
    "processing_times": []
}


def _heuristic_explain(text: str, query: Optional[str] = None, confidence_threshold: float = 0.5) -> TextExplanationResponse:
    """
    Heuristic-based text explanation with token highlighting.
    """
    start_time = time.time()
    
    tokens = [t for t in text.split() if t]
    highlights: List[TokenHighlight] = []
    
    # Query-based highlighting
    if query:
        q_tokens = [qt.lower() for qt in query.split() if len(qt) > 2]
        for i, tok in enumerate(tokens):
            low = tok.lower().strip('.,;:()[]{}"\'')
            if any(qt in low for qt in q_tokens):
                confidence = 0.8 if qt == low else 0.6  # Exact match vs partial
                if confidence >= confidence_threshold:
                    highlights.append(TokenHighlight(
                        index=i,
                        token=tok,
                        reason="query_match",
                        confidence=confidence,
                        importance=confidence
                    ))
    
    # Pattern-based highlighting
    for i, tok in enumerate(tokens):
        # Date patterns
        if any(c.isdigit() for c in tok) and any(ch in tok for ch in ['/', '-', '.']):
            highlights.append(TokenHighlight(
                index=i,
                token=tok,
                reason="date_pattern",
                confidence=0.7,
                importance=0.6
            ))
        
        # Numeric values
        elif tok.replace(',', '').replace('.', '').isdigit():
            highlights.append(TokenHighlight(
                index=i,
                token=tok,
                reason="numeric_value",
                confidence=0.6,
                importance=0.5
            ))
        
        # URLs
        elif 'http' in tok.lower() or 'www.' in tok.lower():
            highlights.append(TokenHighlight(
                index=i,
                token=tok,
                reason="url",
                confidence=0.9,
                importance=0.8
            ))
        
        # Email addresses
        elif '@' in tok and '.' in tok:
            highlights.append(TokenHighlight(
                index=i,
                token=tok,
                reason="email",
                confidence=0.8,
                importance=0.7
            ))
        
        # Capitalized words (potential proper nouns)
        elif tok[0].isupper() and len(tok) > 3:
            highlights.append(TokenHighlight(
                index=i,
                token=tok,
                reason="proper_noun",
                confidence=0.4,
                importance=0.3
            ))
    
    # Remove duplicates and filter by confidence
    seen_indices = set()
    filtered_highlights = []
    for h in highlights:
        if h.index not in seen_indices and h.confidence >= confidence_threshold:
            seen_indices.add(h.index)
            filtered_highlights.append(h)
    
    processing_time = (time.time() - start_time) * 1000
    
    # Generate summary
    highlight_reasons = [h.reason for h in filtered_highlights]
    reason_counts = {}
    for reason in highlight_reasons:
        reason_counts[reason] = reason_counts.get(reason, 0) + 1
    
    summary_parts = []
    if reason_counts:
        for reason, count in reason_counts.items():
            summary_parts.append(f"{count} {reason.replace('_', ' ')} tokens")
        summary = f"Highlighted {len(filtered_highlights)} tokens: " + ", ".join(summary_parts)
    else:
        summary = "No significant patterns detected in the text"
    
    return TextExplanationResponse(
        tokens=tokens,
        highlights=filtered_highlights,
        meta=ExplanationMetadata(
            method="heuristic",
            confidence=0.5,
            processing_time_ms=processing_time,
            model_version="heuristic_v1"
        ),
        summary=summary
    )


def _attention_explain(text: str, query: Optional[str] = None) -> TextExplanationResponse:
    """
    Simulated attention-based explanation (placeholder for real attention models).
    """
    start_time = time.time()
    
    tokens = text.split()
    highlights: List[TokenHighlight] = []
    
    # Simulate attention weights (in real implementation, this would come from a transformer model)
    for i, token in enumerate(tokens):
        # Simulate higher attention for content words
        base_attention = 0.3
        if len(token) > 4:  # Longer words get more attention
            base_attention += 0.2
        if token.lower() in ['important', 'critical', 'significant', 'major', 'key']:
            base_attention += 0.4
        if query and any(q.lower() in token.lower() for q in query.split()):
            base_attention += 0.3
        
        if base_attention > 0.5:
            highlights.append(TokenHighlight(
                index=i,
                token=token,
                reason="high_attention",
                confidence=min(base_attention, 1.0),
                importance=min(base_attention, 1.0)
            ))
    
    processing_time = (time.time() - start_time) * 1000
    
    return TextExplanationResponse(
        tokens=tokens,
        highlights=highlights,
        meta=ExplanationMetadata(
            method="attention",
            confidence=0.7,
            processing_time_ms=processing_time,
            model_version="simulated_attention_v1"
        ),
        summary=f"Attention-based highlighting identified {len(highlights)} important tokens"
    )


# API Endpoints
@router.post("/explain/text", response_model=TextExplanationResponse)
async def explain_text(request: ExplainTextRequest):
    """
    Explain text with token-level highlighting.
    
    Supports multiple explanation methods:
    - heuristic: Pattern-based highlighting
    - attention: Attention-based highlighting (simulated)
    """
    try:
        # Update statistics
        _stats["total_explanations"] += 1
        method_count = _stats["explanations_by_method"].get(request.method, 0)
        _stats["explanations_by_method"][request.method] = method_count + 1
        
        # Route to appropriate explanation method
        if request.method == "heuristic":
            result = _heuristic_explain(
                request.text, 
                request.query, 
                request.confidence_threshold
            )
        elif request.method == "attention":
            result = _attention_explain(request.text, request.query)
        else:
            raise_http_error("UNSUPPORTED_METHOD", f"Explanation method '{request.method}' not supported")
        
        # Track processing time
        if result.meta.processing_time_ms:
            _stats["processing_times"].append(result.meta.processing_time_ms)
            if len(_stats["processing_times"]) > 1000:  # Keep only recent times
                _stats["processing_times"] = _stats["processing_times"][-1000:]
        
        return result
        
    except Exception as e:
        raise_http_error("EXPLANATION_FAILED", f"Text explanation failed: {str(e)}")


@router.post("/explain/compare", response_model=ExplanationComparison)
async def compare_explanations(request: CompareExplanationsRequest):
    """
    Compare multiple explanation methods on the same text.
    
    Provides insight into agreement between different explainability approaches.
    """
    try:
        explanations = {}
        
        for method in request.methods:
            explain_request = ExplainTextRequest(
                text=request.text,
                query=request.query,
                method=method
            )
            explanation = await explain_text(explain_request)
            explanations[method] = explanation
        
        # Calculate agreement score (simplified)
        if len(explanations) >= 2:
            all_highlighted_indices = []
            for exp in explanations.values():
                highlighted = {h.index for h in exp.highlights}
                all_highlighted_indices.append(highlighted)
            
            # Jaccard similarity between first two methods
            if len(all_highlighted_indices) >= 2:
                intersection = len(all_highlighted_indices[0] & all_highlighted_indices[1])
                union = len(all_highlighted_indices[0] | all_highlighted_indices[1])
                agreement_score = intersection / union if union > 0 else 0.0
            else:
                agreement_score = 0.0
        else:
            agreement_score = 1.0
        
        # Determine recommended method
        method_scores = {}
        for method, exp in explanations.items():
            method_scores[method] = exp.meta.confidence
        
        recommended_method = max(method_scores.keys(), key=lambda k: method_scores[k])
        
        # Identify differences
        differences = []
        if len(explanations) >= 2:
            methods = list(explanations.keys())
            exp1, exp2 = explanations[methods[0]], explanations[methods[1]]
            
            if len(exp1.highlights) != len(exp2.highlights):
                differences.append(f"{methods[0]} highlighted {len(exp1.highlights)} tokens vs {methods[1]} highlighted {len(exp2.highlights)} tokens")
            
            reasons1 = {h.reason for h in exp1.highlights}
            reasons2 = {h.reason for h in exp2.highlights}
            unique_reasons1 = reasons1 - reasons2
            unique_reasons2 = reasons2 - reasons1
            
            if unique_reasons1:
                differences.append(f"{methods[0]} uniquely detected: {', '.join(unique_reasons1)}")
            if unique_reasons2:
                differences.append(f"{methods[1]} uniquely detected: {', '.join(unique_reasons2)}")
        
        return ExplanationComparison(
            text=request.text,
            explanations=explanations,
            agreement_score=agreement_score,
            recommended_method=recommended_method,
            differences=differences or ["No significant differences detected"]
        )
        
    except Exception as e:
        raise_http_error("COMPARISON_FAILED", f"Explanation comparison failed: {str(e)}")


@router.get("/model-card", response_model=ModelCard)
def get_model_card(method: str = Query("heuristic", description="Explanation method")):
    """
    Get model card with transparency information.
    
    Provides details about explanation methods, limitations, and ethical considerations.
    """
    try:
        if method == "heuristic":
            return ModelCard(
                name="Heuristic Explainer v1.0",
                description="Rule-based text explanation using pattern matching and keyword highlighting",
                intended_use="Highlight relevant terms, dates, numbers, and query matches in text for OSINT analysis",
                limitations=[
                    "No semantic understanding",
                    "Pattern-based only",
                    "Limited to predefined rules",
                    "No context awareness"
                ],
                metrics={
                    "explainability": "basic",
                    "confidence": 0.5,
                    "precision": "variable",
                    "recall": "variable"
                },
                training_data={
                    "type": "rule-based",
                    "source": "manually crafted patterns",
                    "size": "N/A"
                },
                ethical_considerations=[
                    "May miss important context",
                    "Could reinforce existing biases in pattern selection",
                    "Should not be used for high-stakes decisions without human review"
                ]
            )
        elif method == "attention":
            return ModelCard(
                name="Simulated Attention Explainer v1.0",
                description="Simulated attention-based explanation mimicking transformer attention patterns",
                intended_use="Demonstrate attention-based highlighting for educational and prototyping purposes",
                limitations=[
                    "Simulated attention weights",
                    "Not based on real trained model",
                    "Simplified attention mechanism",
                    "No multi-head or multi-layer attention"
                ],
                metrics={
                    "explainability": "medium",
                    "confidence": 0.7,
                    "simulation_accuracy": "low"
                },
                ethical_considerations=[
                    "Simulated results should not be interpreted as real model behavior",
                    "May mislead users about actual model capabilities",
                    "Should be clearly labeled as simulation"
                ]
            )
        else:
            raise_http_error("UNKNOWN_METHOD", f"No model card available for method: {method}")
            
    except Exception as e:
        raise_http_error("MODEL_CARD_FAILED", f"Failed to get model card: {str(e)}")


@router.get("/stats", response_model=ExplanationStats)
def get_stats():
    """
    Get explanation service statistics.
    
    Returns usage metrics and performance data.
    """
    try:
        avg_confidence = 0.6  # Simplified - would calculate from actual explanations
        avg_processing_time = sum(_stats["processing_times"]) / len(_stats["processing_times"]) if _stats["processing_times"] else 0.0
        
        # Most common patterns (simplified)
        common_patterns = ["query_match", "numeric_value", "date_pattern", "proper_noun", "url"]
        
        return ExplanationStats(
            total_explanations=_stats["total_explanations"],
            explanations_by_method=_stats["explanations_by_method"],
            average_confidence=avg_confidence,
            average_processing_time_ms=avg_processing_time,
            most_common_patterns=common_patterns
        )
        
    except Exception as e:
        raise_http_error("STATS_FAILED", f"Failed to get statistics: {str(e)}")


@router.get("/capabilities", response_model=ServiceCapabilities)
def get_capabilities():
    """
    Get service capabilities and configuration.
    
    Returns available explanation methods and service limits.
    """
    return ServiceCapabilities(
        explanation_methods=["heuristic", "attention"],
        supported_formats=["text/plain"],
        max_text_length=10000,
        features=[
            "token_highlighting",
            "query_relevance",
            "pattern_detection",
            "confidence_scoring",
            "method_comparison",
            "model_transparency"
        ],
        performance_metrics={
            "avg_processing_time_ms": sum(_stats["processing_times"]) / len(_stats["processing_times"]) if _stats["processing_times"] else 0.0,
            "throughput_explanations_per_second": 100.0,  # Estimated
            "max_concurrent_requests": 50
        }
    )


@router.post("/explain/batch", response_model=PaginatedResponse)
async def explain_batch(
    texts: List[str],
    method: str = Query("heuristic", description="Explanation method"),
    query: Optional[str] = Query(None, description="Query for relevance highlighting")
):
    """
    Explain multiple texts in batch.
    
    Efficiently processes multiple texts using the same explanation method.
    """
    try:
        if len(texts) > 50:  # Limit batch size
            raise_http_error("BATCH_TOO_LARGE", "Maximum 50 texts per batch request")
        
        results = []
        
        for i, text in enumerate(texts):
            try:
                request = ExplainTextRequest(
                    text=text,
                    query=query,
                    method=method
                )
                explanation = await explain_text(request)
                results.append({
                    "text_index": i,
                    "explanation": explanation.dict(),
                    "status": "success"
                })
            except Exception as e:
                results.append({
                    "text_index": i,
                    "error": str(e),
                    "status": "failed"
                })
        
        return PaginatedResponse(
            items=results,
            total=len(results),
            page=1,
            size=len(results)
        )
        
    except Exception as e:
        raise_http_error("BATCH_EXPLANATION_FAILED", f"Batch explanation failed: {str(e)}")


@router.get("/methods")
def get_available_methods():
    """
    Get available explanation methods and their descriptions.
    """
    return {
        "methods": [
            {
                "name": "heuristic",
                "description": "Pattern-based highlighting using rules and regex",
                "strengths": ["Fast", "Interpretable", "No model required"],
                "weaknesses": ["Limited semantic understanding", "Rule-dependent"],
                "use_cases": ["Quick analysis", "Pattern detection", "Keyword highlighting"]
            },
            {
                "name": "attention",
                "description": "Attention-based highlighting (simulated)",
                "strengths": ["Context-aware", "Semantic understanding", "Flexible"],
                "weaknesses": ["Simulated only", "Computationally expensive", "Model-dependent"],
                "use_cases": ["Deep analysis", "Content understanding", "Research"]
            }
        ],
        "default_method": "heuristic",
        "experimental_methods": ["attention"],
        "coming_soon": ["lime", "shap", "gradient", "integrated_gradients"]
    }
