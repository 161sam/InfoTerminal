import type { NextApiRequest, NextApiResponse } from 'next';

const OPS_CONTROLLER_URL = process.env.OPS_CONTROLLER_URL || 'http://localhost:8614';

// Utility function to safely convert header values to strings
function getHeaderValue(value: string | string[] | undefined, defaultValue: string): string {
  if (Array.isArray(value)) {
    return value[0] || defaultValue;
  }
  return value || defaultValue;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { name, service, tail } = req.query;
  
  if (typeof name !== 'string') {
    return res.status(400).json({ error: 'Invalid stack name' });
  }

  try {
    // Build query parameters for the ops-controller
    const params = new URLSearchParams();
    if (typeof service === 'string') {
      params.set('service', service);
    }
    if (typeof tail === 'string') {
      params.set('tail', tail);
    }
    
    const queryString = params.toString() ? `?${params.toString()}` : '';
    const response = await fetch(`${OPS_CONTROLLER_URL}/ops/stacks/${encodeURIComponent(name)}/logs${queryString}`, {
      method: 'GET',
      headers: {
        // Forward user context for RBAC
        'X-User-Id': getHeaderValue(req.headers['x-user-id'], 'system'),
        'X-Roles': getHeaderValue(req.headers['x-roles'], 'admin'),
        'X-Scope': getHeaderValue(req.headers['x-scope'], 'infra'),
        'X-Tenant-Id': getHeaderValue(req.headers['x-tenant-id'], 'default')
      }
    });

    if (!response.ok) {
      const error = await response.text();
      return res.status(response.status).json({ 
        error: `Ops controller error: ${error}` 
      });
    }

    // Set up streaming response headers
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    // Handle connection cleanup
    const cleanup = () => {
      if (response.body && 'cancel' in response.body && typeof response.body.cancel === 'function') {
        response.body.cancel();
      }
    };

    req.on('close', cleanup);
    req.on('error', cleanup);

    if (!response.body) {
      return res.status(500).json({ error: 'No response body received' });
    }

    // Stream the response body to the client
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    try {
      while (true) {
        const { done, value } = await reader.read();
        
        if (done) break;
        
        const chunk = decoder.decode(value, { stream: true });
        res.write(chunk);
      }
    } catch (error) {
      console.error('Error streaming logs:', error);
    } finally {
      reader.releaseLock();
      res.end();
    }
  } catch (error) {
    console.error('Error proxying to ops-controller:', error);
    if (!res.headersSent) {
      res.status(500).json({ 
        error: 'Failed to stream logs',
        details: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }
}
