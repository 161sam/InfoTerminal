"""
Pydantic models for XAI Service v1.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


# Request Models
class ExplainTextRequest(BaseModel):
    """Request for text explanation."""
    text: str = Field(..., description="Text to explain", min_length=1)
    query: Optional[str] = Field(None, description="Query to highlight relevance")
    method: str = Field("heuristic", description="Explanation method to use")
    confidence_threshold: float = Field(0.5, ge=0.0, le=1.0, description="Minimum confidence for highlighting")


class ExplainModelRequest(BaseModel):
    """Request for model explanation."""
    model_name: str = Field(..., description="Name of the model to explain")
    input_data: Dict[str, Any] = Field(..., description="Input data for explanation")
    explanation_type: str = Field("attention", description="Type of explanation")


class CompareExplanationsRequest(BaseModel):
    """Request for comparing multiple explanations."""
    text: str = Field(..., description="Text to explain")
    methods: List[str] = Field(..., description="Explanation methods to compare", min_items=2)
    query: Optional[str] = Field(None, description="Query for relevance highlighting")


# Response Models
class TokenHighlight(BaseModel):
    """Individual token highlight information."""
    index: int = Field(..., description="Token position in text", ge=0)
    token: str = Field(..., description="Token text")
    reason: str = Field(..., description="Reason for highlighting")
    confidence: float = Field(..., description="Confidence score", ge=0.0, le=1.0)
    importance: Optional[float] = Field(None, description="Importance score", ge=0.0, le=1.0)


class ExplanationMetadata(BaseModel):
    """Metadata about the explanation."""
    method: str = Field(..., description="Explanation method used")
    confidence: float = Field(..., description="Overall confidence", ge=0.0, le=1.0)
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")
    model_version: Optional[str] = Field(None, description="Model version used")


class TextExplanationResponse(BaseModel):
    """Response for text explanation."""
    tokens: List[str] = Field(..., description="Tokenized text")
    highlights: List[TokenHighlight] = Field(..., description="Highlighted tokens with explanations")
    meta: ExplanationMetadata = Field(..., description="Explanation metadata")
    summary: str = Field(..., description="Human-readable explanation summary")


class ModelCard(BaseModel):
    """Model card with transparency information."""
    name: str = Field(..., description="Model name")
    description: str = Field(..., description="Model description")
    intended_use: str = Field(..., description="Intended use cases")
    limitations: List[str] = Field(..., description="Known limitations")
    metrics: Dict[str, Any] = Field(..., description="Performance metrics")
    training_data: Optional[Dict[str, Any]] = Field(None, description="Training data information")
    ethical_considerations: Optional[List[str]] = Field(None, description="Ethical considerations")


class AttentionVisualization(BaseModel):
    """Attention visualization data."""
    tokens: List[str] = Field(..., description="Input tokens")
    attention_weights: List[List[float]] = Field(..., description="Attention weight matrix")
    head_view: Optional[Dict[str, Any]] = Field(None, description="Multi-head attention visualization")
    layer_info: Optional[Dict[str, Any]] = Field(None, description="Layer-specific information")


class ExplanationComparison(BaseModel):
    """Comparison between multiple explanation methods."""
    text: str = Field(..., description="Original text")
    explanations: Dict[str, TextExplanationResponse] = Field(..., description="Explanations by method")
    agreement_score: float = Field(..., description="Agreement between methods", ge=0.0, le=1.0)
    recommended_method: str = Field(..., description="Recommended explanation method")
    differences: List[str] = Field(..., description="Key differences between methods")


class FeatureImportance(BaseModel):
    """Feature importance explanation."""
    feature_name: str = Field(..., description="Name of the feature")
    importance_score: float = Field(..., description="Importance score")
    direction: str = Field(..., description="Positive or negative influence")
    confidence: float = Field(..., description="Confidence in importance", ge=0.0, le=1.0)


class ModelExplanationResponse(BaseModel):
    """Response for model explanation."""
    model_name: str = Field(..., description="Model that was explained")
    prediction: Dict[str, Any] = Field(..., description="Model prediction")
    feature_importance: List[FeatureImportance] = Field(..., description="Feature importance rankings")
    attention_visualization: Optional[AttentionVisualization] = Field(None, description="Attention visualization")
    explanation_text: str = Field(..., description="Human-readable explanation")
    confidence: float = Field(..., description="Overall explanation confidence", ge=0.0, le=1.0)


# Statistics and Monitoring Models
class ExplanationStats(BaseModel):
    """Statistics about explanation service usage."""
    total_explanations: int = Field(..., description="Total explanations generated", ge=0)
    explanations_by_method: Dict[str, int] = Field(..., description="Explanations per method")
    average_confidence: float = Field(..., description="Average confidence score", ge=0.0, le=1.0)
    average_processing_time_ms: float = Field(..., description="Average processing time", ge=0.0)
    most_common_patterns: List[str] = Field(..., description="Most commonly detected patterns")


class ServiceCapabilities(BaseModel):
    """Service capabilities and available methods."""
    explanation_methods: List[str] = Field(..., description="Available explanation methods")
    supported_formats: List[str] = Field(..., description="Supported input formats")
    max_text_length: int = Field(..., description="Maximum text length", ge=1)
    features: List[str] = Field(..., description="Available features")
    performance_metrics: Dict[str, float] = Field(..., description="Performance benchmarks")


# Error Models
class XAIError(BaseModel):
    """Error model for XAI operations."""
    operation: str = Field(..., description="Operation that failed")
    error_code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
