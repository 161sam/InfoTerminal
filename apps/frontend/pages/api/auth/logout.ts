// pages/api/auth/logout.ts
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
    const authToken = req.cookies.auth_token;

    if (authToken) {
      // Notify auth service about logout
      try {
        await fetch(`${AUTH_SERVICE_URL}/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'application/json',
            'X-Request-ID': generateRequestId(),
          }
        });
      } catch (error) {
        // Continue with logout even if service call fails
        console.error('Auth service logout error:', error);
      }
    }

    // Clear cookies
    const isProduction = process.env.NODE_ENV === 'production';
    const domain = process.env.COOKIE_DOMAIN;
    
    res.setHeader('Set-Cookie', [
      `auth_token=; HttpOnly; Path=/; Max-Age=0; SameSite=Strict${isProduction ? '; Secure' : ''}${domain ? `; Domain=${domain}` : ''}`,
      `refresh_token=; HttpOnly; Path=/; Max-Age=0; SameSite=Strict${isProduction ? '; Secure' : ''}${domain ? `; Domain=${domain}` : ''}`
    ]);

    return res.status(200).json({ success: true, message: 'Logged out successfully' });

  } catch (error) {
    console.error('Logout error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

function generateRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
