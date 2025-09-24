// Agent Configuration Module for InfoTerminal
// Centralized configuration for AI agent capabilities and services

import {
  Search,
  Network,
  Shield,
  MapPin,
  User,
  Cpu,
  FileText,
  Camera,
  Globe,
  Brain,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

export interface AgentCapability {
  id: string;
  name: string;
  displayName: string;
  description: string;
  icon: LucideIcon;
  color: string;
  tools: string[];
  category: "analysis" | "investigation" | "security" | "intelligence";
  expertise: string[];
  defaultModel?: string;
  maxIterations?: number;
}

export interface AgentEndpoint {
  name: string;
  url: string;
  healthPath: string;
  timeout: number;
  retries: number;
}

export interface AgentConfiguration {
  capabilities: AgentCapability[];
  endpoints: AgentEndpoint[];
  defaults: {
    maxIterations: number;
    includeSteps: boolean;
    timeout: number;
    defaultCapability: string;
  };
  features: {
    multiAgent: boolean;
    workflows: boolean;
    toolRestrictions: boolean;
    sessionPersistence: boolean;
  };
}

// Core Agent Capabilities - Enhanced with more specialized agents
export const AGENT_CAPABILITIES: AgentCapability[] = [
  {
    id: "research_assistant",
    name: "research_assistant",
    displayName: "Research Assistant",
    description:
      "Comprehensive research across multiple data sources, fact-checking, and information synthesis",
    icon: Search,
    color: "blue",
    tools: [
      "web_search",
      "database_query",
      "document_analysis",
      "fact_checking",
      "citation_lookup",
    ],
    category: "analysis",
    expertise: [
      "open source intelligence",
      "fact verification",
      "information synthesis",
      "source analysis",
    ],
    maxIterations: 15,
  },
  {
    id: "graph_analyst",
    name: "graph_analyst",
    displayName: "Graph Analyst",
    description:
      "Advanced network analysis, relationship mapping, and connection discovery using graph databases",
    icon: Network,
    color: "purple",
    tools: [
      "neo4j_query",
      "network_analysis",
      "path_finding",
      "community_detection",
      "centrality_analysis",
    ],
    category: "analysis",
    expertise: [
      "social network analysis",
      "entity relationships",
      "network topology",
      "graph algorithms",
    ],
    maxIterations: 12,
  },
  {
    id: "security_analyst",
    name: "security_analyst",
    displayName: "Security Analyst",
    description:
      "Cybersecurity threat assessment, risk analysis, and security intelligence gathering",
    icon: Shield,
    color: "red",
    tools: [
      "threat_intel",
      "vulnerability_scan",
      "risk_assessment",
      "iot_analysis",
      "malware_analysis",
    ],
    category: "security",
    expertise: [
      "cyber threats",
      "vulnerability assessment",
      "risk modeling",
      "security frameworks",
    ],
    maxIterations: 10,
  },
  {
    id: "geospatial_analyst",
    name: "geospatial_analyst",
    displayName: "Geospatial Analyst",
    description:
      "Location intelligence, spatial analysis, geographic insights, and terrain assessment",
    icon: MapPin,
    color: "green",
    tools: [
      "gis_analysis",
      "location_intel",
      "spatial_query",
      "route_analysis",
      "satellite_imagery",
    ],
    category: "intelligence",
    expertise: [
      "geographic intelligence",
      "spatial patterns",
      "location correlation",
      "terrain analysis",
    ],
    maxIterations: 8,
  },
  {
    id: "person_investigator",
    name: "person_investigator",
    displayName: "Person Investigator",
    description:
      "Deep person profiling, background investigation, social network analysis, and identity verification",
    icon: User,
    color: "indigo",
    tools: [
      "social_media",
      "public_records",
      "network_mapping",
      "background_check",
      "identity_verification",
    ],
    category: "investigation",
    expertise: [
      "background checks",
      "social media analysis",
      "identity research",
      "person profiling",
    ],
    maxIterations: 20,
  },
  {
    id: "financial_analyst",
    name: "financial_analyst",
    displayName: "Financial Analyst",
    description:
      "Financial pattern analysis, transaction investigation, risk modeling, and compliance assessment",
    icon: Cpu,
    color: "amber",
    tools: [
      "transaction_analysis",
      "risk_modeling",
      "compliance_check",
      "fraud_detection",
      "financial_intel",
    ],
    category: "investigation",
    expertise: [
      "financial crime",
      "transaction patterns",
      "money laundering",
      "regulatory compliance",
    ],
    maxIterations: 15,
  },
  {
    id: "document_analyst",
    name: "document_analyst",
    displayName: "Document Analyst",
    description:
      "Advanced document processing, content extraction, metadata analysis, and document forensics",
    icon: FileText,
    color: "gray",
    tools: [
      "document_parsing",
      "metadata_extraction",
      "content_analysis",
      "document_similarity",
      "text_mining",
    ],
    category: "analysis",
    expertise: [
      "document forensics",
      "content analysis",
      "information extraction",
      "document classification",
    ],
    maxIterations: 8,
  },
  {
    id: "media_analyst",
    name: "media_analyst",
    displayName: "Media Analyst",
    description:
      "Image and video analysis, media forensics, reverse image search, and visual intelligence",
    icon: Camera,
    color: "pink",
    tools: [
      "image_analysis",
      "reverse_image_search",
      "video_analysis",
      "media_forensics",
      "facial_recognition",
    ],
    category: "intelligence",
    expertise: ["image forensics", "video analysis", "media verification", "visual intelligence"],
    maxIterations: 10,
  },
  {
    id: "web_investigator",
    name: "web_investigator",
    displayName: "Web Investigator",
    description:
      "Deep web research, domain analysis, website forensics, and digital footprint investigation",
    icon: Globe,
    color: "teal",
    tools: ["web_crawling", "domain_analysis", "wayback_machine", "dns_analysis", "whois_lookup"],
    category: "investigation",
    expertise: ["web forensics", "domain intelligence", "digital footprints", "website analysis"],
    maxIterations: 12,
  },
  {
    id: "ai_synthesizer",
    name: "ai_synthesizer",
    displayName: "AI Synthesizer",
    description:
      "Multi-source intelligence synthesis, pattern recognition, and advanced analytical reasoning",
    icon: Brain,
    color: "violet",
    tools: [
      "multi_agent_coordination",
      "pattern_recognition",
      "intelligence_synthesis",
      "analytical_reasoning",
    ],
    category: "intelligence",
    expertise: [
      "intelligence fusion",
      "pattern analysis",
      "strategic thinking",
      "analytical synthesis",
    ],
    maxIterations: 25,
  },
];

// Color mappings for UI consistency
export const CAPABILITY_COLORS = {
  blue: "bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-300 border-blue-200 dark:border-blue-900/30",
  purple:
    "bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-300 border-purple-200 dark:border-purple-900/30",
  red: "bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300 border-red-200 dark:border-red-900/30",
  green:
    "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300 border-green-200 dark:border-green-900/30",
  indigo:
    "bg-indigo-100 text-indigo-800 dark:bg-indigo-900/20 dark:text-indigo-300 border-indigo-200 dark:border-indigo-900/30",
  amber:
    "bg-amber-100 text-amber-800 dark:bg-amber-900/20 dark:text-amber-300 border-amber-200 dark:border-amber-900/30",
  gray: "bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-300 border-gray-200 dark:border-gray-900/30",
  pink: "bg-pink-100 text-pink-800 dark:bg-pink-900/20 dark:text-pink-300 border-pink-200 dark:border-pink-900/30",
  teal: "bg-teal-100 text-teal-800 dark:bg-teal-900/20 dark:text-teal-300 border-teal-200 dark:border-teal-900/30",
  violet:
    "bg-violet-100 text-violet-800 dark:bg-violet-900/20 dark:text-violet-300 border-violet-200 dark:border-violet-900/30",
};

// Agent Service Endpoints
export const AGENT_ENDPOINTS: AgentEndpoint[] = [
  {
    name: "agent-connector",
    url: process.env.NEXT_PUBLIC_AGENT_API || "http://localhost:8610",
    healthPath: "/healthz",
    timeout: 30000,
    retries: 3,
  },
  {
    name: "doc-entities",
    url: process.env.NEXT_PUBLIC_DOCENTITIES_API || "http://localhost:8613",
    healthPath: "/healthz",
    timeout: 15000,
    retries: 2,
  },
  {
    name: "flowise-connector",
    url: process.env.NEXT_PUBLIC_FLOWISE_API || "http://localhost:8620",
    healthPath: "/health",
    timeout: 20000,
    retries: 2,
  },
];

// Agent Configuration
export const AGENT_CONFIG: AgentConfiguration = {
  capabilities: AGENT_CAPABILITIES,
  endpoints: AGENT_ENDPOINTS,
  defaults: {
    maxIterations: parseInt(process.env.NEXT_PUBLIC_AGENT_MAX_ITERATIONS || "10"),
    includeSteps: process.env.NEXT_PUBLIC_AGENT_INCLUDE_STEPS === "true",
    timeout: parseInt(process.env.NEXT_PUBLIC_AGENT_TIMEOUT || "300000"),
    defaultCapability: process.env.NEXT_PUBLIC_AGENT_DEFAULT_TYPE || "research_assistant",
  },
  features: {
    multiAgent: process.env.NEXT_PUBLIC_FEATURE_MULTI_AGENT === "1",
    workflows: process.env.NEXT_PUBLIC_FEATURE_WORKFLOWS === "1",
    toolRestrictions: true,
    sessionPersistence: true,
  },
};

// Utility functions
export const getCapabilityById = (id: string): AgentCapability | undefined => {
  return AGENT_CAPABILITIES.find((cap) => cap.id === id);
};

export const getCapabilitiesByCategory = (
  category: AgentCapability["category"],
): AgentCapability[] => {
  return AGENT_CAPABILITIES.filter((cap) => cap.category === category);
};

export const isCapabilityEnabled = (capabilityId: string): boolean => {
  // Add any capability-specific feature flag logic here
  const capability = getCapabilityById(capabilityId);
  return !!capability;
};

export const getEndpointByName = (name: string): AgentEndpoint | undefined => {
  return AGENT_ENDPOINTS.find((endpoint) => endpoint.name === name);
};

export const getPrimaryEndpoint = (): AgentEndpoint => {
  return AGENT_ENDPOINTS[0]; // agent-connector is primary
};

// Agent health check utilities
export const checkAgentHealth = async (
  endpoint: AgentEndpoint,
): Promise<{
  healthy: boolean;
  responseTime?: number;
  error?: string;
}> => {
  const startTime = Date.now();

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), endpoint.timeout);

    const response = await fetch(`${endpoint.url}${endpoint.healthPath}`, {
      method: "GET",
      signal: controller.signal,
      headers: {
        Accept: "application/json",
      },
    });

    clearTimeout(timeoutId);
    const responseTime = Date.now() - startTime;

    return {
      healthy: response.ok,
      responseTime,
      error: response.ok ? undefined : `HTTP ${response.status}: ${response.statusText}`,
    };
  } catch (error) {
    const responseTime = Date.now() - startTime;
    return {
      healthy: false,
      responseTime,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
};

export const checkAllAgentHealth = async (): Promise<{
  [endpointName: string]: {
    healthy: boolean;
    responseTime?: number;
    error?: string;
  };
}> => {
  const results = await Promise.allSettled(
    AGENT_ENDPOINTS.map(async (endpoint) => ({
      name: endpoint.name,
      result: await checkAgentHealth(endpoint),
    })),
  );

  const healthStatus: { [key: string]: any } = {};

  results.forEach((result, index) => {
    if (result.status === "fulfilled") {
      healthStatus[result.value.name] = result.value.result;
    } else {
      healthStatus[AGENT_ENDPOINTS[index].name] = {
        healthy: false,
        error: "Health check failed",
      };
    }
  });

  return healthStatus;
};

export default AGENT_CONFIG;
