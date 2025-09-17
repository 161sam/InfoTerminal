"""
InfoTerminal E2E OSINT Workflow Tests

Tests for typical OSINT workflows with user journey tracking and performance monitoring.
"""

import pytest
import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dataclasses import dataclass
from typing import List, Dict, Optional
import json
import os
from datetime import datetime

@dataclass
class UserAction:
    """Track individual user actions for journey analysis"""
    timestamp: datetime
    action_type: str
    element: str
    duration_ms: int
    success: bool
    error_message: Optional[str] = None

@dataclass
class WorkflowMetrics:
    """Performance metrics for workflow execution"""
    total_duration_ms: int
    actions: List[UserAction]
    page_load_times: Dict[str, int]
    api_response_times: Dict[str, int]
    errors: List[str]
    completion_rate: float

class OSINTWorkflowTester:
    """E2E testing framework for OSINT workflows"""
    
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.driver = None
        self.wait = None
        self.current_workflow = None
        self.metrics = WorkflowMetrics(
            total_duration_ms=0,
            actions=[],
            page_load_times={},
            api_response_times={},
            errors=[],
            completion_rate=0.0
        )
    
    def setup_driver(self):
        """Initialize Chrome driver with performance monitoring"""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode for CI
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Enable logging for performance monitoring
        options.add_argument("--enable-logging")
        options.add_argument("--log-level=0")
        
        # Performance settings
        prefs = {
            "profile.default_content_setting_values": {
                "notifications": 2
            }
        }
        options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Enable performance timing
        self.driver.execute_script("""
            window.performance.mark('test-start');
        """)
    
    def track_action(self, action_type: str, element: str, duration_ms: int, 
                    success: bool, error_message: str = None):
        """Track user action for journey analysis"""
        action = UserAction(
            timestamp=datetime.now(),
            action_type=action_type,
            element=element,
            duration_ms=duration_ms,
            success=success,
            error_message=error_message
        )
        self.metrics.actions.append(action)
    
    def measure_page_load(self, page_name: str):
        """Measure page load performance"""
        start_time = time.time()
        load_time = self.driver.execute_script("""
            return window.performance.timing.loadEventEnd - 
                   window.performance.timing.navigationStart;
        """)
        self.metrics.page_load_times[page_name] = load_time
        return load_time
    
    def wait_for_element_clickable(self, by: By, value: str, timeout: int = 10):
        """Wait for element to be clickable and track timing"""
        start_time = time.time()
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            duration = int((time.time() - start_time) * 1000)
            self.track_action("wait_for_element", value, duration, True)
            return element
        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            self.track_action("wait_for_element", value, duration, False, str(e))
            raise
    
    def click_element(self, by: By, value: str):
        """Click element with performance tracking"""
        start_time = time.time()
        try:
            element = self.wait_for_element_clickable(by, value)
            element.click()
            duration = int((time.time() - start_time) * 1000)
            self.track_action("click", value, duration, True)
            return element
        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            self.track_action("click", value, duration, False, str(e))
            raise
    
    def type_text(self, by: By, value: str, text: str):
        """Type text with performance tracking"""
        start_time = time.time()
        try:
            element = self.wait_for_element_clickable(by, value)
            element.clear()
            element.send_keys(text)
            duration = int((time.time() - start_time) * 1000)
            self.track_action("type", f"{value}:{text}", duration, True)
            return element
        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            self.track_action("type", f"{value}:{text}", duration, False, str(e))
            raise
    
    def workflow_person_investigation(self, target_name: str):
        """Test Person-of-Interest Investigation workflow"""
        self.current_workflow = "person_investigation"
        workflow_start = time.time()
        
        try:
            # Navigate to main dashboard
            self.driver.get(f"{self.base_url}/dashboard")
            self.measure_page_load("dashboard")
            
            # Open entity search
            self.click_element(By.ID, "entity-search-button")
            
            # Search for person
            self.type_text(By.ID, "entity-search-input", target_name)
            self.click_element(By.ID, "search-submit")
            
            # Wait for search results
            self.wait_for_element_clickable(By.CLASS_NAME, "search-results")
            
            # Select first result
            self.click_element(By.CSS_SELECTOR, ".search-result:first-child")
            
            # Navigate to entity details
            self.wait_for_element_clickable(By.ID, "entity-details-panel")
            
            # Open graph view
            self.click_element(By.ID, "graph-view-button")
            
            # Wait for graph to load
            self.wait_for_element_clickable(By.CLASS_NAME, "graph-container", 15)
            
            # Expand entity connections
            self.click_element(By.ID, "expand-connections-button")
            
            # Wait for expanded graph
            time.sleep(3)  # Allow graph animation to complete
            
            # Export results
            self.click_element(By.ID, "export-button")
            self.click_element(By.ID, "export-json")
            
            workflow_duration = int((time.time() - workflow_start) * 1000)
            self.metrics.total_duration_ms = workflow_duration
            self.metrics.completion_rate = 1.0
            
            return True
            
        except Exception as e:
            self.metrics.errors.append(f"Person investigation failed: {str(e)}")
            self.metrics.completion_rate = len([a for a in self.metrics.actions if a.success]) / len(self.metrics.actions)
            return False
    
    def workflow_domain_analysis(self, domain: str):
        """Test Domain/Infrastructure Analysis workflow"""
        self.current_workflow = "domain_analysis"
        workflow_start = time.time()
        
        try:
            # Navigate to security tools
            self.driver.get(f"{self.base_url}/tools")
            self.measure_page_load("tools")
            
            # Select domain analysis tool
            self.click_element(By.ID, "domain-analysis-tool")
            
            # Enter domain
            self.type_text(By.ID, "domain-input", domain)
            
            # Start analysis
            self.click_element(By.ID, "start-analysis")
            
            # Wait for analysis to complete
            self.wait_for_element_clickable(By.ID, "analysis-complete", 30)
            
            # View results
            self.click_element(By.ID, "view-results")
            
            # Check subdomain results
            self.wait_for_element_clickable(By.CLASS_NAME, "subdomain-results")
            
            # View DNS information
            self.click_element(By.ID, "dns-info-tab")
            
            # Export infrastructure map
            self.click_element(By.ID, "export-infrastructure")
            
            workflow_duration = int((time.time() - workflow_start) * 1000)
            self.metrics.total_duration_ms = workflow_duration
            self.metrics.completion_rate = 1.0
            
            return True
            
        except Exception as e:
            self.metrics.errors.append(f"Domain analysis failed: {str(e)}")
            self.metrics.completion_rate = len([a for a in self.metrics.actions if a.success]) / len(self.metrics.actions)
            return False
    
    def workflow_social_media_investigation(self, username: str):
        """Test Social Media Investigation workflow"""
        self.current_workflow = "social_media_investigation"
        workflow_start = time.time()
        
        try:
            # Navigate to social media tools
            self.driver.get(f"{self.base_url}/social")
            self.measure_page_load("social")
            
            # Enter username
            self.type_text(By.ID, "username-input", username)
            
            # Select platforms
            self.click_element(By.ID, "platform-twitter")
            self.click_element(By.ID, "platform-linkedin")
            self.click_element(By.ID, "platform-instagram")
            
            # Start investigation
            self.click_element(By.ID, "start-investigation")
            
            # Wait for results
            self.wait_for_element_clickable(By.CLASS_NAME, "social-results", 20)
            
            # View profile analysis
            self.click_element(By.ID, "profile-analysis-tab")
            
            # Check sentiment analysis
            self.click_element(By.ID, "sentiment-analysis-tab")
            
            # View connection graph
            self.click_element(By.ID, "connection-graph-tab")
            
            # Export social network map
            self.click_element(By.ID, "export-social-map")
            
            workflow_duration = int((time.time() - workflow_start) * 1000)
            self.metrics.total_duration_ms = workflow_duration
            self.metrics.completion_rate = 1.0
            
            return True
            
        except Exception as e:
            self.metrics.errors.append(f"Social media investigation failed: {str(e)}")
            self.metrics.completion_rate = len([a for a in self.metrics.actions if a.success]) / len(self.metrics.actions)
            return False
    
    def workflow_document_analysis(self, document_path: str):
        """Test Document Leak Analysis workflow"""
        self.current_workflow = "document_analysis"
        workflow_start = time.time()
        
        try:
            # Navigate to document analysis
            self.driver.get(f"{self.base_url}/documents")
            self.measure_page_load("documents")
            
            # Upload document
            file_input = self.driver.find_element(By.ID, "file-upload")
            file_input.send_keys(document_path)
            
            # Start analysis
            self.click_element(By.ID, "analyze-document")
            
            # Wait for processing
            self.wait_for_element_clickable(By.ID, "analysis-results", 30)
            
            # View entity extraction
            self.click_element(By.ID, "entities-tab")
            
            # Check metadata analysis
            self.click_element(By.ID, "metadata-tab")
            
            # View sentiment analysis
            self.click_element(By.ID, "sentiment-tab")
            
            # Export analysis report
            self.click_element(By.ID, "export-report")
            
            workflow_duration = int((time.time() - workflow_start) * 1000)
            self.metrics.total_duration_ms = workflow_duration
            self.metrics.completion_rate = 1.0
            
            return True
            
        except Exception as e:
            self.metrics.errors.append(f"Document analysis failed: {str(e)}")
            self.metrics.completion_rate = len([a for a in self.metrics.actions if a.success]) / len(self.metrics.actions)
            return False
    
    def workflow_geospatial_verification(self, coordinates: tuple):
        """Test Geospatial Event Verification workflow"""
        self.current_workflow = "geospatial_verification"
        workflow_start = time.time()
        
        try:
            # Navigate to geospatial tools
            self.driver.get(f"{self.base_url}/geospatial")
            self.measure_page_load("geospatial")
            
            # Enter coordinates
            lat, lon = coordinates
            self.type_text(By.ID, "latitude-input", str(lat))
            self.type_text(By.ID, "longitude-input", str(lon))
            
            # Start verification
            self.click_element(By.ID, "verify-location")
            
            # Wait for map to load
            self.wait_for_element_clickable(By.CLASS_NAME, "map-container", 15)
            
            # View satellite imagery
            self.click_element(By.ID, "satellite-view")
            
            # Check historical imagery
            self.click_element(By.ID, "historical-imagery")
            
            # Analyze changes
            self.click_element(By.ID, "analyze-changes")
            
            # Export verification report
            self.click_element(By.ID, "export-verification")
            
            workflow_duration = int((time.time() - workflow_start) * 1000)
            self.metrics.total_duration_ms = workflow_duration
            self.metrics.completion_rate = 1.0
            
            return True
            
        except Exception as e:
            self.metrics.errors.append(f"Geospatial verification failed: {str(e)}")
            self.metrics.completion_rate = len([a for a in self.metrics.actions if a.success]) / len(self.metrics.actions)
            return False
    
    def save_metrics(self, output_path: str):
        """Save workflow metrics to JSON file"""
        metrics_data = {
            "workflow": self.current_workflow,
            "timestamp": datetime.now().isoformat(),
            "total_duration_ms": self.metrics.total_duration_ms,
            "completion_rate": self.metrics.completion_rate,
            "page_load_times": self.metrics.page_load_times,
            "api_response_times": self.metrics.api_response_times,
            "errors": self.metrics.errors,
            "actions": [
                {
                    "timestamp": action.timestamp.isoformat(),
                    "action_type": action.action_type,
                    "element": action.element,
                    "duration_ms": action.duration_ms,
                    "success": action.success,
                    "error_message": action.error_message
                }
                for action in self.metrics.actions
            ]
        }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(metrics_data, f, indent=2)
    
    def teardown(self):
        """Clean up driver and save metrics"""
        if self.driver:
            self.driver.quit()

# Test cases using pytest
@pytest.fixture
def workflow_tester():
    """Fixture providing OSINT workflow tester"""
    tester = OSINTWorkflowTester()
    tester.setup_driver()
    yield tester
    tester.teardown()

def test_person_investigation_workflow(workflow_tester):
    """Test complete person investigation workflow"""
    success = workflow_tester.workflow_person_investigation("John Doe")
    
    # Save metrics
    workflow_tester.save_metrics(
        f"tests/user-testing/metrics/person_investigation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    
    # Assertions
    assert success, f"Person investigation failed: {workflow_tester.metrics.errors}"
    assert workflow_tester.metrics.completion_rate >= 0.8, "Completion rate too low"
    assert workflow_tester.metrics.total_duration_ms < 30000, "Workflow took too long"

def test_domain_analysis_workflow(workflow_tester):
    """Test complete domain analysis workflow"""
    success = workflow_tester.workflow_domain_analysis("example.com")
    
    # Save metrics
    workflow_tester.save_metrics(
        f"tests/user-testing/metrics/domain_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    
    # Assertions
    assert success, f"Domain analysis failed: {workflow_tester.metrics.errors}"
    assert workflow_tester.metrics.completion_rate >= 0.8, "Completion rate too low"
    assert workflow_tester.metrics.total_duration_ms < 45000, "Workflow took too long"

def test_social_media_investigation_workflow(workflow_tester):
    """Test complete social media investigation workflow"""
    success = workflow_tester.workflow_social_media_investigation("testuser")
    
    # Save metrics
    workflow_tester.save_metrics(
        f"tests/user-testing/metrics/social_media_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    
    # Assertions
    assert success, f"Social media investigation failed: {workflow_tester.metrics.errors}"
    assert workflow_tester.metrics.completion_rate >= 0.8, "Completion rate too low"
    assert workflow_tester.metrics.total_duration_ms < 40000, "Workflow took too long"

def test_document_analysis_workflow(workflow_tester):
    """Test complete document analysis workflow"""
    # Use a test document (would need to be created)
    test_doc_path = "/path/to/test/document.pdf"
    success = workflow_tester.workflow_document_analysis(test_doc_path)
    
    # Save metrics
    workflow_tester.save_metrics(
        f"tests/user-testing/metrics/document_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    
    # Assertions
    assert success, f"Document analysis failed: {workflow_tester.metrics.errors}"
    assert workflow_tester.metrics.completion_rate >= 0.8, "Completion rate too low"
    assert workflow_tester.metrics.total_duration_ms < 60000, "Workflow took too long"

def test_geospatial_verification_workflow(workflow_tester):
    """Test complete geospatial verification workflow"""
    # Test coordinates (e.g., Times Square)
    coordinates = (40.7580, -73.9855)
    success = workflow_tester.workflow_geospatial_verification(coordinates)
    
    # Save metrics
    workflow_tester.save_metrics(
        f"tests/user-testing/metrics/geospatial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    
    # Assertions
    assert success, f"Geospatial verification failed: {workflow_tester.metrics.errors}"
    assert workflow_tester.metrics.completion_rate >= 0.8, "Completion rate too low"
    assert workflow_tester.metrics.total_duration_ms < 35000, "Workflow took too long"

if __name__ == "__main__":
    # Run tests manually for debugging
    tester = OSINTWorkflowTester()
    tester.setup_driver()
    
    try:
        # Test all workflows
        workflows = [
            ("person_investigation", lambda: tester.workflow_person_investigation("John Doe")),
            ("domain_analysis", lambda: tester.workflow_domain_analysis("example.com")),
            ("social_media", lambda: tester.workflow_social_media_investigation("testuser")),
            ("geospatial", lambda: tester.workflow_geospatial_verification((40.7580, -73.9855)))
        ]
        
        for workflow_name, workflow_func in workflows:
            print(f"Testing {workflow_name}...")
            success = workflow_func()
            print(f"✓ {workflow_name}: {'PASSED' if success else 'FAILED'}")
            
            # Save metrics
            tester.save_metrics(f"tests/user-testing/metrics/{workflow_name}_manual.json")
            
    finally:
        tester.teardown()
