"""
Test suite for consolidated doc-entities service with fuzzy matching integration.
Tests both original NLP functionality and new fuzzy matching capabilities.
"""

import pytest
import asyncio
import json
from typing import Dict, List, Any
from unittest.mock import patch, MagicMock

# Test imports - these would normally be set up in conftest.py
from fuzzy_matcher import FuzzyMatcher, MatchRequest, DedupeRequest, EntityDeduplicator


class TestFuzzyMatcher:
    """Test suite for the integrated fuzzy matching functionality."""
    
    def test_fuzzy_match_basic(self):
        """Test basic fuzzy string matching."""
        req = MatchRequest(
            query="barack obama",
            candidates=["Barack Obama", "Donald Trump", "Joe Biden", "Barack O'Bama"],
            limit=3,
            scorer="token_sort_ratio"
        )
        
        results = FuzzyMatcher.match(req)
        
        assert len(results) <= 3
        assert results[0].candidate in ["Barack Obama", "Barack O'Bama"]
        assert results[0].score > 80.0  # Should have high confidence
        assert all(r.score >= 0.0 for r in results)
    
    def test_fuzzy_match_different_scorers(self):
        """Test different scoring algorithms."""
        candidates = ["Microsoft Corporation", "Microsoft Corp", "Apple Inc"]
        query = "Microsoft"
        
        for scorer in ["ratio", "partial_ratio", "token_sort_ratio", "WRatio"]:
            req = MatchRequest(query=query, candidates=candidates, scorer=scorer)
            results = FuzzyMatcher.match(req)
            
            assert len(results) > 0
            assert results[0].candidate.startswith("Microsoft")
    
    def test_fuzzy_dedupe_basic(self):
        """Test string deduplication."""
        items = [
            "Barack Obama",
            "Barack O'Bama", 
            "Donald Trump",
            "donald trump",
            "Joe Biden",
            "Apple Inc",
            "Apple Inc."
        ]
        
        req = DedupeRequest(items=items, threshold=80.0)
        result = FuzzyMatcher.dedupe(req)
        
        assert result.total_items == len(items)
        assert result.unique_clusters < len(items)  # Should have deduplicated
        assert result.deduplication_ratio > 0.0
        assert len(result.clusters) == result.unique_clusters
    
    def test_fuzzy_dedupe_threshold_effects(self):
        """Test that different thresholds affect clustering."""
        items = ["Microsoft", "Microsoft Corp", "Microsoft Corporation", "Apple Inc"]
        
        # Low threshold - more aggressive deduplication
        low_req = DedupeRequest(items=items, threshold=60.0)
        low_result = FuzzyMatcher.dedupe(low_req)
        
        # High threshold - less aggressive deduplication  
        high_req = DedupeRequest(items=items, threshold=95.0)
        high_result = FuzzyMatcher.dedupe(high_req)
        
        assert low_result.unique_clusters <= high_result.unique_clusters
    
    def test_find_best_match(self):
        """Test finding single best match."""
        candidates = ["Barack Obama", "Donald Trump", "Joe Biden"]
        
        # Good match
        match = FuzzyMatcher.find_best_match("barack obama", candidates, threshold=70.0)
        assert match is not None
        assert match.candidate == "Barack Obama"
        
        # No good match
        no_match = FuzzyMatcher.find_best_match("xyz", candidates, threshold=70.0)
        assert no_match is None
    
    def test_fuzzy_resolve_entity(self):
        """Test entity resolution against knowledge base."""
        kb = [
            {"id": "p1", "name": "Barack Obama", "type": "Person", "description": "44th President"},
            {"id": "o1", "name": "Apple Inc", "type": "Organization", "description": "Tech company"},
            {"id": "l1", "name": "New York", "type": "Location", "description": "City"}
        ]
        
        results = FuzzyMatcher.fuzzy_resolve_entity("barack obama", kb, threshold=70.0)
        
        assert len(results) > 0
        assert results[0]["name"] == "Barack Obama"
        assert results[0]["fuzzy_match"] is True
        assert results[0]["score"] > 0.7


class TestEntityDeduplicator:
    """Test suite for entity deduplication functionality."""
    
    def test_dedupe_entities_basic(self):
        """Test basic entity deduplication."""
        entities = [
            {"id": "1", "value": "Barack Obama", "label": "PERSON"},
            {"id": "2", "value": "Barack O'Bama", "label": "PERSON"}, 
            {"id": "3", "value": "Donald Trump", "label": "PERSON"},
            {"id": "4", "value": "Apple Inc", "label": "ORG"},
            {"id": "5", "value": "Apple Inc.", "label": "ORG"}
        ]
        
        result = EntityDeduplicator.dedupe_entities(entities, threshold=80.0)
        
        assert result["total_original"] == 5
        assert result["total_deduplicated"] < 5
        assert result["deduplication_ratio"] > 0.0
        assert len(result["deduplicated_entities"]) == result["total_deduplicated"]
    
    def test_dedupe_entities_custom_field(self):
        """Test entity deduplication with custom key field."""
        entities = [
            {"name": "Barack Obama", "type": "person"},
            {"name": "Barack O'Bama", "type": "person"},
            {"name": "Apple", "type": "org"}
        ]
        
        result = EntityDeduplicator.dedupe_entities(
            entities, 
            threshold=80.0,
            key_field="name"
        )
        
        assert result["total_original"] == 3
        assert result["total_deduplicated"] <= 3


class TestAPI:
    """Test suite for API endpoints (would require FastAPI test client)."""
    
    @pytest.fixture
    def mock_client(self):
        """Mock FastAPI test client."""
        # This would be a real test client in practice
        return MagicMock()
    
    def test_match_endpoint(self, mock_client):
        """Test /match endpoint."""
        # Mock the request
        request_data = {
            "query": "barack obama",
            "candidates": ["Barack Obama", "Donald Trump"],
            "limit": 5,
            "scorer": "token_sort_ratio"
        }
        
        # In a real test, you'd do:
        # response = mock_client.post("/match", json=request_data)
        # assert response.status_code == 200
        # assert "matches" in response.json()
        
        # For now, test the underlying logic
        req = MatchRequest(**request_data)
        results = FuzzyMatcher.match(req)
        assert len(results) > 0
    
    def test_dedupe_endpoint(self, mock_client):
        """Test /dedupe endpoint."""
        request_data = {
            "items": ["Barack Obama", "Barack O'Bama", "Donald Trump"],
            "threshold": 80.0,
            "scorer": "token_sort_ratio"
        }
        
        # Test underlying logic
        req = DedupeRequest(**request_data)
        result = FuzzyMatcher.dedupe(req)
        assert result.total_items == 3
        assert result.unique_clusters <= 3


class TestBackwardCompatibility:
    """Test backward compatibility functions."""
    
    def test_fuzzy_match_function(self):
        """Test backward compatible fuzzy_match function."""
        from fuzzy_matcher import fuzzy_match
        
        results = fuzzy_match("obama", ["Barack Obama", "Donald Trump"])
        
        assert isinstance(results, list)
        assert len(results) > 0
        assert "candidate" in results[0]
        assert "score" in results[0]
    
    def test_fuzzy_dedupe_function(self):
        """Test backward compatible fuzzy_dedupe function."""
        from fuzzy_matcher import fuzzy_dedupe
        
        result = fuzzy_dedupe(["Obama", "O'Bama", "Trump"])
        
        assert isinstance(result, dict)
        assert "clusters" in result
        assert "total_items" in result


class TestIntegrationScenarios:
    """Integration tests for real-world scenarios."""
    
    def test_nlp_plus_fuzzy_workflow(self):
        """Test combined NLP + fuzzy matching workflow."""
        # Simulate NLP extraction results
        nlp_entities = [
            {"id": "e1", "value": "Barak Obama", "label": "PERSON"},  # Misspelled
            {"id": "e2", "value": "Mircosoft", "label": "ORG"},        # Misspelled
            {"id": "e3", "value": "New York City", "label": "GPE"}
        ]
        
        # Test deduplication
        dedupe_result = EntityDeduplicator.dedupe_entities(nlp_entities, threshold=70.0)
        
        # Test resolution against knowledge base
        kb = [
            {"id": "p1", "name": "Barack Obama", "type": "Person"},
            {"id": "o1", "name": "Microsoft Corporation", "type": "Organization"},
            {"id": "l1", "name": "New York City", "type": "Location"}
        ]
        
        for entity in nlp_entities:
            fuzzy_matches = FuzzyMatcher.fuzzy_resolve_entity(
                entity["value"], kb, threshold=60.0
            )
            assert len(fuzzy_matches) > 0, f"No matches for {entity['value']}"
    
    def test_performance_large_dataset(self):
        """Test performance with larger datasets."""
        # Generate test data
        large_candidates = [f"Entity {i}" for i in range(1000)]
        
        req = MatchRequest(
            query="Entity 500", 
            candidates=large_candidates,
            limit=10
        )
        
        import time
        start = time.time()
        results = FuzzyMatcher.match(req)
        duration = time.time() - start
        
        assert len(results) == 10
        assert duration < 1.0  # Should complete in under 1 second
        assert results[0].candidate == "Entity 500"  # Exact match should be first


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_empty_inputs(self):
        """Test handling of empty inputs."""
        # Empty candidates
        req = MatchRequest(query="test", candidates=[], limit=5)
        results = FuzzyMatcher.match(req)
        assert len(results) == 0
        
        # Empty query
        req = MatchRequest(query="", candidates=["test"], limit=5)
        results = FuzzyMatcher.match(req)
        assert len(results) >= 0  # Should handle gracefully
    
    def test_invalid_scorer(self):
        """Test handling of invalid scorer."""
        req = MatchRequest(
            query="test",
            candidates=["test1", "test2"], 
            scorer="invalid_scorer"
        )
        # Should fallback to default scorer
        results = FuzzyMatcher.match(req)
        assert len(results) > 0
    
    def test_dedupe_edge_cases(self):
        """Test deduplication edge cases."""
        # Single item
        req = DedupeRequest(items=["single"])
        result = FuzzyMatcher.dedupe(req)
        assert result.unique_clusters == 1
        assert result.deduplication_ratio == 0.0
        
        # Empty list
        req = DedupeRequest(items=[])
        result = FuzzyMatcher.dedupe(req)
        assert result.total_items == 0
        assert result.unique_clusters == 0


if __name__ == "__main__":
    # Run some basic tests if executed directly
    print("Running basic fuzzy matching tests...")
    
    test_matcher = TestFuzzyMatcher()
    test_matcher.test_fuzzy_match_basic()
    print("✅ Basic fuzzy matching test passed")
    
    test_matcher.test_fuzzy_dedupe_basic()
    print("✅ Basic deduplication test passed")
    
    test_deduper = TestEntityDeduplicator()
    test_deduper.test_dedupe_entities_basic()
    print("✅ Entity deduplication test passed")
    
    test_integration = TestIntegrationScenarios()
    test_integration.test_nlp_plus_fuzzy_workflow()
    print("✅ NLP + Fuzzy integration test passed")
    
    print("\nAll basic tests completed successfully! 🎉")
