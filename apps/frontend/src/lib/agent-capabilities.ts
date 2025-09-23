import { 
  Search,
  Network,
  Shield,
  MapPin,
  User,
  Cpu
} from 'lucide-react';
import { AgentCapability } from '../panels/types';

export const AGENT_CAPABILITIES: AgentCapability[] = [
  {
    id: 'research_assistant',
    name: 'research_assistant',
    displayName: 'Research Assistant',
    description: 'Comprehensive research across multiple data sources and databases',
    icon: Search,
    color: 'blue',
    tools: ['web_search', 'database_query', 'document_analysis', 'fact_checking'],
    expertise: ['research', 'analysis', 'fact_checking', 'data_mining']
  },
  {
    id: 'graph_analyst', 
    name: 'graph_analyst',
    displayName: 'Graph Analyst',
    description: 'Network analysis, relationship mapping, and connection discovery',
    icon: Network,
    color: 'purple',
    tools: ['neo4j_query', 'network_analysis', 'path_finding', 'community_detection'],
    expertise: ['network_analysis', 'graph_theory', 'relationship_mapping', 'pattern_recognition']
  },
  {
    id: 'security_analyst',
    name: 'security_analyst', 
    displayName: 'Security Analyst',
    description: 'Threat assessment, risk analysis, and security intelligence',
    icon: Shield,
    color: 'red',
    tools: ['threat_intel', 'vulnerability_scan', 'risk_assessment', 'iot_analysis'],
    expertise: ['cybersecurity', 'threat_analysis', 'risk_management', 'forensics']
  },
  {
    id: 'geospatial_analyst',
    name: 'geospatial_analyst',
    displayName: 'Geospatial Analyst', 
    description: 'Location intelligence, spatial analysis, and geographic insights',
    icon: MapPin,
    color: 'green',
    tools: ['gis_analysis', 'location_intel', 'spatial_query', 'route_analysis'],
    expertise: ['gis', 'spatial_analysis', 'geolocation', 'mapping']
  },
  {
    id: 'InvestigatePerson',
    name: 'InvestigatePerson',
    displayName: 'Person Investigation',
    description: 'Deep person profiling, background checks, and social network analysis',
    icon: User,
    color: 'indigo',
    tools: ['social_media', 'public_records', 'network_mapping', 'background_check'],
    expertise: ['osint', 'social_media_analysis', 'background_investigation', 'person_profiling']
  },
  {
    id: 'FinancialRiskAssistant',
    name: 'FinancialRiskAssistant',
    displayName: 'Financial Risk Analysis',
    description: 'Financial pattern analysis, risk modeling, and compliance assessment',
    icon: Cpu,
    color: 'amber',
    tools: ['transaction_analysis', 'risk_modeling', 'compliance_check', 'fraud_detection'],
    expertise: ['financial_analysis', 'risk_modeling', 'compliance', 'fraud_detection']
  }
];
