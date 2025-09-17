// Agent API Index Route Handler
// Provides overview of available agent API endpoints and services

import type { NextApiRequest, NextApiResponse } from 'next';
import { AGENT_CAPABILITIES, AGENT_ENDPOINTS, AGENT_CONFIG } from '@/lib/agent-config';
import { getAgentApis, FEATURES } from '@/lib/config';

interface AgentAPIIndex {
  info: {
    service: string;
    version: string;
    description: string;
    timestamp: string;
  };
  endpoints: {
    [path: string]: {
      method: string;
      description: string;
      parameters?: string[];
    };
  };
  services: {
    name: string;
    url: string;
    description: string;
  }[];
  capabilities: {
    total: number;
    categories: string[];
    available: string[];
  };
  configuration: {
    features: typeof FEATURES;
    defaults: typeof AGENT_CONFIG.defaults;
  };
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<AgentAPIIndex | { error: string }>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const apis = getAgentApis();
    
    const response: AgentAPIIndex = {
      info: {
        service: 'InfoTerminal Agent API',
        version: '2.0.0',
        description: 'AI-powered investigation and analysis services',
        timestamp: new Date().toISOString()
      },
      endpoints: {
        '/api/agent': {
          method: 'GET',
          description: 'This API overview'
        },
        '/api/agent/chat': {
          method: 'POST',
          description: 'Chat with AI agents',
          parameters: ['messages', 'agent_type', 'session_id', 'max_iterations', 'include_steps']
        },
        '/api/agent/capabilities': {
          method: 'GET|POST',
          description: 'List capabilities (GET) or run capability (POST)',
          parameters: ['capability', 'context', 'session_id', 'tools']
        },
        '/api/agent/health': {
          method: 'GET',
          description: 'Health status of agent services'
        },
        '/api/agent/playbooks': {
          method: 'POST',
          description: 'Legacy playbook execution (backward compatibility)',
          parameters: ['name', 'params']
        }
      },
      services: AGENT_ENDPOINTS.map(endpoint => ({
        name: endpoint.name,
        url: endpoint.url,
        description: getServiceDescription(endpoint.name)
      })),
      capabilities: {
        total: AGENT_CAPABILITIES.length,
        categories: [...new Set(AGENT_CAPABILITIES.map(c => c.category))],
        available: AGENT_CAPABILITIES.map(c => c.id)
      },
      configuration: {
        features: FEATURES,
        defaults: AGENT_CONFIG.defaults
      }
    };

    return res.status(200).json(response);

  } catch (error: any) {
    console.error('Agent API index error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

function getServiceDescription(serviceName: string): string {
  const descriptions: { [key: string]: string } = {
    'agent-connector': 'Primary agent orchestration and chat interface',
    'doc-entities': 'Document processing and entity extraction',
    'flowise-connector': 'Flowise workflow integration for complex agent chains'
  };
  
  return descriptions[serviceName] || 'Agent service component';
}
