"""
Fuzzy string matching module integrated from entity-resolution service.
Provides RapidFuzz-based string matching and deduplication capabilities.
"""

from typing import List, Dict, Any, Tuple, Optional
from rapidfuzz import process, fuzz
from pydantic import BaseModel


class MatchRequest(BaseModel):
    """Request model for fuzzy string matching."""
    query: str
    candidates: List[str]
    limit: int = 5
    scorer: str = "token_sort_ratio"  # or "partial_ratio", "ratio", "token_set_ratio"


class MatchResult(BaseModel):
    """Result model for fuzzy string matching."""
    candidate: str
    score: float
    index: Optional[int] = None


class DedupeRequest(BaseModel):
    """Request model for string deduplication."""
    items: List[str]
    threshold: float = 90.0
    scorer: str = "token_sort_ratio"


class DedupeResult(BaseModel):
    """Result model for string deduplication."""
    clusters: List[List[str]]
    total_items: int
    unique_clusters: int
    deduplication_ratio: float


class FuzzyMatcher:
    """Enhanced fuzzy string matcher with multiple scoring algorithms."""
    
    SCORERS = {
        "ratio": fuzz.ratio,
        "partial_ratio": fuzz.partial_ratio,
        "token_sort_ratio": fuzz.token_sort_ratio,
        "token_set_ratio": fuzz.token_set_ratio,
        "WRatio": fuzz.WRatio,  # Weighted ratio (best general-purpose)
        "QRatio": fuzz.QRatio   # Quick ratio (fastest)
    }
    
    @classmethod
    def match(cls, req: MatchRequest) -> List[MatchResult]:
        """
        Perform fuzzy string matching against a list of candidates.
        
        Args:
            req: Match request with query, candidates, limit, and scorer
            
        Returns:
            List of match results sorted by score (descending)
        """
        scorer = cls.SCORERS.get(req.scorer, fuzz.token_sort_ratio)
        
        # Use process.extract for efficient matching
        matches = process.extract(
            req.query, 
            req.candidates, 
            scorer=scorer, 
            limit=req.limit
        )
        
        # Convert to MatchResult objects
        results = []
        for candidate, score, index in matches:
            results.append(MatchResult(
                candidate=candidate,
                score=float(score),
                index=index
            ))
        
        return results
    
    @classmethod
    def dedupe(cls, req: DedupeRequest) -> DedupeResult:
        """
        Deduplicate a list of strings using fuzzy clustering.
        
        Args:
            req: Deduplication request with items, threshold, and scorer
            
        Returns:
            Deduplication result with clustered groups
        """
        scorer = cls.SCORERS.get(req.scorer, fuzz.token_sort_ratio)
        clusters: List[List[str]] = []
        visited = set()
        
        for i, item_x in enumerate(req.items):
            if i in visited:
                continue
                
            # Start new cluster with current item
            cluster = [item_x]
            visited.add(i)
            
            # Find similar items for this cluster
            for j, item_y in enumerate(req.items[i+1:], start=i+1):
                if j in visited:
                    continue
                    
                similarity_score = scorer(item_x, item_y)
                if similarity_score >= req.threshold:
                    cluster.append(item_y)
                    visited.add(j)
            
            clusters.append(cluster)
        
        # Calculate deduplication statistics
        total_items = len(req.items)
        unique_clusters = len(clusters)
        deduplication_ratio = (total_items - unique_clusters) / total_items if total_items > 0 else 0.0
        
        return DedupeResult(
            clusters=clusters,
            total_items=total_items,
            unique_clusters=unique_clusters,
            deduplication_ratio=deduplication_ratio
        )
    
    @classmethod
    def find_best_match(
        cls, 
        query: str, 
        candidates: List[str], 
        scorer: str = "token_sort_ratio",
        threshold: float = 60.0
    ) -> Optional[MatchResult]:
        """
        Find the single best match above a threshold.
        
        Args:
            query: String to match
            candidates: List of candidate strings
            scorer: Scoring algorithm to use
            threshold: Minimum score threshold
            
        Returns:
            Best match result or None if below threshold
        """
        if not candidates:
            return None
            
        req = MatchRequest(
            query=query,
            candidates=candidates,
            limit=1,
            scorer=scorer
        )
        
        matches = cls.match(req)
        if matches and matches[0].score >= threshold:
            return matches[0]
            
        return None
    
    @classmethod
    def fuzzy_resolve_entity(
        cls,
        entity_value: str,
        knowledge_base: List[Dict[str, Any]],
        scorer: str = "WRatio",
        threshold: float = 70.0
    ) -> List[Dict[str, Any]]:
        """
        Resolve entity against knowledge base using fuzzy matching.
        
        Args:
            entity_value: Entity value to resolve
            knowledge_base: List of knowledge base entries with 'name' field
            scorer: Scoring algorithm to use  
            threshold: Minimum confidence threshold
            
        Returns:
            List of potential matches with scores
        """
        if not knowledge_base:
            return []
        
        # Extract names from knowledge base
        kb_names = [entry.get("name", "") for entry in knowledge_base]
        
        # Perform fuzzy matching
        req = MatchRequest(
            query=entity_value,
            candidates=kb_names,
            limit=10,
            scorer=scorer
        )
        
        matches = cls.match(req)
        
        # Build resolution results
        results = []
        for match in matches:
            if match.score >= threshold:
                # Find the original KB entry
                original_entry = knowledge_base[match.index] if match.index is not None else {}
                
                result = {
                    "node_id": original_entry.get("id", f"fuzzy:{entity_value.replace(' ', '-')}"),
                    "score": match.score / 100.0,  # Normalize to 0-1
                    "name": match.candidate,
                    "type": original_entry.get("type", "Unknown"),
                    "description": original_entry.get("description", ""),
                    "fuzzy_match": True,
                    "original_query": entity_value
                }
                results.append(result)
        
        return results


class EntityDeduplicator:
    """Specialized deduplicator for entity lists."""
    
    @classmethod
    def dedupe_entities(
        cls,
        entities: List[Dict[str, Any]],
        threshold: float = 85.0,
        key_field: str = "value"
    ) -> Dict[str, Any]:
        """
        Deduplicate entity list based on entity values.
        
        Args:
            entities: List of entity dictionaries
            threshold: Similarity threshold for clustering
            key_field: Field to use for comparison
            
        Returns:
            Deduplication result with original entity references
        """
        if not entities:
            return {
                "clusters": [],
                "deduplicated_entities": [],
                "total_original": 0,
                "total_deduplicated": 0,
                "deduplication_ratio": 0.0
            }
        
        # Extract values for deduplication
        values = [entity.get(key_field, "") for entity in entities]
        
        # Perform deduplication
        req = DedupeRequest(items=values, threshold=threshold)
        dedupe_result = FuzzyMatcher.dedupe(req)
        
        # Map clusters back to original entities
        entity_clusters = []
        deduplicated_entities = []
        
        for cluster in dedupe_result.clusters:
            if not cluster:
                continue
                
            # Find entities for this cluster
            cluster_entities = []
            for value in cluster:
                for i, entity in enumerate(entities):
                    if entity.get(key_field, "") == value:
                        cluster_entities.append(entity)
                        break
            
            entity_clusters.append(cluster_entities)
            
            # Use first entity as representative
            if cluster_entities:
                representative = cluster_entities[0].copy()
                representative["cluster_size"] = len(cluster_entities)
                representative["variants"] = [e.get(key_field, "") for e in cluster_entities[1:]]
                deduplicated_entities.append(representative)
        
        return {
            "clusters": entity_clusters,
            "deduplicated_entities": deduplicated_entities,
            "total_original": len(entities),
            "total_deduplicated": len(deduplicated_entities),
            "deduplication_ratio": (len(entities) - len(deduplicated_entities)) / len(entities)
        }


# Convenience functions for backward compatibility
def fuzzy_match(query: str, candidates: List[str], **kwargs) -> List[Dict[str, Any]]:
    """Backward compatible fuzzy matching function."""
    req = MatchRequest(query=query, candidates=candidates, **kwargs)
    results = FuzzyMatcher.match(req)
    return [{"candidate": r.candidate, "score": r.score} for r in results]


def fuzzy_dedupe(items: List[str], **kwargs) -> Dict[str, Any]:
    """Backward compatible deduplication function."""
    req = DedupeRequest(items=items, **kwargs)
    result = FuzzyMatcher.dedupe(req)
    return {
        "clusters": result.clusters,
        "total_items": result.total_items,
        "unique_clusters": result.unique_clusters,
        "deduplication_ratio": result.deduplication_ratio
    }
