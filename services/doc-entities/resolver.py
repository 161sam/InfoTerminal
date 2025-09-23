"""Enhanced entity resolver with fuzzy matching and alias linking."""

from __future__ import annotations

import os
import re
import time
import uuid
from collections import Counter
from typing import Any, Dict, Iterable, List, Optional, Tuple

from fuzzy_matcher import FuzzyMatcher

from metrics import (
    RESOLVER_CONFIDENCE,
    RESOLVER_LATENCY,
    RESOLVER_OUTCOMES,
    RESOLVER_RUNS,
)

# ---------------------------------------------------------------------------
# Alias / canonical knowledge base (demo friendly, extensible via env)
# ---------------------------------------------------------------------------

_ALIAS_KB: Dict[str, Dict[str, Any]] = {
    "person:barack-obama": {
        "type": "Person",
        "aliases": {
            "barack obama",
            "barack h obama",
            "president obama",
            "obama",
        },
        "name": "Barack Obama",
        "confidence": 0.94,
    },
    "person:donald-trump": {
        "type": "Person",
        "aliases": {"donald trump", "president trump", "trump"},
        "name": "Donald Trump",
        "confidence": 0.93,
    },
    "org:openai": {
        "type": "Organization",
        "aliases": {"openai", "openai lp", "openai inc"},
        "name": "OpenAI",
        "confidence": 0.91,
    },
    "org:microsoft": {
        "type": "Organization",
        "aliases": {"microsoft", "microsoft corp", "microsoft corporation"},
        "name": "Microsoft Corporation",
        "confidence": 0.9,
    },
    "location:berlin": {
        "type": "Location",
        "aliases": {"berlin", "berlin, germany"},
        "name": "Berlin",
        "confidence": 0.92,
    },
    "location:new-york-city": {
        "type": "Location",
        "aliases": {"new york", "new york city", "nyc"},
        "name": "New York City",
        "confidence": 0.92,
    },
}


def _normalise(value: Optional[str]) -> str:
    if not value:
        return ""
    cleaned = re.sub(r"[^\w\s]", " ", value.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def _alias_candidates(entity: Any) -> List[Dict[str, Any]]:
    """Return alias-based candidates for a given entity."""

    aliases: List[Dict[str, Any]] = []
    normalised_value = _normalise(getattr(entity, "value", ""))
    if not normalised_value:
        return aliases

    entity_type = _normalise(getattr(entity, "label", ""))
    for node_id, payload in _ALIAS_KB.items():
        kb_type = _normalise(payload.get("type"))
        if kb_type and entity_type and kb_type != entity_type:
            continue
        if normalised_value in payload.get("aliases", set()):
            aliases.append(
                {
                    "node_id": node_id,
                    "score": float(payload.get("confidence", 0.9)),
                    "name": payload.get("name"),
                    "type": payload.get("type"),
                    "source": "alias_match",
                    "fuzzy_match": False,
                    "match_value": normalised_value,
                }
            )

    return aliases


def resolve_entities(entity_ids: Iterable[str], mode: str = "async") -> List[Dict[str, Any]]:
    """Resolve a batch of entities and record observability metrics."""

    RESOLVER_RUNS.labels(mode=mode).inc()
    start = time.perf_counter()

    # Import here to avoid circular imports
    from db import SessionLocal
    from models import Entity, EntityResolution

    status_counter: Counter[str] = Counter()
    observed_scores: List[float] = []
    results: List[Dict[str, Any]] = []

    with SessionLocal() as db:
        for entity_id in entity_ids:
            try:
                status, score, payload = _resolve_single(db, Entity, EntityResolution, entity_id)
                status_counter[status] += 1
                if score is not None and status in {"resolved", "ambiguous"}:
                    observed_scores.append(score)
                if payload:
                    results.append(payload)
            except Exception as exc:  # pragma: no cover - defensive path
                print(f"Error resolving entity {entity_id}: {exc}")
                status_counter["error"] += 1
            finally:
                db.flush()

        db.commit()

    for status, count in status_counter.items():
        RESOLVER_OUTCOMES.labels(status=status).inc(count)
    for score in observed_scores:
        RESOLVER_CONFIDENCE.observe(score)
    RESOLVER_LATENCY.labels(mode=mode).observe(time.perf_counter() - start)

    return results


def _resolve_single(
    db,
    entity_model,
    resolution_model,
    entity_id: str,
) -> Tuple[str, Optional[float], Optional[Dict[str, Any]]]:
    """Internal helper that resolves a single entity inside an open session."""

    try:
        entity_uuid = uuid.UUID(entity_id)
    except ValueError:
        return "invalid_id", None, None

    entity = db.get(entity_model, entity_uuid)
    if not entity:
        return "missing", None, None

    resolution = db.get(resolution_model, entity.id)
    if not resolution:
        resolution = resolution_model(entity_id=entity.id, status="processing")
        db.add(resolution)
    else:
        resolution.status = "processing"

    candidates = _find_candidates(entity)
    status, best_score = _apply_resolution(resolution, candidates)

    payload = {
        "entity_id": str(entity.id),
        "status": resolution.status,
        "node_id": resolution.node_id,
        "score": resolution.score,
        "candidates": resolution.candidates or [],
    }

    return status, best_score, payload


def _apply_resolution(resolution: Any, candidates: List[Dict[str, Any]]) -> Tuple[str, Optional[float]]:
    """Apply resolver decision logic and update the SQLAlchemy model."""

    threshold = float(os.getenv("RESOLVE_CONFIDENCE_THRESHOLD", "0.7"))
    resolution.candidates = candidates[:5] if candidates else []

    if not candidates:
        resolution.node_id = None
        resolution.score = None
        resolution.status = "unmatched"
        return "unmatched", None

    best_candidate = max(candidates, key=lambda x: x.get("score", 0.0))
    best_score = float(best_candidate.get("score", 0.0)) if best_candidate else None

    if best_candidate and best_score is not None and best_score >= threshold:
        resolution.node_id = best_candidate.get("node_id")
        resolution.score = best_score
        resolution.status = "resolved"
        return "resolved", best_score

    resolution.node_id = None
    resolution.score = best_score
    resolution.status = "ambiguous"
    return "ambiguous", best_score


def _merge_candidates(*groups: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    merged: Dict[str, Dict[str, Any]] = {}
    for group in groups:
        for candidate in group:
            node_id = candidate.get("node_id")
            if not node_id:
                continue
            existing = merged.get(node_id)
            if existing is None or candidate.get("score", 0) > existing.get("score", 0):
                merged[node_id] = {**existing, **candidate} if existing else dict(candidate)
            elif existing is not None:
                # Merge metadata while keeping best score
                existing.update({k: v for k, v in candidate.items() if k not in existing})
    return list(merged.values())


def _find_candidates(entity: Any) -> List[Dict[str, Any]]:
    """Find potential matches for entity in knowledge graph with heuristics."""

    use_fuzzy_fallback = os.getenv("RESOLVE_FUZZY_FALLBACK", "1") == "1"
    entity_value = (entity.value or "").lower()
    label = (entity.label or "").upper()

    alias_matches = _alias_candidates(entity)
    heuristic_matches: List[Dict[str, Any]] = []

    if label == "PERSON":
        if "obama" in entity_value:
            heuristic_matches.append(
                {
                    "node_id": "person:barack-obama",
                    "score": 0.9,
                    "name": "Barack Obama",
                    "type": "Person",
                    "description": "44th President of the United States",
                    "source": "heuristic",
                }
            )
        elif "trump" in entity_value:
            heuristic_matches.append(
                {
                    "node_id": "person:donald-trump",
                    "score": 0.88,
                    "name": "Donald Trump",
                    "type": "Person",
                    "description": "45th and 47th President of the United States",
                    "source": "heuristic",
                }
            )
        elif any(name in entity_value for name in ["john", "jane", "smith", "doe"]):
            heuristic_matches.append(
                {
                    "node_id": f"person:{entity_value.replace(' ', '-')}",
                    "score": 0.6,
                    "name": entity.value,
                    "type": "Person",
                    "description": f"Person named {entity.value}",
                    "source": "heuristic",
                }
            )

    elif label in {"ORG", "ORGANIZATION"}:
        if "apple" in entity_value:
            heuristic_matches.append(
                {
                    "node_id": "org:apple-inc",
                    "score": 0.85,
                    "name": "Apple Inc.",
                    "type": "Organization",
                    "description": "Technology company",
                    "source": "heuristic",
                }
            )
        elif "google" in entity_value:
            heuristic_matches.append(
                {
                    "node_id": "org:google",
                    "score": 0.85,
                    "name": "Google LLC",
                    "type": "Organization",
                    "description": "Technology and internet company",
                    "source": "heuristic",
                }
            )
        elif "microsoft" in entity_value:
            heuristic_matches.append(
                {
                    "node_id": "org:microsoft",
                    "score": 0.88,
                    "name": "Microsoft Corporation",
                    "type": "Organization",
                    "description": "Technology company",
                    "source": "heuristic",
                }
            )
        elif any(org in entity_value for org in ["corp", "inc", "llc", "ltd", "company"]):
            heuristic_matches.append(
                {
                    "node_id": f"org:{entity_value.replace(' ', '-')}",
                    "score": 0.65,
                    "name": entity.value,
                    "type": "Organization",
                    "description": f"Organization: {entity.value}",
                    "source": "heuristic",
                }
            )

    elif label in {"GPE", "LOCATION", "LOC"}:
        if "new york" in entity_value or entity_value == "nyc":
            heuristic_matches.append(
                {
                    "node_id": "location:new-york-city",
                    "score": 0.9,
                    "name": "New York City",
                    "type": "Location",
                    "description": "Largest city in the United States",
                    "source": "heuristic",
                }
            )
        elif "london" in entity_value:
            heuristic_matches.append(
                {
                    "node_id": "location:london",
                    "score": 0.9,
                    "name": "London",
                    "type": "Location",
                    "description": "Capital city of the United Kingdom",
                    "source": "heuristic",
                }
            )
        elif "berlin" in entity_value:
            heuristic_matches.append(
                {
                    "node_id": "location:berlin",
                    "score": 0.9,
                    "name": "Berlin",
                    "type": "Location",
                    "description": "Capital city of Germany",
                    "source": "heuristic",
                }
            )
        elif "paris" in entity_value:
            heuristic_matches.append(
                {
                    "node_id": "location:paris",
                    "score": 0.9,
                    "name": "Paris",
                    "type": "Location",
                    "description": "Capital city of France",
                    "source": "heuristic",
                }
            )
        elif any(loc in entity_value for loc in ["city", "state", "country", "street", "avenue"]):
            heuristic_matches.append(
                {
                    "node_id": f"location:{entity_value.replace(' ', '-')}",
                    "score": 0.65,
                    "name": entity.value,
                    "type": "Location",
                    "description": f"Location: {entity.value}",
                    "source": "heuristic",
                }
            )

    elif label in {"MONEY", "PERCENT", "DATE"}:
        heuristic_matches.append(
            {
                "node_id": f"literal:{label.lower()}:{entity_value.replace(' ', '-')}",
                "score": 0.8,
                "name": entity.value,
                "type": "Literal",
                "description": f"{entity.label}: {entity.value}",
                "source": "heuristic",
            }
        )

    candidates = _merge_candidates(alias_matches, heuristic_matches)

    highest_score = max((cand.get("score", 0) for cand in candidates), default=0.0)
    if use_fuzzy_fallback and highest_score < 0.7:
        fuzzy_candidates = _fuzzy_resolve_fallback(entity)
        for fuzzy_candidate in fuzzy_candidates:
            fuzzy_candidate["fuzzy_match"] = True
            fuzzy_candidate.setdefault("source", "fuzzy_fallback")
        candidates = _merge_candidates(candidates, fuzzy_candidates)

    return candidates


def _fuzzy_resolve_fallback(entity: Any) -> List[Dict[str, Any]]:
    """Fuzzy matching fallback for entity resolution."""
    if not entity or not entity.value:
        return []
        
    # Mock knowledge base for fuzzy matching - in production this would be real KB
    mock_knowledge_base = [
        {"id": "person:barack-obama", "name": "Barack Obama", "type": "Person", "description": "44th President"},
        {"id": "person:donald-trump", "name": "Donald Trump", "type": "Person", "description": "45th President"}, 
        {"id": "org:apple-inc", "name": "Apple Inc", "type": "Organization", "description": "Technology company"},
        {"id": "org:microsoft", "name": "Microsoft Corporation", "type": "Organization", "description": "Tech company"},
        {"id": "org:google", "name": "Google LLC", "type": "Organization", "description": "Search company"},
        {"id": "loc:new-york", "name": "New York City", "type": "Location", "description": "Major US city"},
        {"id": "loc:london", "name": "London", "type": "Location", "description": "UK capital"},
        {"id": "loc:paris", "name": "Paris", "type": "Location", "description": "French capital"}
    ]
    
    try:
        # Filter knowledge base by entity type if possible
        filtered_kb = mock_knowledge_base
        if entity.label == "PERSON":
            filtered_kb = [kb for kb in mock_knowledge_base if kb["type"] == "Person"]
        elif entity.label in ["ORG", "ORGANIZATION"]: 
            filtered_kb = [kb for kb in mock_knowledge_base if kb["type"] == "Organization"]
        elif entity.label in ["GPE", "LOCATION", "LOC"]:
            filtered_kb = [kb for kb in mock_knowledge_base if kb["type"] == "Location"]
        
        # Use fuzzy matching to find candidates
        fuzzy_threshold = float(os.getenv("RESOLVE_FUZZY_THRESHOLD", "65.0"))
        fuzzy_results = FuzzyMatcher.fuzzy_resolve_entity(
            entity.value,
            filtered_kb, 
            scorer="WRatio",
            threshold=fuzzy_threshold
        )
        
        return fuzzy_results
        
    except Exception as e:
        print(f"Fuzzy fallback failed for entity {entity.value}: {e}")
        return []


def resolve_single_entity(entity_id: str) -> Optional[Dict[str, Any]]:
    """Resolve a single entity synchronously and return resolution info."""

    results = resolve_entities([entity_id], mode="sync")
    return results[0] if results else None
