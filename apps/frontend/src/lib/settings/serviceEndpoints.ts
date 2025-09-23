import {
  Search,
  Database,
  Brain,
  Eye,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import type { EndpointSettings } from '@/lib/endpoints';

export interface ServiceEndpoint {
  key: keyof EndpointSettings;
  label: string;
  description: string;
  icon: LucideIcon;
  required: boolean;
  defaultPort?: string;
}

export const SERVICE_ENDPOINTS: ServiceEndpoint[] = [
  {
    key: "SEARCH_API",
    label: "Search API",
    description: "Full-text search and document indexing service",
    icon: Search,
    required: true,
    defaultPort: "8001"
  },
  {
    key: "GRAPH_API",
    label: "Graph Database API",
    description: "Neo4j graph database for relationship analysis",
    icon: Database,
    required: true,
    defaultPort: "7474"
  },
  {
    key: "DOCENTITIES_API",
    label: "Document Entities API",
    description: "NLP service for entity extraction and document processing",
    icon: Brain,
    required: true,
    defaultPort: "8003"
  },
  {
    key: "VIEWS_API",
    label: "Views API",
    description: "Data visualization and analytics service",
    icon: Eye,
    required: false,
    defaultPort: "8004"
  },
  {
    key: "NLP_API",
    label: "NLP Processing API",
    description: "Advanced natural language processing capabilities",
    icon: Brain,
    required: false,
    defaultPort: "8005"
  }
];

export interface EndpointSummary {
  total: number;
  configured: number;
  healthy: number;
}

export const calculateEndpointSummary = (endpoints: EndpointSettings): EndpointSummary => {
  const total = SERVICE_ENDPOINTS.length;
  const configured = SERVICE_ENDPOINTS.filter(ep => endpoints[ep.key]).length;
  
  // Health status would need to be implemented with actual health checks
  // For now, we return 0 as placeholder
  const healthy = 0;
  
  return { total, configured, healthy };
};
