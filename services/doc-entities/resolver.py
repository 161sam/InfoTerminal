"""Enhanced entity resolver with basic entity matching logic."""
import time
import uuid
from typing import Iterable, List, Dict, Any, Optional

from metrics import RESOLVER_RUNS, RESOLVER_ENTS, RESOLVER_LAT


def resolve_entities(entity_ids: Iterable[str], mode: str = "async") -> None:
    """Enhanced resolver with basic entity matching."""
    RESOLVER_RUNS.labels(mode=mode).inc()
    start = time.perf_counter()
    
    resolved_count = 0
    unmatched_count = 0
    
    # Import here to avoid circular imports
    from db import SessionLocal
    from models import Entity, EntityResolution
    
    with SessionLocal() as db:
        for entity_id in entity_ids:
            try:
                entity = db.get(Entity, uuid.UUID(entity_id))
                if not entity:
                    continue
                
                # Get or create resolution record
                resolution = db.get(EntityResolution, entity.id)
                if not resolution:
                    resolution = EntityResolution(entity_id=entity.id, status="processing")
                    db.add(resolution)
                else:
                    resolution.status = "processing"
                
                # Basic entity resolution logic
                candidates = _find_candidates(entity)
                
                if candidates:
                    best_candidate = max(candidates, key=lambda x: x.get('score', 0))
                    if best_candidate['score'] > 0.7:  # Confidence threshold
                        resolution.node_id = best_candidate['node_id']
                        resolution.score = best_candidate['score']
                        resolution.status = "resolved"
                        resolution.candidates = candidates[:5]  # Store top 5
                        resolved_count += 1
                    else:
                        resolution.status = "ambiguous"
                        resolution.candidates = candidates[:5]
                        unmatched_count += 1
                else:
                    resolution.status = "unmatched"
                    unmatched_count += 1
                    
            except Exception as e:
                # Log error but continue processing other entities
                print(f"Error resolving entity {entity_id}: {e}")
                if 'resolution' in locals():
                    resolution.status = "error"
                unmatched_count += 1
        
        db.commit()
    
    # Update metrics
    RESOLVER_ENTS.labels(status="resolved").inc(resolved_count)
    RESOLVER_ENTS.labels(status="unmatched").inc(unmatched_count)
    RESOLVER_LAT.observe(time.perf_counter() - start)


def _find_candidates(entity: Any) -> List[Dict[str, Any]]:
    """Find potential matches for entity in knowledge graph."""
    candidates = []
    
    # Simple heuristics for demo/testing
    entity_value = entity.value.lower() if entity.value else ""
    
    if entity.label == "PERSON":
        # Mock some person candidates
        if "obama" in entity_value:
            candidates.append({
                "node_id": "person:barack-obama",
                "score": 0.95,
                "name": "Barack Obama",
                "type": "Person",
                "description": "44th President of the United States"
            })
        elif "trump" in entity_value:
            candidates.append({
                "node_id": "person:donald-trump", 
                "score": 0.95,
                "name": "Donald Trump",
                "type": "Person",
                "description": "45th and 47th President of the United States"
            })
        elif any(name in entity_value for name in ["john", "jane", "smith", "doe"]):
            candidates.append({
                "node_id": f"person:{entity_value.replace(' ', '-')}",
                "score": 0.6,
                "name": entity.value,
                "type": "Person",
                "description": f"Person named {entity.value}"
            })
    
    elif entity.label in ["ORG", "ORGANIZATION"]:
        # Mock some organization candidates
        if "apple" in entity_value:
            candidates.append({
                "node_id": "org:apple-inc",
                "score": 0.9,
                "name": "Apple Inc.",
                "type": "Organization",
                "description": "Technology company"
            })
        elif "google" in entity_value:
            candidates.append({
                "node_id": "org:google",
                "score": 0.9,
                "name": "Google LLC",
                "type": "Organization", 
                "description": "Technology and internet company"
            })
        elif "microsoft" in entity_value:
            candidates.append({
                "node_id": "org:microsoft",
                "score": 0.9,
                "name": "Microsoft Corporation",
                "type": "Organization",
                "description": "Technology company"
            })
        elif any(org in entity_value for org in ["corp", "inc", "llc", "ltd", "company"]):
            candidates.append({
                "node_id": f"org:{entity_value.replace(' ', '-')}",
                "score": 0.7,
                "name": entity.value,
                "type": "Organization",
                "description": f"Organization: {entity.value}"
            })
    
    elif entity.label in ["GPE", "LOCATION"]:
        # Mock some location candidates
        if "new york" in entity_value:
            candidates.append({
                "node_id": "location:new-york-city",
                "score": 0.95,
                "name": "New York City",
                "type": "Location",
                "description": "Largest city in the United States"
            })
        elif "london" in entity_value:
            candidates.append({
                "node_id": "location:london",
                "score": 0.95,
                "name": "London",
                "type": "Location",
                "description": "Capital city of the United Kingdom"
            })
        elif "berlin" in entity_value:
            candidates.append({
                "node_id": "location:berlin",
                "score": 0.95,
                "name": "Berlin",
                "type": "Location",
                "description": "Capital city of Germany"
            })
        elif "paris" in entity_value:
            candidates.append({
                "node_id": "location:paris",
                "score": 0.95,
                "name": "Paris",
                "type": "Location",
                "description": "Capital city of France"
            })
        elif any(loc in entity_value for loc in ["city", "state", "country", "street", "avenue"]):
            candidates.append({
                "node_id": f"location:{entity_value.replace(' ', '-')}",
                "score": 0.7,
                "name": entity.value,
                "type": "Location",
                "description": f"Location: {entity.value}"
            })
    
    elif entity.label in ["MONEY", "PERCENT", "DATE"]:
        # These entities typically don't need resolution to external knowledge graphs
        candidates.append({
            "node_id": f"literal:{entity.label.lower()}:{entity_value.replace(' ', '-')}",
            "score": 0.8,
            "name": entity.value,
            "type": "Literal",
            "description": f"{entity.label}: {entity.value}"
        })
    
    return candidates


def resolve_single_entity(entity_id: str) -> Optional[Dict[str, Any]]:
    """Resolve a single entity synchronously and return resolution info."""
    from db import SessionLocal
    from models import Entity, EntityResolution
    
    with SessionLocal() as db:
        entity = db.get(Entity, uuid.UUID(entity_id))
        if not entity:
            return None
            
        # Get or create resolution record
        resolution = db.get(EntityResolution, entity.id)
        if not resolution:
            resolution = EntityResolution(entity_id=entity.id, status="processing")
            db.add(resolution)
        else:
            resolution.status = "processing"
        
        db.commit()  # Commit status change
        
        try:
            candidates = _find_candidates(entity)
            
            if candidates:
                best_candidate = max(candidates, key=lambda x: x.get('score', 0))
                if best_candidate['score'] > 0.7:
                    resolution.node_id = best_candidate['node_id']
                    resolution.score = best_candidate['score']
                    resolution.status = "resolved"
                    resolution.candidates = candidates[:5]
                else:
                    resolution.status = "ambiguous"
                    resolution.candidates = candidates[:5]
            else:
                resolution.status = "unmatched"
                
            db.commit()
            
            return {
                "entity_id": entity_id,
                "status": resolution.status,
                "node_id": resolution.node_id,
                "score": resolution.score,
                "candidates": resolution.candidates or []
            }
            
        except Exception as e:
            print(f"Error resolving entity {entity_id}: {e}")
            resolution.status = "error"
            db.commit()
            return {
                "entity_id": entity_id,
                "status": "error",
                "error": str(e)
            }
