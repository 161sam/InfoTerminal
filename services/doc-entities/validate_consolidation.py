#!/usr/bin/env python3
"""
Validation script for consolidated doc-entities service.
Tests all functionality to ensure no features were lost during consolidation.
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class ServiceValidator:
    """Comprehensive validation for the consolidated doc-entities service."""
    
    def __init__(self, base_url: str = "http://localhost:8613"):
        """Initialize validator with service URL."""
        self.base_url = base_url.rstrip("/")
        self.session = self._create_session()
        self.test_results = []
        
    def _create_session(self) -> requests.Session:
        """Create HTTP session with retry configuration."""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
    
    def log_test(self, name: str, passed: bool, message: str = ""):
        """Log test result."""
        status = "✅" if passed else "❌"
        full_message = f"{status} {name}"
        if message:
            full_message += f": {message}"
        print(full_message)
        
        self.test_results.append({
            "name": name,
            "passed": passed,
            "message": message,
            "timestamp": time.time()
        })
    
    def test_health_endpoints(self) -> bool:
        """Test basic health endpoints."""
        try:
            # Test healthz
            response = self.session.get(f"{self.base_url}/healthz", timeout=5)
            health_ok = response.status_code == 200 and response.json().get("status") == "ok"
            self.log_test("Health endpoint", health_ok, f"Status: {response.status_code}")
            
            # Test readyz
            response = self.session.get(f"{self.base_url}/readyz", timeout=5)
            ready_ok = response.status_code == 200 and response.json().get("ok") is True
            self.log_test("Ready endpoint", ready_ok, f"Status: {response.status_code}")
            
            return health_ok and ready_ok
            
        except Exception as e:
            self.log_test("Health endpoints", False, f"Error: {e}")
            return False
    
    def test_nlp_endpoints(self) -> bool:
        """Test original NLP functionality."""
        test_text = "Barack Obama worked at Apple Inc. in New York City. He earned $100,000 annually."
        all_passed = True
        
        # Test NER endpoint
        try:
            response = self.session.post(
                f"{self.base_url}/ner",
                json={"text": test_text, "lang": "en"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                entities = data.get("entities", [])
                has_entities = len(entities) > 0
                has_person = any(e.get("label") == "PERSON" for e in entities)
                
                self.log_test(
                    "NER endpoint", 
                    has_entities and has_person,
                    f"Found {len(entities)} entities"
                )
            else:
                self.log_test("NER endpoint", False, f"HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("NER endpoint", False, f"Error: {e}")
            all_passed = False
        
        # Test Summary endpoint
        try:
            response = self.session.post(
                f"{self.base_url}/summary",
                json={"text": test_text, "lang": "en"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                has_summary = "summary" in data and data["summary"]
                self.log_test("Summary endpoint", has_summary)
            else:
                self.log_test("Summary endpoint", False, f"HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("Summary endpoint", False, f"Error: {e}")
            all_passed = False
        
        # Test Relations endpoint
        try:
            response = self.session.post(
                f"{self.base_url}/relations",
                json={"text": test_text, "lang": "en", "extract_new": True},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                has_relations = "relations" in data
                self.log_test("Relations endpoint", has_relations, 
                            f"Found {len(data.get('relations', []))} relations")
            else:
                self.log_test("Relations endpoint", False, f"HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("Relations endpoint", False, f"Error: {e}")
            all_passed = False
        
        return all_passed
    
    def test_fuzzy_endpoints(self) -> bool:
        """Test new fuzzy matching functionality."""
        all_passed = True
        
        # Test Match endpoint
        try:
            test_data = {
                "query": "barack obama",
                "candidates": ["Barack Obama", "Donald Trump", "Joe Biden", "Barack O'Bama"],
                "limit": 3,
                "scorer": "token_sort_ratio"
            }
            
            response = self.session.post(
                f"{self.base_url}/match",
                json=test_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get("matches", [])
                has_matches = len(matches) > 0
                good_score = matches[0].get("score", 0) > 80 if matches else False
                
                self.log_test(
                    "Fuzzy Match endpoint",
                    has_matches and good_score,
                    f"Best match: {matches[0].get('candidate')} ({matches[0].get('score'):.1f})" if matches else "No matches"
                )
            else:
                self.log_test("Fuzzy Match endpoint", False, f"HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("Fuzzy Match endpoint", False, f"Error: {e}")
            all_passed = False
        
        # Test Dedupe endpoint
        try:
            test_data = {
                "items": ["Barack Obama", "Barack O'Bama", "Donald Trump", "donald trump", "Joe Biden"],
                "threshold": 80.0,
                "scorer": "token_sort_ratio"
            }
            
            response = self.session.post(
                f"{self.base_url}/dedupe",
                json=test_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                clusters = data.get("clusters", [])
                total_items = data.get("total_items", 0)
                unique_clusters = data.get("unique_clusters", 0)
                dedupe_ratio = data.get("deduplication_ratio", 0)
                
                deduped = unique_clusters < total_items
                self.log_test(
                    "Fuzzy Dedupe endpoint",
                    deduped,
                    f"Reduced {total_items} to {unique_clusters} clusters ({dedupe_ratio:.1%} reduction)"
                )
            else:
                self.log_test("Fuzzy Dedupe endpoint", False, f"HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("Fuzzy Dedupe endpoint", False, f"Error: {e}")
            all_passed = False
        
        # Test Entity Dedupe endpoint
        try:
            test_entities = [
                {"id": "1", "value": "Barack Obama", "label": "PERSON"},
                {"id": "2", "value": "Barack O'Bama", "label": "PERSON"},
                {"id": "3", "value": "Apple Inc", "label": "ORG"},
                {"id": "4", "value": "Apple Inc.", "label": "ORG"}
            ]
            
            response = self.session.post(
                f"{self.base_url}/entities/dedupe",
                json=test_entities,
                params={"threshold": 80.0},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                total_orig = data.get("total_original", 0)
                total_deduped = data.get("total_deduplicated", 0)
                
                entity_deduped = total_deduped < total_orig
                self.log_test(
                    "Entity Dedupe endpoint",
                    entity_deduped,
                    f"Reduced {total_orig} to {total_deduped} entities"
                )
            else:
                self.log_test("Entity Dedupe endpoint", False, f"HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("Entity Dedupe endpoint", False, f"Error: {e}")
            all_passed = False
        
        return all_passed
    
    def test_enhanced_workflow(self) -> bool:
        """Test combined NLP + Fuzzy matching workflow."""
        try:
            # Use annotate endpoint which combines multiple features
            test_text = "Barak Obama worked at Mircosoft in New York."  # Intentional typos
            
            response = self.session.post(
                f"{self.base_url}/annotate",
                json={
                    "text": test_text,
                    "lang": "en",
                    "title": "Test Document",
                    "extract_relations": True,
                    "do_summary": True
                },
                timeout=20
            )
            
            if response.status_code == 200:
                data = response.json()
                has_entities = len(data.get("entities", [])) > 0
                has_relations = len(data.get("relations", [])) > 0
                has_html = "html" in data and data["html"]
                has_doc_id = "doc_id" in data
                
                workflow_ok = has_entities and has_html and has_doc_id
                self.log_test(
                    "Enhanced NLP workflow",
                    workflow_ok,
                    f"Entities: {len(data.get('entities', []))}, Relations: {len(data.get('relations', []))}"
                )
                
                return workflow_ok
            else:
                self.log_test("Enhanced NLP workflow", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Enhanced NLP workflow", False, f"Error: {e}")
            return False
    
    def test_performance(self) -> bool:
        """Test performance characteristics."""
        all_passed = True
        
        # Test NLP performance
        test_text = "Barack Obama, the 44th President of the United States, worked at various organizations before entering politics. He was born in Hawaii and studied at Harvard Law School."
        
        try:
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/annotate",
                json={"text": test_text, "lang": "en"},
                timeout=30
            )
            nlp_duration = time.time() - start_time
            
            nlp_fast_enough = nlp_duration < 5.0  # Should complete in under 5 seconds
            self.log_test(
                "NLP Performance",
                nlp_fast_enough,
                f"{nlp_duration:.2f}s (target: <5s)"
            )
            all_passed &= nlp_fast_enough
            
        except Exception as e:
            self.log_test("NLP Performance", False, f"Error: {e}")
            all_passed = False
        
        # Test fuzzy matching performance
        large_candidates = [f"Entity {i}" for i in range(1000)]
        
        try:
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/match",
                json={
                    "query": "Entity 500",
                    "candidates": large_candidates,
                    "limit": 10
                },
                timeout=10
            )
            fuzzy_duration = time.time() - start_time
            
            fuzzy_fast_enough = fuzzy_duration < 1.0  # Should complete in under 1 second
            self.log_test(
                "Fuzzy Performance",
                fuzzy_fast_enough,
                f"{fuzzy_duration:.2f}s for 1000 candidates (target: <1s)"
            )
            all_passed &= fuzzy_fast_enough
            
        except Exception as e:
            self.log_test("Fuzzy Performance", False, f"Error: {e}")
            all_passed = False
        
        return all_passed
    
    def test_error_handling(self) -> bool:
        """Test error handling and edge cases."""
        all_passed = True
        
        # Test empty inputs
        try:
            response = self.session.post(
                f"{self.base_url}/match",
                json={"query": "test", "candidates": []},
                timeout=5
            )
            empty_handled = response.status_code == 200
            self.log_test("Empty candidates handling", empty_handled)
            all_passed &= empty_handled
            
        except Exception as e:
            self.log_test("Empty candidates handling", False, f"Error: {e}")
            all_passed = False
        
        # Test invalid scorer
        try:
            response = self.session.post(
                f"{self.base_url}/match",
                json={
                    "query": "test",
                    "candidates": ["test1", "test2"],
                    "scorer": "invalid_scorer"
                },
                timeout=5
            )
            invalid_scorer_handled = response.status_code == 200
            self.log_test("Invalid scorer handling", invalid_scorer_handled)
            all_passed &= invalid_scorer_handled
            
        except Exception as e:
            self.log_test("Invalid scorer handling", False, f"Error: {e}")
            all_passed = False
        
        return all_passed
    
    def run_all_tests(self) -> bool:
        """Run all validation tests."""
        print("🔧 InfoTerminal Service Consolidation Validation")
        print("=" * 50)
        print(f"Testing service at: {self.base_url}")
        print()
        
        all_passed = True
        
        # Core functionality tests
        print("📋 Core Functionality Tests:")
        all_passed &= self.test_health_endpoints()
        all_passed &= self.test_nlp_endpoints()
        
        print("\n🎯 New Fuzzy Matching Tests:")
        all_passed &= self.test_fuzzy_endpoints()
        
        print("\n🔄 Enhanced Workflow Tests:")
        all_passed &= self.test_enhanced_workflow()
        
        print("\n⚡ Performance Tests:")
        all_passed &= self.test_performance()
        
        print("\n🛡️ Error Handling Tests:")
        all_passed &= self.test_error_handling()
        
        # Summary
        print("\n" + "=" * 50)
        passed_tests = sum(1 for result in self.test_results if result["passed"])
        total_tests = len(self.test_results)
        
        if all_passed:
            print(f"🎉 ALL TESTS PASSED ({passed_tests}/{total_tests})")
            print("✅ Service consolidation successful!")
        else:
            print(f"❌ SOME TESTS FAILED ({passed_tests}/{total_tests})")
            print("⚠️  Service consolidation needs attention.")
            
            # Show failed tests
            failed_tests = [r for r in self.test_results if not r["passed"]]
            if failed_tests:
                print("\nFailed tests:")
                for test in failed_tests:
                    print(f"  - {test['name']}: {test['message']}")
        
        return all_passed
    
    def generate_report(self, output_file: str = "validation_report.json") -> None:
        """Generate detailed validation report."""
        report = {
            "timestamp": time.time(),
            "service_url": self.base_url,
            "total_tests": len(self.test_results),
            "passed_tests": sum(1 for r in self.test_results if r["passed"]),
            "overall_success": all(r["passed"] for r in self.test_results),
            "test_results": self.test_results
        }
        
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Detailed report saved to: {output_file}")


def main():
    """Main validation script entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate consolidated doc-entities service")
    parser.add_argument(
        "--url", 
        default="http://localhost:8613",
        help="Service base URL (default: http://localhost:8613)"
    )
    parser.add_argument(
        "--report",
        help="Generate detailed JSON report to specified file"
    )
    
    args = parser.parse_args()
    
    validator = ServiceValidator(args.url)
    
    try:
        success = validator.run_all_tests()
        
        if args.report:
            validator.generate_report(args.report)
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Validation failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
