"""Pydantic request/response models for the doc-entities API."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EntityModel(BaseModel):
    id: Optional[str] = Field(None, description="Entity ID")
    text: str = Field(..., description="Entity text")
    label: str = Field(..., description="Entity label/type")
    start: int = Field(..., description="Start character position")
    end: int = Field(..., description="End character position")
    confidence: Optional[float] = Field(None, description="Confidence score")
    context: Optional[str] = Field(None, description="Context around entity")
    resolution_status: Optional[str] = Field(None, description="Entity linking status")
    resolution_score: Optional[float] = Field(None, description="Entity linking confidence")
    resolution_target: Optional[str] = Field(None, description="Resolved graph node identifier")


class RelationModel(BaseModel):
    id: Optional[str] = Field(None, description="Relation ID")
    subject: str = Field(..., description="Subject entity text")
    subject_label: str = Field(..., description="Subject entity label")
    predicate: str = Field(..., description="Relation type/predicate")
    object: str = Field(..., description="Object entity text")
    object_label: str = Field(..., description="Object entity label")
    confidence: Optional[float] = Field(None, description="Confidence score")
    context: Optional[str] = Field(None, description="Relation context")


class NERRequest(BaseModel):
    text: str = Field(..., description="Text to analyze")
    language: str = Field("en", description="Language for NER")


class NERResponse(BaseModel):
    entities: List[EntityModel] = Field(default_factory=list)
    model: str = Field(..., description="NER model used")
    language: str = Field(..., description="Language processed")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")


class RelationExtractionRequest(BaseModel):
    text: str = Field(..., description="Document text")
    language: str = Field("en", description="Language code")
    entities: Optional[List[EntityModel]] = Field(None, description="Pre-extracted entities")
    extract_new_entities: bool = Field(True, description="Whether to extract entities if not provided")


class RelationExtractionResponse(BaseModel):
    relations: List[RelationModel] = Field(default_factory=list)
    entities: List[EntityModel] = Field(default_factory=list)
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")


class SummarizationRequest(BaseModel):
    text: str = Field(..., description="Text to summarize")
    language: str = Field("en", description="Language code")


class SummarizationResponse(BaseModel):
    summary: str = Field(..., description="Generated summary")
    original_length: int = Field(..., description="Original text length")
    summary_length: int = Field(..., description="Summary text length")
    compression_ratio: float = Field(..., description="Summary compression ratio")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")


class DocumentAnnotationRequest(BaseModel):
    text: str = Field(..., description="Document text")
    language: str = Field("en", description="Language code")
    doc_id: Optional[str] = Field(None, description="Document identifier")
    title: Optional[str] = Field(None, description="Document title")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    extract_entities: bool = Field(True)
    extract_relations: bool = Field(True)
    generate_summary: bool = Field(False)
    resolve_entities: bool = Field(False)


class DocumentAnnotationResponse(BaseModel):
    doc_id: str = Field(..., description="Document identifier")
    entities: List[EntityModel] = Field(default_factory=list)
    relations: List[RelationModel] = Field(default_factory=list)
    summary: Optional[str] = Field(None, description="Generated summary")
    html_content: Optional[str] = Field(None, description="HTML with highlighted entities")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DocumentModel(BaseModel):
    doc_id: str = Field(..., description="Document identifier")
    title: Optional[str] = Field(None, description="Document title")
    text: Optional[str] = Field(None, description="Document text")
    entities: List[EntityModel] = Field(default_factory=list)
    relations: List[RelationModel] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = Field(None, description="Document metadata")
    created_at: Optional[str] = Field(None, description="Creation timestamp")


class EntityResolutionRequest(BaseModel):
    entity_ids: List[str] = Field(..., description="Entity identifiers to resolve")


class EntityResolutionResponse(BaseModel):
    resolved_entities: List[Dict[str, Any]] = Field(default_factory=list)
    resolution_metadata: Dict[str, Any] = Field(default_factory=dict)


class FuzzyMatchRequest(BaseModel):
    query: str = Field(..., description="Query string")
    candidates: List[str] = Field(..., description="Candidate strings")
    threshold: float = Field(85.0, ge=0.0, le=100.0, description="Similarity threshold")
    limit: int = Field(10, description="Maximum number of matches")
    scorer: str = Field("fuzz.ratio", description="Scoring algorithm")


class FuzzyMatchResponse(BaseModel):
    query: str = Field(..., description="Original query")
    matches: List[Dict[str, Any]] = Field(default_factory=list)
    total_candidates: int = Field(..., description="Total candidates processed")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")


class FuzzyDedupeRequest(BaseModel):
    strings: List[str] = Field(..., description="Strings to deduplicate")
    threshold: float = Field(85.0, ge=0.0, le=100.0, description="Similarity threshold")
    scorer: str = Field("fuzz.ratio", description="Scoring algorithm")


class FuzzyDedupeResponse(BaseModel):
    clusters: List[List[str]] = Field(default_factory=list)
    total_items: int = Field(...)
    unique_clusters: int = Field(...)
    deduplication_ratio: float = Field(...)
    threshold: float = Field(...)
    scorer: str = Field(...)
