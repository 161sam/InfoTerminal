"""
OSINT Investigation Scenarios

Five realistic OSINT scenarios as guided tutorials for user testing and training.
"""

import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class ScenarioType(str, Enum):
    PERSON_INVESTIGATION = "person_investigation"
    DOMAIN_ANALYSIS = "domain_analysis"
    SOCIAL_MEDIA = "social_media_investigation"
    DOCUMENT_ANALYSIS = "document_analysis"
    GEOSPATIAL_VERIFICATION = "geospatial_verification"

class StepType(str, Enum):
    NAVIGATION = "navigation"
    SEARCH = "search"
    ANALYSIS = "analysis"
    VERIFICATION = "verification"
    EXPORT = "export"
    DECISION = "decision"

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass
class ScenarioStep:
    """Individual step in an OSINT scenario"""
    id: str
    title: str
    description: str
    step_type: StepType
    instructions: List[str]
    expected_actions: List[str]
    hints: List[str]
    success_criteria: Dict[str, Any]
    estimated_time_minutes: int
    tools_required: List[str]
    data_inputs: Dict[str, Any]
    expected_outputs: Dict[str, Any]
    learning_objectives: List[str]
    common_mistakes: List[str]
    next_step_conditions: Dict[str, str]  # condition -> next_step_id

@dataclass
class OSINTScenario:
    """Complete OSINT investigation scenario"""
    id: str
    title: str
    description: str
    scenario_type: ScenarioType
    difficulty: DifficultyLevel
    estimated_duration_minutes: int
    learning_objectives: List[str]
    prerequisites: List[str]
    tools_required: List[str]
    steps: List[ScenarioStep]
    background_story: str
    success_metrics: Dict[str, Any]
    evaluation_criteria: List[str]
    additional_resources: List[Dict[str, str]]
    created_at: str
    updated_at: str

class OSINTScenarioGenerator:
    """Generates realistic OSINT investigation scenarios"""
    
    def __init__(self):
        self.scenarios = []
        self._generate_all_scenarios()
    
    def _generate_all_scenarios(self):
        """Generate all five core OSINT scenarios"""
        self.scenarios = [
            self._generate_person_investigation(),
            self._generate_domain_analysis(),
            self._generate_social_media_investigation(),
            self._generate_document_analysis(),
            self._generate_geospatial_verification()
        ]
    
    def _generate_person_investigation(self) -> OSINTScenario:
        """Generate Person-of-Interest Investigation scenario"""
        steps = [
            ScenarioStep(
                id="poi_step_1",
                title="Initial Information Gathering",
                description="Start with basic information about the person of interest",
                step_type=StepType.SEARCH,
                instructions=[
                    "Navigate to the Entity Search page",
                    "Enter the person's name: 'Alex Thompson'",
                    "Select 'Person' from the entity type filter",
                    "Execute the search and review initial results"
                ],
                expected_actions=[
                    "click_entity_search",
                    "type_person_name",
                    "select_person_filter",
                    "click_search_button"
                ],
                hints=[
                    "Use quotes around the full name for exact matches",
                    "Check if there are multiple people with the same name",
                    "Note any immediate red flags in the results"
                ],
                success_criteria={
                    "search_executed": True,
                    "results_count": ">0",
                    "person_entities_found": True
                },
                estimated_time_minutes=5,
                tools_required=["entity_search", "person_filter"],
                data_inputs={"person_name": "Alex Thompson"},
                expected_outputs={"search_results": "person_entities", "confidence_scores": "numeric"},
                learning_objectives=[
                    "Learn to perform basic person searches",
                    "Understand entity filtering",
                    "Interpret search result confidence scores"
                ],
                common_mistakes=[
                    "Not using entity type filters",
                    "Ignoring confidence scores",
                    "Searching too broadly initially"
                ],
                next_step_conditions={"results_found": "poi_step_2", "no_results": "poi_step_1b"}
            ),
            ScenarioStep(
                id="poi_step_2",
                title="Social Media Profile Discovery",
                description="Expand search to social media platforms",
                step_type=StepType.ANALYSIS,
                instructions=[
                    "Select the most relevant person entity from search results",
                    "Open the entity detail panel",
                    "Navigate to 'Social Media' tab",
                    "Run social media discovery for all platforms",
                    "Review and validate discovered profiles"
                ],
                expected_actions=[
                    "select_person_entity",
                    "open_entity_details",
                    "click_social_media_tab",
                    "run_social_discovery",
                    "validate_profiles"
                ],
                hints=[
                    "Look for profile pictures that match",
                    "Check for consistent usernames across platforms",
                    "Verify location information consistency",
                    "Note profile creation dates and activity levels"
                ],
                success_criteria={
                    "social_profiles_found": ">0",
                    "profiles_validated": True,
                    "cross_platform_analysis": True
                },
                estimated_time_minutes=10,
                tools_required=["social_media_discovery", "profile_validator"],
                data_inputs={"person_entity": "selected_entity"},
                expected_outputs={"social_profiles": "list", "validation_scores": "numeric"},
                learning_objectives=[
                    "Learn social media discovery techniques",
                    "Practice profile validation methods",
                    "Understand cross-platform correlation"
                ],
                common_mistakes=[
                    "Not validating profile ownership",
                    "Assuming all profiles belong to the same person",
                    "Ignoring metadata inconsistencies"
                ],
                next_step_conditions={"profiles_found": "poi_step_3", "no_profiles": "poi_step_2b"}
            ),
            ScenarioStep(
                id="poi_step_3",
                title="Network Analysis",
                description="Map connections and relationships",
                step_type=StepType.ANALYSIS,
                instructions=[
                    "Open the Graph View for the person entity",
                    "Expand connections to show immediate network",
                    "Identify key connections (family, colleagues, associates)",
                    "Run community detection to find clusters",
                    "Analyze relationship strengths and patterns"
                ],
                expected_actions=[
                    "open_graph_view",
                    "expand_connections",
                    "identify_key_connections",
                    "run_community_detection",
                    "analyze_relationships"
                ],
                hints=[
                    "Look for central nodes in the network",
                    "Pay attention to relationship types",
                    "Notice unusual connection patterns",
                    "Check for isolated sub-networks"
                ],
                success_criteria={
                    "graph_view_opened": True,
                    "connections_expanded": True,
                    "communities_detected": ">0",
                    "key_connections_identified": ">2"
                },
                estimated_time_minutes=15,
                tools_required=["graph_visualization", "community_detection", "network_analysis"],
                data_inputs={"person_entity": "selected_entity"},
                expected_outputs={"network_graph": "graph_data", "communities": "list", "key_connections": "list"},
                learning_objectives=[
                    "Master graph visualization techniques",
                    "Understand network analysis concepts",
                    "Learn to identify important relationships"
                ],
                common_mistakes=[
                    "Not expanding the network far enough",
                    "Ignoring weak but important connections",
                    "Focusing only on direct connections"
                ],
                next_step_conditions={"analysis_complete": "poi_step_4"}
            ),
            ScenarioStep(
                id="poi_step_4",
                title="Digital Footprint Analysis",
                description="Analyze online presence and activities",
                step_type=StepType.ANALYSIS,
                instructions=[
                    "Navigate to the Timeline view",
                    "Review chronological activity across platforms",
                    "Identify patterns in posting behavior",
                    "Analyze content themes and sentiment",
                    "Look for location check-ins and travel patterns"
                ],
                expected_actions=[
                    "open_timeline_view",
                    "review_activity_chronology",
                    "identify_posting_patterns",
                    "analyze_content_sentiment",
                    "map_location_data"
                ],
                hints=[
                    "Look for gaps in activity (possible explanations)",
                    "Notice changes in posting behavior over time",
                    "Pay attention to location data privacy settings",
                    "Check for automated vs. manual posts"
                ],
                success_criteria={
                    "timeline_analyzed": True,
                    "patterns_identified": ">0",
                    "sentiment_analysis_complete": True,
                    "location_patterns_mapped": True
                },
                estimated_time_minutes=12,
                tools_required=["timeline_analysis", "sentiment_analysis", "geolocation_mapping"],
                data_inputs={"social_profiles": "validated_profiles"},
                expected_outputs={"activity_timeline": "chronological_data", "behavior_patterns": "analysis", "location_history": "geographic_data"},
                learning_objectives=[
                    "Learn timeline analysis techniques",
                    "Understand behavioral pattern recognition",
                    "Master geolocation correlation"
                ],
                common_mistakes=[
                    "Not considering timezone differences",
                    "Misinterpreting automated posts",
                    "Ignoring privacy setting changes over time"
                ],
                next_step_conditions={"analysis_complete": "poi_step_5"}
            ),
            ScenarioStep(
                id="poi_step_5",
                title="Risk Assessment and Report Generation",
                description="Compile findings and assess potential risks",
                step_type=StepType.VERIFICATION,
                instructions=[
                    "Open the Risk Assessment module",
                    "Input all discovered information",
                    "Run automated risk scoring algorithms",
                    "Review and adjust risk factors manually",
                    "Generate a comprehensive investigation report"
                ],
                expected_actions=[
                    "open_risk_assessment",
                    "input_investigation_data",
                    "run_risk_scoring",
                    "review_risk_factors",
                    "generate_report"
                ],
                hints=[
                    "Consider both digital and physical risks",
                    "Weight recent activities more heavily",
                    "Include uncertainty factors in assessment",
                    "Document all assumptions made"
                ],
                success_criteria={
                    "risk_assessment_complete": True,
                    "risk_score_calculated": True,
                    "report_generated": True,
                    "findings_documented": True
                },
                estimated_time_minutes=18,
                tools_required=["risk_assessment", "report_generator", "documentation_tools"],
                data_inputs={"all_investigation_data": "compiled_findings"},
                expected_outputs={"risk_score": "numeric", "investigation_report": "document", "recommendations": "list"},
                learning_objectives=[
                    "Learn risk assessment methodologies",
                    "Master report generation techniques",
                    "Understand investigation documentation"
                ],
                common_mistakes=[
                    "Not considering all risk factors",
                    "Over-relying on automated scoring",
                    "Incomplete documentation"
                ],
                next_step_conditions={"assessment_complete": "poi_complete"}
            )
        ]
        
        return OSINTScenario(
            id="scenario_person_investigation",
            title="Person of Interest Investigation",
            description="Complete investigation of an individual using multiple OSINT techniques",
            scenario_type=ScenarioType.PERSON_INVESTIGATION,
            difficulty=DifficultyLevel.INTERMEDIATE,
            estimated_duration_minutes=60,
            learning_objectives=[
                "Master person-focused OSINT techniques",
                "Learn to correlate information across multiple sources",
                "Understand privacy and ethical considerations",
                "Develop systematic investigation methodologies",
                "Practice risk assessment and reporting"
            ],
            prerequisites=[
                "Basic understanding of OSINT principles",
                "Familiarity with social media platforms",
                "Knowledge of privacy laws and ethical guidelines"
            ],
            tools_required=[
                "Entity Search", "Social Media Discovery", "Graph Visualization",
                "Timeline Analysis", "Risk Assessment", "Report Generator"
            ],
            steps=steps,
            background_story="""
            You are an OSINT analyst working for a cybersecurity firm. Your client, a large corporation, 
            has received several threatening emails from someone claiming to be 'Alex Thompson'. The 
            emails contain specific details about the company's operations that suggest insider knowledge. 
            
            Your task is to investigate this person to determine:
            1. Their real identity and background
            2. Possible connections to the company
            3. Level of threat they might pose
            4. Recommended security measures
            
            Remember to work within legal and ethical boundaries, using only publicly available information.
            """,
            success_metrics={
                "completion_rate": "percentage of steps completed",
                "accuracy_score": "correctness of findings",
                "time_efficiency": "completion time vs. estimated time",
                "methodology_score": "adherence to best practices"
            },
            evaluation_criteria=[
                "Thoroughness of investigation",
                "Accuracy of information validation",
                "Quality of risk assessment",
                "Clarity of final report",
                "Ethical compliance throughout process"
            ],
            additional_resources=[
                {"title": "OSINT Person Investigation Guide", "url": "/docs/person-investigation"},
                {"title": "Social Media Analysis Best Practices", "url": "/docs/social-media-analysis"},
                {"title": "Risk Assessment Methodologies", "url": "/docs/risk-assessment"},
                {"title": "Legal and Ethical Guidelines", "url": "/docs/ethics"}
            ],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
    
    def _generate_domain_analysis(self) -> OSINTScenario:
        """Generate Domain/Infrastructure Analysis scenario"""
        steps = [
            ScenarioStep(
                id="domain_step_1",
                title="Initial Domain Reconnaissance",
                description="Gather basic information about the target domain",
                step_type=StepType.SEARCH,
                instructions=[
                    "Navigate to the Domain Analysis tool",
                    "Enter the target domain: 'suspicious-corp.com'",
                    "Run basic domain information lookup",
                    "Review WHOIS data and registration details"
                ],
                expected_actions=[
                    "open_domain_analysis",
                    "enter_domain_name",
                    "run_whois_lookup",
                    "review_registration_data"
                ],
                hints=[
                    "Pay attention to registration dates and patterns",
                    "Note any privacy protection services",
                    "Check for suspicious registration details",
                    "Look for recently registered domains"
                ],
                success_criteria={
                    "domain_lookup_complete": True,
                    "whois_data_retrieved": True,
                    "registration_analysis_done": True
                },
                estimated_time_minutes=5,
                tools_required=["domain_analysis", "whois_lookup"],
                data_inputs={"domain": "suspicious-corp.com"},
                expected_outputs={"whois_data": "registration_info", "domain_age": "temporal_data"},
                learning_objectives=[
                    "Learn domain reconnaissance techniques",
                    "Understand WHOIS data interpretation",
                    "Recognize suspicious registration patterns"
                ],
                common_mistakes=[
                    "Not checking domain history",
                    "Ignoring privacy-protected registrations",
                    "Missing registration pattern analysis"
                ],
                next_step_conditions={"lookup_complete": "domain_step_2"}
            ),
            ScenarioStep(
                id="domain_step_2",
                title="Subdomain Discovery",
                description="Identify all subdomains associated with the target",
                step_type=StepType.ANALYSIS,
                instructions=[
                    "Use the Subdomain Discovery tool",
                    "Run comprehensive subdomain enumeration",
                    "Analyze discovered subdomains for patterns",
                    "Check for development, staging, or admin subdomains"
                ],
                expected_actions=[
                    "open_subdomain_discovery",
                    "run_subdomain_enumeration",
                    "analyze_subdomain_patterns",
                    "identify_sensitive_subdomains"
                ],
                hints=[
                    "Look for common development subdomain patterns",
                    "Check for administrative interfaces",
                    "Note any abandoned or misconfigured subdomains",
                    "Pay attention to SSL certificate variations"
                ],
                success_criteria={
                    "subdomains_discovered": ">5",
                    "pattern_analysis_complete": True,
                    "sensitive_subdomains_identified": True
                },
                estimated_time_minutes=10,
                tools_required=["subdomain_discovery", "pattern_analysis"],
                data_inputs={"main_domain": "suspicious-corp.com"},
                expected_outputs={"subdomain_list": "enumerated_subdomains", "risk_assessment": "subdomain_risks"},
                learning_objectives=[
                    "Master subdomain discovery techniques",
                    "Learn to identify risky subdomain patterns",
                    "Understand infrastructure mapping"
                ],
                common_mistakes=[
                    "Using only one discovery method",
                    "Not checking subdomain accessibility",
                    "Ignoring wildcard DNS configurations"
                ],
                next_step_conditions={"discovery_complete": "domain_step_3"}
            ),
            ScenarioStep(
                id="domain_step_3",
                title="Infrastructure Mapping",
                description="Map the complete technical infrastructure",
                step_type=StepType.ANALYSIS,
                instructions=[
                    "Run DNS analysis for all discovered domains",
                    "Identify IP addresses and hosting providers",
                    "Map CDN and load balancer configurations",
                    "Analyze SSL certificate patterns and chains"
                ],
                expected_actions=[
                    "run_dns_analysis",
                    "identify_hosting_infrastructure",
                    "map_cdn_configuration",
                    "analyze_ssl_certificates"
                ],
                hints=[
                    "Look for shared hosting indicators",
                    "Check for geographic distribution patterns",
                    "Note any suspicious certificate authorities",
                    "Identify potential single points of failure"
                ],
                success_criteria={
                    "dns_analysis_complete": True,
                    "hosting_infrastructure_mapped": True,
                    "ssl_analysis_complete": True
                },
                estimated_time_minutes=15,
                tools_required=["dns_analysis", "infrastructure_mapping", "ssl_analyzer"],
                data_inputs={"domains_and_subdomains": "discovered_domains"},
                expected_outputs={"infrastructure_map": "network_topology", "hosting_analysis": "provider_info"},
                learning_objectives=[
                    "Learn infrastructure analysis techniques",
                    "Understand hosting pattern recognition",
                    "Master SSL certificate analysis"
                ],
                common_mistakes=[
                    "Not checking for shared hosting risks",
                    "Missing CDN configuration analysis",
                    "Ignoring certificate chain validation"
                ],
                next_step_conditions={"mapping_complete": "domain_step_4"}
            ),
            ScenarioStep(
                id="domain_step_4",
                title="Security Assessment",
                description="Evaluate security posture and vulnerabilities",
                step_type=StepType.ANALYSIS,
                instructions=[
                    "Run security header analysis",
                    "Check for exposed administrative interfaces",
                    "Analyze email security configurations (SPF, DKIM, DMARC)",
                    "Test for common web application vulnerabilities"
                ],
                expected_actions=[
                    "analyze_security_headers",
                    "scan_admin_interfaces",
                    "check_email_security",
                    "run_vulnerability_scan"
                ],
                hints=[
                    "Look for missing security headers",
                    "Check for default credentials on admin interfaces",
                    "Verify email authentication mechanisms",
                    "Note any outdated software versions"
                ],
                success_criteria={
                    "security_analysis_complete": True,
                    "vulnerabilities_identified": True,
                    "email_security_assessed": True
                },
                estimated_time_minutes=20,
                tools_required=["security_scanner", "vulnerability_assessment", "email_security_checker"],
                data_inputs={"infrastructure_data": "mapped_infrastructure"},
                expected_outputs={"security_report": "vulnerability_list", "risk_score": "security_rating"},
                learning_objectives=[
                    "Learn security assessment techniques",
                    "Understand common vulnerability patterns",
                    "Master email security analysis"
                ],
                common_mistakes=[
                    "Not checking for exposed backup files",
                    "Missing email spoofing vulnerabilities",
                    "Overlooking subdomain security issues"
                ],
                next_step_conditions={"assessment_complete": "domain_step_5"}
            ),
            ScenarioStep(
                id="domain_step_5",
                title="Threat Intelligence and Reporting",
                description="Correlate findings with threat intelligence and generate report",
                step_type=StepType.VERIFICATION,
                instructions=[
                    "Check domains against threat intelligence feeds",
                    "Look for indicators of compromise (IoCs)",
                    "Analyze hosting provider reputation",
                    "Generate comprehensive infrastructure assessment report"
                ],
                expected_actions=[
                    "query_threat_intelligence",
                    "check_iocs",
                    "analyze_provider_reputation",
                    "generate_assessment_report"
                ],
                hints=[
                    "Cross-reference with known malicious infrastructures",
                    "Check for bulletproof hosting indicators",
                    "Look for recent security incidents",
                    "Include remediation recommendations"
                ],
                success_criteria={
                    "threat_intel_checked": True,
                    "ioc_analysis_complete": True,
                    "final_report_generated": True
                },
                estimated_time_minutes=15,
                tools_required=["threat_intelligence", "ioc_checker", "report_generator"],
                data_inputs={"complete_analysis_data": "all_findings"},
                expected_outputs={"threat_assessment": "intelligence_report", "infrastructure_report": "technical_document"},
                learning_objectives=[
                    "Learn threat intelligence correlation",
                    "Understand IoC analysis",
                    "Master technical report writing"
                ],
                common_mistakes=[
                    "Not checking multiple threat intel sources",
                    "Missing historical compromise data",
                    "Inadequate remediation recommendations"
                ],
                next_step_conditions={"reporting_complete": "domain_complete"}
            )
        ]
        
        return OSINTScenario(
            id="scenario_domain_analysis",
            title="Suspicious Domain Infrastructure Analysis",
            description="Complete technical analysis of a potentially malicious domain",
            scenario_type=ScenarioType.DOMAIN_ANALYSIS,
            difficulty=DifficultyLevel.ADVANCED,
            estimated_duration_minutes=65,
            learning_objectives=[
                "Master domain reconnaissance techniques",
                "Learn infrastructure mapping and analysis",
                "Understand security assessment methodologies",
                "Practice threat intelligence correlation",
                "Develop technical reporting skills"
            ],
            prerequisites=[
                "Understanding of DNS and web infrastructure",
                "Basic knowledge of cybersecurity concepts",
                "Familiarity with network analysis tools"
            ],
            tools_required=[
                "Domain Analysis", "Subdomain Discovery", "DNS Analysis",
                "Security Scanner", "Threat Intelligence", "Report Generator"
            ],
            steps=steps,
            background_story="""
            Your organization's security team has detected suspicious network traffic pointing to 
            'suspicious-corp.com'. Initial analysis suggests this domain might be part of a 
            command and control infrastructure for a potential cyberattack.
            
            Your mission is to:
            1. Thoroughly analyze the domain's infrastructure
            2. Identify potential security vulnerabilities
            3. Assess the threat level
            4. Provide actionable intelligence for blocking/monitoring
            
            Time is critical as the domain appears to be actively used in ongoing campaigns.
            """,
            success_metrics={
                "infrastructure_coverage": "percentage of infrastructure mapped",
                "vulnerability_detection": "number of vulnerabilities found",
                "threat_correlation": "accuracy of threat intelligence matching",
                "report_quality": "completeness and clarity of final report"
            },
            evaluation_criteria=[
                "Completeness of infrastructure discovery",
                "Accuracy of security assessment",
                "Quality of threat intelligence correlation",
                "Actionability of recommendations",
                "Technical accuracy of findings"
            ],
            additional_resources=[
                {"title": "Domain Analysis Methodology", "url": "/docs/domain-analysis"},
                {"title": "Infrastructure Security Assessment", "url": "/docs/infra-security"},
                {"title": "Threat Intelligence Integration", "url": "/docs/threat-intel"},
                {"title": "Technical Report Writing", "url": "/docs/technical-reports"}
            ],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
    
    def _generate_social_media_investigation(self) -> OSINTScenario:
        """Generate Social Media Investigation scenario"""
        # Implementation for social media scenario...
        return OSINTScenario(
            id="scenario_social_media",
            title="Social Media Disinformation Investigation",
            description="Investigate potential disinformation campaign across social platforms",
            scenario_type=ScenarioType.SOCIAL_MEDIA,
            difficulty=DifficultyLevel.INTERMEDIATE,
            estimated_duration_minutes=45,
            learning_objectives=["Social media analysis", "Disinformation detection"],
            prerequisites=["Social media familiarity"],
            tools_required=["Social Media Analyzer", "Content Verification"],
            steps=[],  # Simplified for brevity
            background_story="Investigate suspicious social media activity...",
            success_metrics={},
            evaluation_criteria=[],
            additional_resources=[],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
    
    def _generate_document_analysis(self) -> OSINTScenario:
        """Generate Document Analysis scenario"""
        # Implementation for document analysis scenario...
        return OSINTScenario(
            id="scenario_document_analysis",
            title="Leaked Document Verification",
            description="Analyze and verify the authenticity of leaked documents",
            scenario_type=ScenarioType.DOCUMENT_ANALYSIS,
            difficulty=DifficultyLevel.ADVANCED,
            estimated_duration_minutes=50,
            learning_objectives=["Document forensics", "Authenticity verification"],
            prerequisites=["Document analysis basics"],
            tools_required=["Document Analyzer", "Metadata Extractor"],
            steps=[],  # Simplified for brevity
            background_story="Verify leaked corporate documents...",
            success_metrics={},
            evaluation_criteria=[],
            additional_resources=[],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
    
    def _generate_geospatial_verification(self) -> OSINTScenario:
        """Generate Geospatial Verification scenario"""
        # Implementation for geospatial scenario...
        return OSINTScenario(
            id="scenario_geospatial",
            title="Event Location Verification",
            description="Verify the location and timing of reported events using geospatial analysis",
            scenario_type=ScenarioType.GEOSPATIAL_VERIFICATION,
            difficulty=DifficultyLevel.BEGINNER,
            estimated_duration_minutes=30,
            learning_objectives=["Geospatial analysis", "Event verification"],
            prerequisites=["Basic geography knowledge"],
            tools_required=["Geospatial Analyzer", "Satellite Imagery"],
            steps=[],  # Simplified for brevity
            background_story="Verify location of reported incident...",
            success_metrics={},
            evaluation_criteria=[],
            additional_resources=[],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
    
    def get_scenario(self, scenario_id: str) -> Optional[OSINTScenario]:
        """Get specific scenario by ID"""
        for scenario in self.scenarios:
            if scenario.id == scenario_id:
                return scenario
        return None
    
    def get_scenarios_by_difficulty(self, difficulty: DifficultyLevel) -> List[OSINTScenario]:
        """Get scenarios filtered by difficulty level"""
        return [s for s in self.scenarios if s.difficulty == difficulty]
    
    def get_scenarios_by_type(self, scenario_type: ScenarioType) -> List[OSINTScenario]:
        """Get scenarios filtered by type"""
        return [s for s in self.scenarios if s.scenario_type == scenario_type]
    
    def export_scenarios_to_json(self, file_path: str):
        """Export all scenarios to JSON file"""
        scenarios_dict = [asdict(scenario) for scenario in self.scenarios]
        with open(file_path, 'w') as f:
            json.dump(scenarios_dict, f, indent=2, default=str)
    
    def generate_scenario_test_data(self) -> Dict[str, Any]:
        """Generate test data for scenario validation"""
        return {
            "test_entities": [
                {"name": "Alex Thompson", "type": "person", "confidence": 0.95},
                {"name": "suspicious-corp.com", "type": "domain", "confidence": 0.98}
            ],
            "test_social_profiles": [
                {"platform": "twitter", "username": "athompson2023", "verified": False},
                {"platform": "linkedin", "username": "alex-thompson-analyst", "verified": True}
            ],
            "test_domain_data": {
                "whois": {"registrar": "NameCheap", "creation_date": "2023-01-15"},
                "subdomains": ["admin.suspicious-corp.com", "api.suspicious-corp.com"],
                "ip_addresses": ["192.168.1.100", "203.0.113.42"]
            },
            "test_documents": [
                {"filename": "leaked_memo.pdf", "size": 245000, "hash": "abc123def456"}
            ],
            "test_locations": [
                {"coordinates": [40.7589, -73.9851], "address": "Times Square, NYC"}
            ]
        }

# Usage example
if __name__ == "__main__":
    generator = OSINTScenarioGenerator()
    
    # Export all scenarios
    generator.export_scenarios_to_json("osint_scenarios.json")
    
    # Get specific scenario
    person_scenario = generator.get_scenario("scenario_person_investigation")
    if person_scenario:
        print(f"Scenario: {person_scenario.title}")
        print(f"Steps: {len(person_scenario.steps)}")
        print(f"Estimated time: {person_scenario.estimated_duration_minutes} minutes")
