// Agent Health Check API Route Handler
// Provides health status for agent services

import type { NextApiRequest, NextApiResponse } from 'next';
import { checkAllAgentHealth, AGENT_ENDPOINTS } from '@/lib/agent-config';

interface HealthResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  services: {
    [serviceName: string]: {
      healthy: boolean;
      responseTime?: number;
      error?: string;
      lastCheck: string;
    };
  };
  summary: {
    total: number;
    healthy: number;
    unhealthy: number;
  };
  timestamp: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<HealthResponse>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({} as HealthResponse);
  }

  try {
    const healthResults = await checkAllAgentHealth();
    const timestamp = new Date().toISOString();
    
    // Transform health results
    const services: HealthResponse['services'] = {};
    
    Object.entries(healthResults).forEach(([serviceName, result]) => {
      services[serviceName] = {
        ...result,
        lastCheck: timestamp
      };
    });

    // Calculate summary
    const healthyCount = Object.values(services).filter(s => s.healthy).length;
    const totalCount = Object.keys(services).length;
    const unhealthyCount = totalCount - healthyCount;

    let status: 'healthy' | 'degraded' | 'unhealthy';
    if (healthyCount === totalCount) {
      status = 'healthy';
    } else if (healthyCount > 0) {
      status = 'degraded';
    } else {
      status = 'unhealthy';
    }

    const response: HealthResponse = {
      status,
      services,
      summary: {
        total: totalCount,
        healthy: healthyCount,
        unhealthy: unhealthyCount
      },
      timestamp
    };

    // Set appropriate status code
    const httpStatus = status === 'healthy' ? 200 : status === 'degraded' ? 207 : 503;
    
    return res.status(httpStatus).json(response);

  } catch (error: any) {
    console.error('Health check error:', error);
    
    const errorResponse: HealthResponse = {
      status: 'unhealthy',
      services: {},
      summary: {
        total: AGENT_ENDPOINTS.length,
        healthy: 0,
        unhealthy: AGENT_ENDPOINTS.length
      },
      timestamp: new Date().toISOString()
    };

    return res.status(503).json(errorResponse);
  }
}
