// Legacy Playbooks API Route Handler
// Provides backward compatibility for existing playbook functionality

import type { NextApiRequest, NextApiResponse } from 'next';
import { getAgentApis } from '@/lib/config';
import { getCapabilityById } from '@/lib/agent-config';

interface PlaybookRunRequest {
  name: string;
  params?: {
    q?: string;
    [key: string]: any;
  };
}

interface PlaybookRunResponse {
  result: string;
  status: 'success' | 'error';
  details?: any;
  execution_time?: number;
  tools_used?: string[];
  error?: string;
}

// Legacy playbook name mapping to new capabilities
const PLAYBOOK_MAPPING: { [key: string]: string } = {
  'InvestigatePerson': 'person_investigator',
  'FinancialRiskAssistant': 'financial_analyst',
  'ResearchAssistant': 'research_assistant',
  'GraphAnalyst': 'graph_analyst',
  'SecurityAnalyst': 'security_analyst',
  'GeospatialAnalyst': 'geospatial_analyst'
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<PlaybookRunResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ 
      result: '', 
      status: 'error', 
      error: 'Method not allowed' 
    });
  }

  try {
    const apis = getAgentApis();
    const { name, params = {} }: PlaybookRunRequest = req.body;

    if (!name) {
      return res.status(400).json({
        result: '',
        status: 'error',
        error: 'Playbook name is required'
      });
    }

    // Map legacy playbook name to new capability
    const capabilityId = PLAYBOOK_MAPPING[name] || name.toLowerCase().replace(/([A-Z])/g, '_$1').substring(1);
    const capability = getCapabilityById(capabilityId);

    if (!capability) {
      return res.status(404).json({
        result: '',
        status: 'error',
        error: `Playbook '${name}' not found. Available playbooks: ${Object.keys(PLAYBOOK_MAPPING).join(', ')}`
      });
    }

    // Convert legacy params format to new context format
    const context = params.q || params.query || params.input || `Execute ${capability.displayName} analysis`;
    
    // Prepare request for capability execution
    const requestBody = {
      capability: capabilityId,
      agent_type: capability.name,
      context,
      session_id: `playbook_${Date.now()}`,
      tools: capability.tools,
      max_iterations: capability.maxIterations || 10
    };

    const startTime = Date.now();

    // Execute via capabilities API
    const response = await fetch(`${apis.primary}/capabilities/run`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'InfoTerminal-Frontend-Playbooks'
      },
      body: JSON.stringify(requestBody),
      signal: AbortSignal.timeout(120000) // 2 minute timeout for playbooks
    });

    const executionTime = Date.now() - startTime;

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Playbook execution error:', response.status, errorText);
      
      return res.status(response.status).json({
        result: '',
        status: 'error',
        error: `Playbook execution failed: ${response.status} ${response.statusText}`,
        execution_time: executionTime
      });
    }

    const data = await response.json();
    
    // Format response for legacy compatibility
    const playbookResponse: PlaybookRunResponse = {
      result: data.result || data.response || `${capability.displayName} completed successfully`,
      status: 'success',
      details: {
        capability: capability.displayName,
        steps: data.steps || [],
        references: data.references
      },
      execution_time: data.execution_time || executionTime,
      tools_used: data.tools_used || capability.tools
    };

    return res.status(200).json(playbookResponse);

  } catch (error: any) {
    console.error('Playbooks API error:', error);
    
    let errorMessage = 'Internal server error';
    let statusCode = 500;
    
    if (error.name === 'TimeoutError') {
      errorMessage = 'Playbook execution timeout';
      statusCode = 408;
    } else if (error.name === 'AbortError') {
      errorMessage = 'Playbook execution was aborted';
      statusCode = 408;
    }
    
    return res.status(statusCode).json({
      result: '',
      status: 'error',
      error: errorMessage
    });
  }
}
