"""
OSINT Workflow End-to-End Tests for InfoTerminal

Comprehensive test suite covering real-world OSINT investigation scenarios
including entity discovery, relationship mapping, and collaborative features.
"""

import asyncio
import json
import os
import pytest
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from unittest.mock import AsyncMock, patch

import aiohttp
import websockets
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
import neo4j
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis


@dataclass
class TestResult:
    """Test result data structure"""
    test_name: str
    start_time: datetime
    end_time: datetime
    status: str  # "passed", "failed", "skipped"
    duration_ms: int
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class InvestigationScenario:
    """OSINT investigation test scenario"""
    name: str
    description: str
    initial_entities: List[Dict[str, Any]]
    expected_discoveries: List[Dict[str, Any]]
    workflow_steps: List[Dict[str, Any]]
    success_criteria: Dict[str, Any]


class OSINTWorkflowTester:
    """Main test orchestrator for OSINT workflows"""
    
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.api_url = os.getenv("API_URL", "http://localhost:8000")
        self.ws_url = os.getenv("WS_URL", "ws://localhost:8083")
        
        # Database connections
        self.pg_engine = None
        self.neo4j_driver = None
        self.redis_client = None
        
        # Browser automation
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        # Test results
        self.test_results: List[TestResult] = []
        self.current_test_start: Optional[datetime] = None
    
    async def setup(self):
        """Initialize test environment and connections"""
        print("🔧 Setting up OSINT Workflow Test Environment...")
        
        # Setup database connections
        await self._setup_database_connections()
        
        # Setup browser automation
        await self._setup_browser()
        
        # Verify system health
        await self._verify_system_health()
        
        print("✅ Test environment ready")
    
    async def teardown(self):
        """Cleanup test environment"""
        print("🧹 Cleaning up test environment...")
        
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        
        if self.neo4j_driver:
            await self.neo4j_driver.close()
        
        if self.redis_client:
            await self.redis_client.close()
        
        print("✅ Cleanup completed")
    
    async def _setup_database_connections(self):
        """Setup database connections for testing"""
        try:
            # PostgreSQL
            db_url = os.getenv("TEST_DATABASE_URL", "postgresql://test:test@localhost:5432/infoterminal_test")
            self.pg_engine = create_engine(db_url)
            
            # Neo4j
            neo4j_uri = os.getenv("TEST_NEO4J_URI", "bolt://localhost:7687")
            neo4j_user = os.getenv("TEST_NEO4J_USER", "neo4j")
            neo4j_password = os.getenv("TEST_NEO4J_PASSWORD", "test")
            self.neo4j_driver = neo4j.AsyncGraphDatabase.driver(
                neo4j_uri, auth=(neo4j_user, neo4j_password)
            )
            
            # Redis
            redis_url = os.getenv("TEST_REDIS_URL", "redis://localhost:6379")
            self.redis_client = redis.Redis.from_url(redis_url)
            
        except Exception as e:
            print(f"❌ Failed to setup database connections: {e}")
            raise
    
    async def _setup_browser(self):
        """Setup browser automation"""
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=os.getenv("HEADLESS", "true").lower() == "true",
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='InfoTerminal E2E Test Bot 1.0'
            )
            
            self.page = await self.context.new_page()
            
            # Enable console logging
            self.page.on("console", lambda msg: print(f"Browser: {msg.text}"))
            self.page.on("pageerror", lambda error: print(f"Page Error: {error}"))
            
        except Exception as e:
            print(f"❌ Failed to setup browser: {e}")
            raise
    
    async def _verify_system_health(self):
        """Verify all system components are healthy"""
        health_checks = [
            ("Frontend", f"{self.base_url}/api/health"),
            ("Backend API", f"{self.api_url}/health"),
            ("WebSocket", f"{self.ws_url.replace('ws', 'http')}/health"),
        ]
        
        async with aiohttp.ClientSession() as session:
            for service_name, health_url in health_checks:
                try:
                    async with session.get(health_url, timeout=10) as response:
                        if response.status != 200:
                            raise Exception(f"Health check failed: {response.status}")
                        print(f"✅ {service_name} is healthy")
                except Exception as e:
                    print(f"❌ {service_name} health check failed: {e}")
                    raise
    
    def start_test(self, test_name: str):
        """Start timing a test"""
        self.current_test_start = datetime.now()
        print(f"\n🧪 Starting test: {test_name}")
    
    def end_test(self, test_name: str, status: str = "passed", error_message: str = None, metadata: Dict = None):
        """End timing a test and record results"""
        end_time = datetime.now()
        duration_ms = int((end_time - self.current_test_start).total_seconds() * 1000)
        
        result = TestResult(
            test_name=test_name,
            start_time=self.current_test_start,
            end_time=end_time,
            status=status,
            duration_ms=duration_ms,
            error_message=error_message,
            metadata=metadata
        )
        
        self.test_results.append(result)
        
        status_icon = "✅" if status == "passed" else "❌" if status == "failed" else "⏭️"
        print(f"{status_icon} Test {test_name} {status} ({duration_ms}ms)")
        
        if error_message:
            print(f"   Error: {error_message}")
    
    async def run_person_investigation_workflow(self) -> TestResult:
        """Test complete person investigation workflow"""
        test_name = "person_investigation_workflow"
        self.start_test(test_name)
        
        try:
            # Navigate to the application
            await self.page.goto(self.base_url)
            await self.page.wait_for_load_state("networkidle")
            
            # Step 1: Start new investigation
            await self.page.click('[data-testid="new-investigation-btn"]')
            await self.page.fill('[data-testid="investigation-name"]', "Test Person Investigation")
            await self.page.select_option('[data-testid="investigation-type"]', "person")
            await self.page.click('[data-testid="create-investigation"]')
            
            # Step 2: Add initial entity (person)
            await self.page.click('[data-testid="add-entity-btn"]')
            await self.page.select_option('[data-testid="entity-type"]', "person")
            await self.page.fill('[data-testid="person-name"]', "John Doe")
            await self.page.fill('[data-testid="person-email"]', "john.doe@example.com")
            await self.page.click('[data-testid="save-entity"]')
            
            # Step 3: Run domain analysis plugin
            await self.page.click('[data-testid="run-plugin"]')
            await self.page.select_option('[data-testid="plugin-select"]', "domain_analysis")
            await self.page.click('[data-testid="execute-plugin"]')
            
            # Wait for plugin execution
            await self.page.wait_for_selector('[data-testid="plugin-completed"]', timeout=30000)
            
            # Step 4: Verify graph visualization updates
            graph_nodes = await self.page.locator('[data-testid="graph-node"]').count()
            if graph_nodes < 2:
                raise Exception(f"Expected at least 2 nodes in graph, found {graph_nodes}")
            
            # Step 5: Test collaborative features
            await self.page.click('[data-testid="share-investigation"]')
            await self.page.fill('[data-testid="share-email"]', "colleague@example.com")
            await self.page.click('[data-testid="send-share"]')
            
            # Step 6: Export investigation report
            await self.page.click('[data-testid="export-report"]')
            await self.page.select_option('[data-testid="export-format"]', "pdf")
            
            # Wait for download
            download_info = await self.page.wait_for_download()
            if not download_info:
                raise Exception("Failed to generate investigation report")
            
            # Verify database state
            await self._verify_investigation_in_database("Test Person Investigation")
            
            self.end_test(test_name, "passed", metadata={
                "graph_nodes": graph_nodes,
                "download_size": download_info.path().stat().st_size if download_info.path().exists() else 0
            })
            
        except Exception as e:
            self.end_test(test_name, "failed", str(e))
            raise
    
    async def run_domain_investigation_workflow(self) -> TestResult:
        """Test domain investigation workflow with multiple plugins"""
        test_name = "domain_investigation_workflow"
        self.start_test(test_name)
        
        try:
            await self.page.goto(f"{self.base_url}/search")
            
            # Step 1: Search for domain
            await self.page.fill('[data-testid="search-input"]', "example.com")
            await self.page.click('[data-testid="search-btn"]')
            
            # Wait for search results
            await self.page.wait_for_selector('[data-testid="search-results"]')
            
            # Step 2: Start investigation from search result
            await self.page.click('[data-testid="investigate-domain"]')
            
            # Step 3: Run multiple plugins in sequence
            plugins_to_run = [
                "whois_lookup",
                "dns_enumeration", 
                "subdomain_discovery",
                "ssl_certificate_analysis"
            ]
            
            discovered_entities = 0
            for plugin in plugins_to_run:
                await self.page.click('[data-testid="run-plugin"]')
                await self.page.select_option('[data-testid="plugin-select"]', plugin)
                await self.page.click('[data-testid="execute-plugin"]')
                
                # Wait for completion
                await self.page.wait_for_selector(f'[data-testid="plugin-{plugin}-completed"]', timeout=60000)
                
                # Count new entities discovered
                current_count = await self.page.locator('[data-testid="entity-count"]').text_content()
                discovered_entities = int(current_count)
            
            # Step 4: Analyze relationships in graph
            await self.page.click('[data-testid="graph-view"]')
            await self.page.wait_for_selector('[data-testid="graph-canvas"]')
            
            # Test graph interactions
            await self.page.click('[data-testid="center-graph"]')
            await self.page.click('[data-testid="filter-relationships"]')
            
            # Step 5: Generate domain intelligence report
            await self.page.click('[data-testid="generate-report"]')
            await self.page.select_option('[data-testid="report-template"]', "domain_intelligence")
            
            report_ready = await self.page.wait_for_selector('[data-testid="report-ready"]', timeout=30000)
            
            if discovered_entities < 5:
                raise Exception(f"Expected at least 5 entities, discovered {discovered_entities}")
            
            self.end_test(test_name, "passed", metadata={
                "discovered_entities": discovered_entities,
                "plugins_executed": len(plugins_to_run)
            })
            
        except Exception as e:
            self.end_test(test_name, "failed", str(e))
            raise
    
    async def run_social_media_investigation_workflow(self) -> TestResult:
        """Test social media investigation workflow"""
        test_name = "social_media_investigation_workflow"
        self.start_test(test_name)
        
        try:
            await self.page.goto(f"{self.base_url}/tools/social-media")
            
            # Step 1: Configure social media investigation
            await self.page.fill('[data-testid="username-input"]', "testuser123")
            await self.page.check('[data-testid="platform-twitter"]')
            await self.page.check('[data-testid="platform-linkedin"]')
            await self.page.check('[data-testid="platform-facebook"]')
            
            # Step 2: Start investigation
            await self.page.click('[data-testid="start-social-investigation"]')
            
            # Wait for platform searches to complete
            platforms_completed = 0
            for platform in ["twitter", "linkedin", "facebook"]:
                try:
                    await self.page.wait_for_selector(
                        f'[data-testid="platform-{platform}-completed"]', 
                        timeout=45000
                    )
                    platforms_completed += 1
                except:
                    print(f"⚠️ Platform {platform} search timed out")
            
            # Step 3: Analyze social connections
            if platforms_completed > 0:
                await self.page.click('[data-testid="analyze-connections"]')
                await self.page.wait_for_selector('[data-testid="connection-analysis-complete"]')
            
            # Step 4: Generate timeline view
            await self.page.click('[data-testid="timeline-view"]')
            timeline_events = await self.page.locator('[data-testid="timeline-event"]').count()
            
            # Step 5: Export social intelligence report
            await self.page.click('[data-testid="export-social-report"]')
            
            self.end_test(test_name, "passed", metadata={
                "platforms_completed": platforms_completed,
                "timeline_events": timeline_events
            })
            
        except Exception as e:
            self.end_test(test_name, "failed", str(e))
            raise
    
    async def run_collaborative_investigation_workflow(self) -> TestResult:
        """Test collaborative investigation features"""
        test_name = "collaborative_investigation_workflow"
        self.start_test(test_name)
        
        try:
            # This test requires two browser contexts to simulate collaboration
            context2 = await self.browser.new_context()
            page2 = await context2.new_page()
            
            # User 1: Create investigation
            await self.page.goto(self.base_url)
            await self.page.click('[data-testid="new-investigation-btn"]')
            await self.page.fill('[data-testid="investigation-name"]', "Collaborative Test")
            await self.page.click('[data-testid="create-investigation"]')
            
            # Get investigation URL
            investigation_url = await self.page.url
            
            # Share investigation
            await self.page.click('[data-testid="share-investigation"]')
            share_link = await self.page.locator('[data-testid="share-link"]').text_content()
            
            # User 2: Join investigation
            await page2.goto(share_link)
            await page2.wait_for_selector('[data-testid="investigation-joined"]')
            
            # Test real-time collaboration
            # User 1: Add entity
            await self.page.click('[data-testid="add-entity-btn"]')
            await self.page.fill('[data-testid="entity-name"]', "Collaborative Entity")
            await self.page.click('[data-testid="save-entity"]')
            
            # User 2: Should see the new entity
            await page2.wait_for_selector('[data-testid="entity-Collaborative Entity"]', timeout=10000)
            
            # User 2: Add comment
            await page2.click('[data-testid="add-comment"]')
            await page2.fill('[data-testid="comment-text"]', "This is a test comment")
            await page2.click('[data-testid="save-comment"]')
            
            # User 1: Should see the comment
            await self.page.wait_for_selector('[data-testid="comment-This is a test comment"]', timeout=10000)
            
            # Test cursor tracking
            await page2.mouse.move(500, 300)
            cursor_visible = await self.page.locator('[data-testid="user2-cursor"]').is_visible()
            
            await context2.close()
            
            self.end_test(test_name, "passed", metadata={
                "real_time_sync": True,
                "cursor_tracking": cursor_visible
            })
            
        except Exception as e:
            self.end_test(test_name, "failed", str(e))
            raise
    
    async def run_performance_stress_test(self) -> TestResult:
        """Test system performance under load"""
        test_name = "performance_stress_test"
        self.start_test(test_name)
        
        try:
            # Create large investigation with many entities
            await self.page.goto(self.base_url)
            await self.page.click('[data-testid="new-investigation-btn"]')
            await self.page.fill('[data-testid="investigation-name"]', "Performance Test")
            await self.page.click('[data-testid="create-investigation"]')
            
            # Add many entities quickly
            entity_count = 50
            for i in range(entity_count):
                await self.page.click('[data-testid="add-entity-btn"]')
                await self.page.fill('[data-testid="entity-name"]', f"Entity {i}")
                await self.page.click('[data-testid="save-entity"]')
                
                # Every 10 entities, check performance
                if i > 0 and i % 10 == 0:
                    start_time = time.time()
                    await self.page.wait_for_selector('[data-testid="graph-updated"]')
                    render_time = (time.time() - start_time) * 1000
                    
                    if render_time > 2000:  # 2 seconds threshold
                        raise Exception(f"Graph rendering too slow: {render_time}ms at {i} entities")
            
            # Test graph performance with many nodes
            await self.page.click('[data-testid="graph-view"]')
            
            start_time = time.time()
            await self.page.click('[data-testid="center-graph"]')
            center_time = (time.time() - start_time) * 1000
            
            # Test search performance
            start_time = time.time()
            await self.page.fill('[data-testid="search-entities"]', "Entity 25")
            await self.page.wait_for_selector('[data-testid="search-results"]')
            search_time = (time.time() - start_time) * 1000
            
            self.end_test(test_name, "passed", metadata={
                "entity_count": entity_count,
                "graph_center_time_ms": center_time,
                "search_time_ms": search_time
            })
            
        except Exception as e:
            self.end_test(test_name, "failed", str(e))
            raise
    
    async def _verify_investigation_in_database(self, investigation_name: str):
        """Verify investigation was properly saved to database"""
        async with self.neo4j_driver.session() as session:
            result = await session.run(
                "MATCH (i:Investigation {name: $name}) RETURN count(i) as count",
                name=investigation_name
            )
            record = await result.single()
            if record["count"] == 0:
                raise Exception(f"Investigation '{investigation_name}' not found in database")
    
    async def run_all_workflows(self) -> List[TestResult]:
        """Run all OSINT workflow tests"""
        print("🚀 Starting comprehensive OSINT workflow tests...")
        
        workflows = [
            self.run_person_investigation_workflow,
            self.run_domain_investigation_workflow,
            self.run_social_media_investigation_workflow,
            self.run_collaborative_investigation_workflow,
            self.run_performance_stress_test,
        ]
        
        for workflow in workflows:
            try:
                await workflow()
                # Small delay between tests
                await asyncio.sleep(2)
            except Exception as e:
                print(f"❌ Workflow failed: {e}")
                continue
        
        return self.test_results
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        if not self.test_results:
            return {"error": "No test results available"}
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r.status == "passed")
        failed_tests = sum(1 for r in self.test_results if r.status == "failed")
        
        total_duration = sum(r.duration_ms for r in self.test_results)
        avg_duration = total_duration / total_tests if total_tests > 0 else 0
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
                "total_duration_ms": total_duration,
                "average_duration_ms": avg_duration
            },
            "test_results": [asdict(result) for result in self.test_results],
            "timestamp": datetime.now().isoformat(),
            "environment": {
                "base_url": self.base_url,
                "api_url": self.api_url,
                "ws_url": self.ws_url
            }
        }
        
        return report


# Pytest integration
@pytest.fixture
async def workflow_tester():
    """Pytest fixture for workflow tester"""
    tester = OSINTWorkflowTester()
    await tester.setup()
    yield tester
    await tester.teardown()


@pytest.mark.asyncio
async def test_person_investigation_workflow(workflow_tester):
    """Test person investigation workflow"""
    await workflow_tester.run_person_investigation_workflow()
    assert workflow_tester.test_results[-1].status == "passed"


@pytest.mark.asyncio
async def test_domain_investigation_workflow(workflow_tester):
    """Test domain investigation workflow"""
    await workflow_tester.run_domain_investigation_workflow()
    assert workflow_tester.test_results[-1].status == "passed"


@pytest.mark.asyncio
async def test_collaborative_features(workflow_tester):
    """Test collaborative investigation features"""
    await workflow_tester.run_collaborative_investigation_workflow()
    assert workflow_tester.test_results[-1].status == "passed"


@pytest.mark.asyncio
async def test_performance_under_load(workflow_tester):
    """Test system performance under load"""
    await workflow_tester.run_performance_stress_test()
    assert workflow_tester.test_results[-1].status == "passed"


# CLI execution
async def main():
    """Main CLI function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="InfoTerminal OSINT Workflow Tests")
    parser.add_argument("--base-url", default="http://localhost:3000", help="Frontend base URL")
    parser.add_argument("--report-file", default="workflow_test_results.json", help="Test report output file")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    
    args = parser.parse_args()
    
    # Set environment variables
    os.environ["HEADLESS"] = "true" if args.headless else "false"
    
    tester = OSINTWorkflowTester(base_url=args.base_url)
    
    try:
        await tester.setup()
        await tester.run_all_workflows()
        
        # Generate and save report
        report = tester.generate_test_report()
        
        with open(args.report_file, "w") as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n📊 Test Report Generated: {args.report_file}")
        print(f"✅ Passed: {report['summary']['passed']}")
        print(f"❌ Failed: {report['summary']['failed']}")
        print(f"📈 Success Rate: {report['summary']['success_rate']:.1f}%")
        print(f"⏱️ Total Duration: {report['summary']['total_duration_ms']}ms")
        
    finally:
        await tester.teardown()


if __name__ == "__main__":
    asyncio.run(main())
