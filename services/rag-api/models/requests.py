"""
Pydantic models for RAG API Service v1.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class LawDoc(BaseModel):
    """Legal document for indexing and retrieval."""
    id: str = Field(..., description="Unique document identifier")
    title: Optional[str] = Field(None, description="Document title")
    paragraph: Optional[str] = Field(None, description="Paragraph or section identifier")
    text: str = Field(..., description="Document text content", min_length=1)
    domain: Optional[str] = Field(None, description="Legal domain (e.g., compliance, tax)")
    source: Optional[str] = Field(None, description="Source of the document")
    effective_date: Optional[str] = Field(None, description="Effective date of the law")


class RetrieveResponse(BaseModel):
    """Response for document retrieval."""
    total: int = Field(..., description="Total number of matching documents", ge=0)
    items: List[Dict[str, Any]] = Field(..., description="Retrieved documents")


class ContextResponse(BaseModel):
    """Response for entity context search."""
    entity: str = Field(..., description="Entity for which context was requested")
    laws: List[Dict[str, Any]] = Field(..., description="Relevant laws for the entity")


class KNNVectorRequest(BaseModel):
    """Request for vector-based KNN search."""
    vector: List[float] = Field(..., description="Query vector for similarity search")
    k: int = Field(10, description="Number of nearest neighbors to return", ge=1, le=100)
    filters: Optional[Dict[str, Any]] = Field(None, description="Additional filters for search")


class HybridRequest(BaseModel):
    """Request for hybrid search combining BM25 and KNN."""
    q: str = Field(..., description="Query text", min_length=1)
    top_k: int = Field(10, description="Number of results from text search", ge=1, le=100)
    k: int = Field(10, description="Number of results from vector search", ge=1, le=100)
    alpha: float = Field(0.5, description="Weight for BM25 vs KNN (0.0-1.0)", ge=0.0, le=1.0)
    filters: Optional[Dict[str, Any]] = Field(None, description="Search filters")


class EfSearchRequest(BaseModel):
    """Request to update ef_search parameter for HNSW index."""
    ef_search: int = Field(..., description="ef_search parameter for HNSW", ge=1, le=1000)


class IndexResponse(BaseModel):
    """Response for document indexing."""
    status: str = Field(..., description="Indexing status")
    id: str = Field(..., description="Document ID")
    message: str = Field(default="Document successfully indexed")


class GraphUpsertRequest(BaseModel):
    """Request for upserting law into graph database."""
    doc: LawDoc = Field(..., description="Law document to upsert")
    applies_to: Optional[List[str]] = Field(None, description="Sectors this law applies to")
    sectors: Optional[List[str]] = Field(None, description="Legal sectors")
    firms: Optional[List[str]] = Field(None, description="Firms this law applies to")


class GraphUpsertResponse(BaseModel):
    """Response for graph upsert operation."""
    status: str = Field(..., description="Upsert status")
    law_id: str = Field(..., description="Law document ID")
    sectors: List[str] = Field(default_factory=list, description="Applied sectors")
    firms: List[str] = Field(default_factory=list, description="Applied firms")


class ExtractEventsRequest(BaseModel):
    """Request for event extraction from text."""
    text: str = Field(..., description="Text to extract events from", min_length=1)


class Event(BaseModel):
    """Extracted event information."""
    type: str = Field(..., description="Type of event detected")
    date: Optional[str] = Field(None, description="Date associated with event")
    snippet: str = Field(..., description="Text snippet containing the event")


class ExtractEventsResponse(BaseModel):
    """Response for event extraction."""
    events: List[Event] = Field(..., description="Extracted events from text")


class FeedbackRequest(BaseModel):
    """Request for providing feedback/labels."""
    query: Optional[str] = Field(None, description="Original query")
    document_id: Optional[str] = Field(None, description="Document ID")
    relevance: Optional[int] = Field(None, description="Relevance score (1-5)", ge=1, le=5)
    label: Optional[str] = Field(None, description="Text label or category")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional feedback metadata")


class FeedbackResponse(BaseModel):
    """Response for feedback submission.""" 
    status: str = Field(..., description="Feedback submission status")
    message: str = Field(default="Feedback successfully recorded")


class SearchParameters(BaseModel):
    """Common search parameters."""
    query: str = Field(..., description="Search query", min_length=1)
    top_k: int = Field(10, description="Number of results to return", ge=1, le=100)
    rerank: int = Field(0, description="Reranking method (0=none, 1=term-coverage, 2=embedding)", ge=0, le=2)


class KNNSearchParameters(BaseModel):
    """Parameters for KNN search."""
    query: str = Field(..., description="Search query for embedding", min_length=1)
    k: int = Field(10, description="Number of nearest neighbors", ge=1, le=100)


class ContextSearchParameters(BaseModel):
    """Parameters for context search."""
    entity: str = Field(..., description="Entity to find context for", min_length=1)
    top_k: int = Field(10, description="Maximum number of laws to return", ge=1, le=100)
