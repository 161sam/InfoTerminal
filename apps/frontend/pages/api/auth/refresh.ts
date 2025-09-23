// pages/api/auth/refresh.ts
import type { NextApiRequest, NextApiResponse } from 'next';

const AUTH_SERVICE_URL = process.env.AUTH_SERVICE_URL || 'http://localhost:8080';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const refreshToken = req.cookies.refresh_token;

    if (!refreshToken) {
      return res.status(401).json({ error: 'No refresh token' });
    }

    // Forward request to auth service
    const response = await fetch(`${AUTH_SERVICE_URL}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Request-ID': generateRequestId(),
      },
      body: JSON.stringify({
        refresh_token: refreshToken
      })
    });

    const data = await response.json();

    if (!response.ok) {
      // If refresh token is invalid, clear cookies
      if (response.status === 401) {
        const isProduction = process.env.NODE_ENV === 'production';
        const domain = process.env.COOKIE_DOMAIN;
        
        res.setHeader('Set-Cookie', [
          `auth_token=; HttpOnly; Path=/; Max-Age=0; SameSite=Strict${isProduction ? '; Secure' : ''}${domain ? `; Domain=${domain}` : ''}`,
          `refresh_token=; HttpOnly; Path=/; Max-Age=0; SameSite=Strict${isProduction ? '; Secure' : ''}${domain ? `; Domain=${domain}` : ''}`
        ]);
      }
      return res.status(response.status).json(data);
    }

    // Update cookies with new tokens
    const isProduction = process.env.NODE_ENV === 'production';
    const domain = process.env.COOKIE_DOMAIN;
    
    res.setHeader('Set-Cookie', [
      `auth_token=${data.access_token}; HttpOnly; Path=/; Max-Age=1800; SameSite=Strict${isProduction ? '; Secure' : ''}${domain ? `; Domain=${domain}` : ''}`,
      `refresh_token=${data.refresh_token}; HttpOnly; Path=/; Max-Age=604800; SameSite=Strict${isProduction ? '; Secure' : ''}${domain ? `; Domain=${domain}` : ''}`
    ]);

    return res.status(200).json({
      access_token: data.access_token,
      token_type: data.token_type,
      expires_in: data.expires_in
    });

  } catch (error) {
    console.error('Token refresh error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

function generateRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
