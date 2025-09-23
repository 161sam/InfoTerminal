"""Domain router for doc-entities v1 endpoints."""
from __future__ import annotations

import html
import time
import uuid
from collections import Counter
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query

from _shared.api_standards import APIError, ErrorCodes
from fuzzy_matcher import DedupeRequest, FuzzyMatcher, MatchRequest
from nlp_loader import ner_spacy, summarize
from nlp_client import ner as nlp_ner
from relation_extractor import extract_relations
from resolver import resolve_entities

from ..db import SessionLocal
from ..models import Document, Entity, EntityResolution, Relation, RelationResolution
from ..models.api_models import (
    DocumentAnnotationRequest,
    DocumentAnnotationResponse,
    DocumentModel,
    EntityModel,
    EntityResolutionResponse,
    FuzzyDedupeRequest,
    FuzzyDedupeResponse,
    FuzzyMatchRequest,
    FuzzyMatchResponse,
    NERRequest,
    NERResponse,
    RelationExtractionRequest,
    RelationExtractionResponse,
    RelationModel,
    SummarizationRequest,
    SummarizationResponse,
)


@dataclass
class DocEntitiesService:
    """Encapsulates doc-entities domain behaviours."""

    allow_test: bool
    graph_api_url: str
    graph_write_relations: bool
    session_factory: Any = SessionLocal

    def __post_init__(self) -> None:
        if self.allow_test:
            self.mem_texts: Dict[str, Dict[str, Any]] = {}
            self.mem_entities: Dict[str, List[Dict[str, Any]]] = {}
        else:
            self.mem_texts = {}
            self.mem_entities = {}

    # ------------------------------------------------------------------
    # Helper utilities
    # ------------------------------------------------------------------
    def _context(self, text: str, start: Optional[int], end: Optional[int], width: int = 30) -> str:
        if start is None or end is None:
            return ""
        s = max(0, start - width)
        e = min(len(text), end + width)
        return text[s:e]

    def _highlight(self, text: str, entities: List[EntityModel]) -> str:
        spans = sorted(
            [
                (ent.start, ent.end, ent.label, ent.text)
                for ent in entities
                if ent.start is not None and ent.end is not None
            ],
            key=lambda tup: tup[0],
        )
        parts: List[str] = []
        cur = 0
        for start, end, label, _ in spans:
            start = max(0, start)
            end = min(len(text), end)
            parts.append(html.escape(text[cur:start]))
            parts.append(
                f'<span class="entity" data-label="{html.escape(label or "")}">{html.escape(text[start:end])}</span>'
            )
            cur = end
        parts.append(html.escape(text[cur:]))
        return "".join(parts)

    def _write_relations_to_graph(self, doc_id: str, relations: List[RelationModel]):
        if not self.graph_write_relations:
            return
        try:
            import requests
        except ImportError:
            return

        try:
            payload = {
                "doc_id": doc_id,
                "relations": [
                    {
                        "subject": rel.subject,
                        "subject_label": rel.subject_label,
                        "predicate": rel.predicate,
                        "object": rel.object,
                        "object_label": rel.object_label,
                        "confidence": rel.confidence,
                        "context": rel.context,
                    }
                    for rel in relations
                ],
            }
            response = requests.post(f"{self.graph_api_url}/v1/relations", json=payload, timeout=10)
            if response.status_code == 200 and not self.allow_test:
                with self.session_factory() as db:
                    for relation in relations:
                        if relation.id:
                            rel_resolution = db.get(RelationResolution, uuid.UUID(relation.id))
                            if rel_resolution:
                                rel_resolution.status = "resolved"
                                rel_resolution.graph_edge_id = response.json().get("edge_id")
                    db.commit()
        except Exception:
            # Swallow errors to avoid failing primary request
            return

    # ------------------------------------------------------------------
    # Endpoint handlers
    # ------------------------------------------------------------------
    def extract_entities(self, request: NERRequest) -> NERResponse:
        start_time = time.time()
        entities_data = ner_spacy(request.text, request.language)
        entities = [
            EntityModel(
                text=data.get("text", ""),
                label=data.get("label", ""),
                start=data.get("start", 0),
                end=data.get("end", 0),
                confidence=data.get("score"),
            )
            for data in entities_data
        ]
        return NERResponse(
            entities=entities,
            model="spaCy",
            language=request.language,
            processing_time_ms=int((time.time() - start_time) * 1000),
        )

    def extract_text_relations(self, request: RelationExtractionRequest) -> RelationExtractionResponse:
        start_time = time.time()
        if request.entities:
            entities = [
                {
                    "id": str(uuid.uuid4()),
                    "text": ent.text,
                    "label": ent.label,
                    "span_start": ent.start,
                    "span_end": ent.end,
                    "value": ent.text,
                }
                for ent in request.entities
            ]
        elif request.extract_new_entities:
            ner_result = ner_spacy(request.text, request.language)
            entities = [
                {
                    "id": str(uuid.uuid4()),
                    "text": ent["text"],
                    "label": ent["label"],
                    "span_start": ent["start"],
                    "span_end": ent["end"],
                    "value": ent["text"],
                }
                for ent in ner_result
            ]
        else:
            entities = []

        if len(entities) < 2:
            return RelationExtractionResponse(
                relations=[],
                entities=[],
                processing_time_ms=int((time.time() - start_time) * 1000),
            )

        extracted_relations = extract_relations(request.text, entities)
        relations: List[RelationModel] = []
        for rel in extracted_relations:
            subject_entity = next((e for e in entities if e["id"] == rel["subject_entity_id"]), None)
            object_entity = next((e for e in entities if e["id"] == rel["object_entity_id"]), None)
            if subject_entity and object_entity:
                relations.append(
                    RelationModel(
                        subject=subject_entity["value"],
                        subject_label=subject_entity["label"],
                        predicate=rel["predicate"],
                        object=object_entity["value"],
                        object_label=object_entity["label"],
                        confidence=rel.get("confidence", 0.5),
                        context=rel.get("context", ""),
                    )
                )

        entity_models = [
            EntityModel(
                id=ent["id"],
                text=ent["text"],
                label=ent["label"],
                start=ent["span_start"],
                end=ent["span_end"],
                confidence=ent.get("confidence"),
            )
            for ent in entities
        ]

        return RelationExtractionResponse(
            relations=relations,
            entities=entity_models,
            processing_time_ms=int((time.time() - start_time) * 1000),
        )

    def summarize_text(self, request: SummarizationRequest) -> SummarizationResponse:
        start_time = time.time()
        summary_text = summarize(request.text, request.language)
        original_length = len(request.text)
        summary_length = len(summary_text)
        compression_ratio = summary_length / original_length if original_length else 0
        return SummarizationResponse(
            summary=summary_text,
            original_length=original_length,
            summary_length=summary_length,
            compression_ratio=compression_ratio,
            processing_time_ms=int((time.time() - start_time) * 1000),
        )

    def annotate_document(
        self,
        request: DocumentAnnotationRequest,
        background_tasks: BackgroundTasks,
    ) -> DocumentAnnotationResponse:
        doc_id = request.doc_id or str(uuid.uuid4())
        metadata = request.metadata or {}
        entities: List[EntityModel] = []
        relations: List[RelationModel] = []
        summary_text: Optional[str] = None

        if self.allow_test:
            tokens = request.text.split()
            if request.extract_entities and tokens:
                ent_text = tokens[0]
                entity = EntityModel(
                    id=str(uuid.uuid4()),
                    text=ent_text,
                    label="TEST",
                    start=0,
                    end=len(ent_text),
                    confidence=0.5,
                    context=self._context(request.text, 0, len(ent_text)),
                    resolution_status="pending",
                    resolution_score=None,
                    resolution_target=None,
                )
                entities.append(entity)
            if request.extract_relations and len(entities) >= 2:
                relations.append(
                    RelationModel(
                        subject=entities[0].text,
                        subject_label=entities[0].label,
                        predicate="RELATED_TO",
                        object=entities[1].text,
                        object_label=entities[1].label,
                        confidence=0.5,
                    )
                )
            if request.generate_summary:
                summary_text = f"Summary of document with {len(entities)} entities"
            self.mem_texts[doc_id] = {
                "title": request.title,
                "text": request.text,
                "metadata": metadata,
            }
            self.mem_entities[doc_id] = [entity.dict() for entity in entities]
        else:
            with self.session_factory() as db:
                doc = Document(id=uuid.UUID(doc_id), title=request.title, aleph_id=metadata.get("aleph_id"))
                db.merge(doc)

                if request.extract_entities:
                    ner_result = nlp_ner(request.text)
                    for ent_data in ner_result:
                        context = self._context(request.text, ent_data.get("start"), ent_data.get("end"))
                        ent = Entity(
                            doc_id=doc.id,
                            label=ent_data.get("label", ""),
                            value=ent_data.get("text", ""),
                            span_start=ent_data.get("start"),
                            span_end=ent_data.get("end"),
                            confidence=ent_data.get("score"),
                            context=context,
                        )
                        db.add(ent)
                        db.flush()
                        db.add(EntityResolution(entity_id=ent.id, status="pending"))
                        entities.append(
                            EntityModel(
                                id=str(ent.id),
                                text=ent.value,
                                label=ent.label,
                                start=ent.span_start,
                                end=ent.span_end,
                                confidence=ent.confidence,
                                context=context,
                                resolution_status="pending",
                                resolution_score=None,
                                resolution_target=None,
                            )
                        )

                if request.extract_relations and len(entities) >= 2:
                    entity_dicts = [
                        {
                            "id": ent.id,
                            "text": ent.text,
                            "label": ent.label,
                            "span_start": ent.start,
                            "span_end": ent.end,
                            "value": ent.text,
                        }
                        for ent in entities
                    ]
                    extracted_relations = extract_relations(request.text, entity_dicts)
                    for rel in extracted_relations:
                        relation_obj = Relation(
                            doc_id=doc.id,
                            subject_entity_id=uuid.UUID(rel["subject_entity_id"]),
                            object_entity_id=uuid.UUID(rel["object_entity_id"]),
                            predicate=rel["predicate"],
                            predicate_text=rel.get("predicate_text"),
                            confidence=rel.get("confidence"),
                            span_start=rel.get("span_start"),
                            span_end=rel.get("span_end"),
                            context=rel.get("context"),
                            extraction_method=rel.get("extraction_method"),
                            metadata_json=rel.get("metadata"),
                        )
                        db.add(relation_obj)
                        db.flush()
                        db.add(RelationResolution(relation_id=relation_obj.id, status="pending"))
                        subject_entity = next((e for e in entities if e.id == rel["subject_entity_id"]), None)
                        object_entity = next((e for e in entities if e.id == rel["object_entity_id"]), None)
                        if subject_entity and object_entity:
                            relations.append(
                                RelationModel(
                                    id=str(relation_obj.id),
                                    subject=subject_entity.text,
                                    subject_label=subject_entity.label,
                                    predicate=rel["predicate"],
                                    object=object_entity.text,
                                    object_label=object_entity.label,
                                    confidence=rel.get("confidence", 0.5),
                                    context=rel.get("context", ""),
                                )
                            )

                if request.generate_summary:
                    summary_text = summarize(request.text, request.language)

                db.commit()

                if self.graph_write_relations and relations:
                    background_tasks.add_task(self._write_relations_to_graph, doc_id, relations)

        if request.resolve_entities and entities:
            entity_ids = [ent.id for ent in entities if ent.id]
            if entity_ids:
                background_tasks.add_task(resolve_entities, entity_ids)

        resolution_counts = Counter(ent.resolution_status or "unknown" for ent in entities)
        score_values = [ent.resolution_score for ent in entities if ent.resolution_score is not None]

        html_content = self._highlight(request.text, entities)
        metadata_out = {
            "doc_id": doc_id,
            "extracted_entities": len(entities),
            "extracted_relations": len(relations),
            "has_summary": summary_text is not None,
            "language": request.language,
            "processing_timestamp": time.time(),
        }
        if resolution_counts:
            metadata_out["linking_status_counts"] = dict(resolution_counts)
            metadata_out["linking_resolved"] = resolution_counts.get("resolved", 0)
            metadata_out["linking_unmatched"] = resolution_counts.get("unmatched", 0)
            metadata_out["linking_pending"] = resolution_counts.get("pending", 0)
        if score_values:
            metadata_out["linking_mean_score"] = sum(score_values) / len(score_values)

        return DocumentAnnotationResponse(
            doc_id=doc_id,
            entities=entities,
            relations=relations,
            summary=summary_text,
            html_content=html_content,
            metadata=metadata_out,
        )

    def get_document(self, doc_id: str) -> DocumentModel:
        if self.allow_test:
            doc_info = self.mem_texts.get(doc_id)
            if not doc_info:
                raise APIError(
                    code=ErrorCodes.RESOURCE_NOT_FOUND,
                    message="Document not found",
                    status_code=404,
                    details={"doc_id": doc_id},
                )
            entities_data = self.mem_entities.get(doc_id, [])
            return DocumentModel(
                doc_id=doc_id,
                title=doc_info.get("title"),
                text=doc_info.get("text"),
                entities=[EntityModel(**ent) for ent in entities_data],
                relations=[],
                metadata=doc_info.get("metadata"),
            )

        with self.session_factory() as db:
            doc = db.get(Document, uuid.UUID(doc_id))
            if not doc:
                raise APIError(
                    code=ErrorCodes.RESOURCE_NOT_FOUND,
                    message="Document not found",
                    status_code=404,
                    details={"doc_id": doc_id},
                )
            entities: List[EntityModel] = []
            for ent in db.query(Entity).filter_by(doc_id=doc.id):
                resolution = db.get(EntityResolution, ent.id)
                entities.append(
                    EntityModel(
                        id=str(ent.id),
                        text=ent.value,
                        label=ent.label,
                        start=ent.span_start,
                        end=ent.span_end,
                        confidence=ent.confidence,
                        context=ent.context,
                        resolution_status=resolution.status if resolution else None,
                        resolution_score=resolution.score if resolution else None,
                        resolution_target=resolution.node_id if resolution else None,
                    )
                )
            relations = []
            for relation in db.query(Relation).filter_by(doc_id=doc.id):
                subject_entity = db.get(Entity, relation.subject_entity_id)
                object_entity = db.get(Entity, relation.object_entity_id)
                if subject_entity and object_entity:
                    relations.append(
                        RelationModel(
                            id=str(relation.id),
                            subject=subject_entity.value,
                            subject_label=subject_entity.label,
                            predicate=relation.predicate,
                            object=object_entity.value,
                            object_label=object_entity.label,
                            confidence=relation.confidence,
                            context=relation.context,
                        )
                    )
            resolution_counts = Counter(ent.resolution_status or "unknown" for ent in entities)
            metadata: Dict[str, Any] = {
                "source": getattr(doc, "source", None),
                "aleph_id": getattr(doc, "aleph_id", None),
                "linking_status_counts": dict(resolution_counts),
                "linking_resolved": resolution_counts.get("resolved", 0),
                "linking_unmatched": resolution_counts.get("unmatched", 0),
                "linking_pending": resolution_counts.get("pending", 0),
            }
            score_values = [ent.resolution_score for ent in entities if ent.resolution_score is not None]
            if score_values:
                metadata["linking_mean_score"] = sum(score_values) / len(score_values)

            return DocumentModel(
                doc_id=doc_id,
                title=doc.title,
                text=None,
                entities=entities,
                relations=relations,
                metadata=metadata,
                created_at=doc.created_at.isoformat() if getattr(doc, "created_at", None) else None,
            )

    def resolve_document_entities(
        self,
        doc_id: str,
        background_tasks: BackgroundTasks,
        force_resolution: bool = Query(False, description="Force re-resolution"),
    ) -> EntityResolutionResponse:
        if self.allow_test:
            if doc_id not in self.mem_entities:
                raise APIError(
                    code=ErrorCodes.RESOURCE_NOT_FOUND,
                    message="Document not found",
                    status_code=404,
                    details={"doc_id": doc_id},
                )
            entities_data = self.mem_entities[doc_id]
            entity_ids = [ent["id"] for ent in entities_data]
            if entity_ids:
                background_tasks.add_task(resolve_entities, entity_ids)
            return EntityResolutionResponse(
                resolved_entities=[
                    {"entity_id": ent_id, "status": "processing", "confidence": 0.85}
                    for ent_id in entity_ids
                ],
                resolution_metadata={
                    "doc_id": doc_id,
                    "entity_count": len(entity_ids),
                    "force_resolution": force_resolution,
                    "status": "started",
                },
            )

        with self.session_factory() as db:
            doc = db.get(Document, uuid.UUID(doc_id))
            if not doc:
                raise APIError(
                    code=ErrorCodes.RESOURCE_NOT_FOUND,
                    message="Document not found",
                    status_code=404,
                    details={"doc_id": doc_id},
                )
            entities = db.query(Entity).filter_by(doc_id=doc.id).all()
            entity_ids = [str(entity.id) for entity in entities]
            for entity in entities:
                resolution = db.get(EntityResolution, entity.id)
                if resolution:
                    if force_resolution or resolution.status == "pending":
                        resolution.status = "processing"
                else:
                    db.add(EntityResolution(entity_id=entity.id, status="processing"))
            db.commit()
            if entity_ids:
                background_tasks.add_task(resolve_entities, entity_ids)
            return EntityResolutionResponse(
                resolved_entities=[{"entity_id": ent_id, "status": "processing"} for ent_id in entity_ids],
                resolution_metadata={
                    "doc_id": doc_id,
                    "entity_count": len(entity_ids),
                    "force_resolution": force_resolution,
                    "status": "started",
                },
            )

    def fuzzy_match(self, request: FuzzyMatchRequest) -> FuzzyMatchResponse:
        start_time = time.time()
        results = FuzzyMatcher.match(
            MatchRequest(
                query=request.query,
                candidates=request.candidates,
                threshold=request.threshold,
                limit=request.limit,
                scorer=request.scorer,
            )
        )
        matches = [
            {"candidate": r.candidate, "score": r.score, "index": r.index}
            for r in results
        ]
        return FuzzyMatchResponse(
            query=request.query,
            matches=matches,
            total_candidates=len(request.candidates),
            processing_time_ms=int((time.time() - start_time) * 1000),
        )

    def fuzzy_dedupe(self, request: FuzzyDedupeRequest) -> FuzzyDedupeResponse:
        result = FuzzyMatcher.dedupe(
            DedupeRequest(strings=request.strings, threshold=request.threshold, scorer=request.scorer)
        )
        return FuzzyDedupeResponse(
            clusters=result.clusters,
            total_items=result.total_items,
            unique_clusters=result.unique_clusters,
            deduplication_ratio=result.deduplication_ratio,
            threshold=request.threshold,
            scorer=request.scorer,
        )


def build_doc_entities_router(service: DocEntitiesService) -> APIRouter:
    router = APIRouter(prefix="/v1", tags=["doc-entities"])

    router.post(
        "/extract/entities",
        response_model=NERResponse,
        summary="Extract named entities",
        description="Extract named entities from text using NLP models",
        tags=["nlp"],
    )(service.extract_entities)

    router.post(
        "/extract/relations",
        response_model=RelationExtractionResponse,
        summary="Extract relations",
        description="Extract relations between entities in text",
        tags=["nlp"],
    )(service.extract_text_relations)

    router.post(
        "/summarize",
        response_model=SummarizationResponse,
        summary="Summarize text",
        description="Generate text summaries using NLP models",
        tags=["nlp"],
    )(service.summarize_text)

    router.post(
        "/documents/annotate",
        response_model=DocumentAnnotationResponse,
        summary="Annotate document",
        description="Comprehensive document annotation with NLP processing",
        tags=["documents"],
    )(service.annotate_document)

    router.get(
        "/documents/{doc_id}",
        response_model=DocumentModel,
        summary="Get document",
        description="Retrieve document with annotations",
        tags=["documents"],
    )(service.get_document)

    router.post(
        "/documents/{doc_id}/resolve",
        response_model=EntityResolutionResponse,
        summary="Resolve document entities",
        description="Resolve all entities in a document against knowledge graph",
        tags=["documents"],
    )(service.resolve_document_entities)

    router.post(
        "/fuzzy/match",
        response_model=FuzzyMatchResponse,
        summary="Fuzzy string matching",
        description="Perform fuzzy string matching using advanced algorithms",
        tags=["nlp"],
    )(service.fuzzy_match)

    router.post(
        "/fuzzy/dedupe",
        response_model=FuzzyDedupeResponse,
        summary="Fuzzy deduplication",
        description="Deduplicate strings using fuzzy clustering",
        tags=["nlp"],
    )(service.fuzzy_dedupe)

    return router


__all__ = ["DocEntitiesService", "build_doc_entities_router"]
