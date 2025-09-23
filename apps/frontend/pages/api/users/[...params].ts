// pages/api/users/[...params].ts
import type { NextApiRequest, NextApiResponse } from 'next';

const AUTH_SERVICE_URL = process.env.AUTH_SERVICE_URL || 'http://localhost:8080';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const authToken = req.cookies.auth_token;

    if (!authToken) {
      return res.status(401).json({ error: 'Not authenticated' });
    }

    // Extract dynamic path parameters
    const { params } = req.query;
    const pathSegments = Array.isArray(params) ? params : [params];
    const path = pathSegments.filter(Boolean).join('/');

    // Build query string for GET requests
    const queryParams = { ...req.query };
    delete queryParams.params; // Remove the dynamic route parameter
    
    const queryString = req.method === 'GET' && Object.keys(queryParams).length > 0
      ? '?' + new URLSearchParams(queryParams as Record<string, string>).toString()
      : '';

    // Forward request to auth service
    const response = await fetch(`${AUTH_SERVICE_URL}/users/${path}${queryString}`, {
      method: req.method,
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json',
        'X-Request-ID': generateRequestId(),
        'X-Forwarded-For': getClientIP(req),
        'User-Agent': req.headers['user-agent'] || 'InfoTerminal-Frontend',
      },
      ...(req.method !== 'GET' && req.body ? { body: JSON.stringify(req.body) } : {})
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json(data);
    }

    return res.status(200).json(data);

  } catch (error) {
    console.error('User API error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

function generateRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

function getClientIP(req: NextApiRequest): string {
  const forwarded = req.headers['x-forwarded-for'];
  const ip = forwarded 
    ? (Array.isArray(forwarded) ? forwarded[0] : forwarded.split(',')[0])
    : req.connection?.remoteAddress || req.socket?.remoteAddress || 'unknown';
  return ip;
}
