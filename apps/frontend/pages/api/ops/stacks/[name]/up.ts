import type { NextApiRequest, NextApiResponse } from 'next';

const OPS_CONTROLLER_URL = process.env.OPS_CONTROLLER_URL || 'http://localhost:8614';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { name } = req.query;
  
  if (typeof name !== 'string') {
    return res.status(400).json({ error: 'Invalid stack name' });
  }

  try {
    const response = await fetch(`${OPS_CONTROLLER_URL}/ops/stacks/${encodeURIComponent(name)}/up`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Forward user context for RBAC
        'X-User-Id': req.headers['x-user-id'] || 'system',
        'X-Roles': req.headers['x-roles'] || 'admin',
        'X-Scope': req.headers['x-scope'] || 'infra',
        'X-Tenant-Id': req.headers['x-tenant-id'] || 'default'
      }
    });

    if (!response.ok) {
      const error = await response.text();
      return res.status(response.status).json({ 
        error: `Ops controller error: ${error}` 
      });
    }

    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    console.error('Error proxying to ops-controller:', error);
    res.status(500).json({ 
      error: 'Failed to start stack',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
