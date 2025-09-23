"""
XAI service models package.
"""

from .requests import (
    # Request Models
    ExplainTextRequest,
    ExplainModelRequest,
    CompareExplanationsRequest,
    
    # Response Models
    TokenHighlight,
    ExplanationMetadata,
    TextExplanationResponse,
    ModelCard,
    AttentionVisualization,
    ExplanationComparison,
    FeatureImportance,
    ModelExplanationResponse,
    ExplanationStats,
    ServiceCapabilities,
    
    # Error Models
    XAIError
)

__all__ = [
    # Request Models
    "ExplainTextRequest",
    "ExplainModelRequest",
    "CompareExplanationsRequest",
    
    # Response Models
    "TokenHighlight",
    "ExplanationMetadata",
    "TextExplanationResponse",
    "ModelCard",
    "AttentionVisualization", 
    "ExplanationComparison",
    "FeatureImportance",
    "ModelExplanationResponse",
    "ExplanationStats",
    "ServiceCapabilities",
    
    # Error Models
    "XAIError"
]
