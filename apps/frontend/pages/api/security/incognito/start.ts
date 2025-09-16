// pages/api/security/incognito/start.ts
import type { NextApiRequest, NextApiResponse } from 'next';

interface StartIncognitoRequest {
  autoWipeMinutes?: number;
  memoryOnlyMode?: boolean;
  isolatedContainers?: boolean;
}

interface IncognitoSession {
  id: string;
  started: number;
  autoWipeAt: number;
  dataSize: number;
  containerCount: number;
  status: 'active' | 'expired' | 'wiped';
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<IncognitoSession | { error: string }>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const {
      autoWipeMinutes = 60,
      memoryOnlyMode = true,
      isolatedContainers = true
    }: StartIncognitoRequest = req.body;

    // Generate unique session ID
    const sessionId = `incognito_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const started = Date.now();
    const autoWipeAt = autoWipeMinutes ? started + (autoWipeMinutes * 60 * 1000) : 0;

    // Call ops controller to start incognito session
    const opsControllerUrl = process.env.OPS_CONTROLLER_URL || 'http://localhost:8614';
    const response = await fetch(`${opsControllerUrl}/security/incognito/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        sessionId,
        autoWipeMinutes,
        memoryOnlyMode,
        isolatedContainers
      })
    });

    if (!response.ok) {
      throw new Error('Failed to start incognito session');
    }

    const sessionData = await response.json();

    const session: IncognitoSession = {
      id: sessionId,
      started,
      autoWipeAt,
      dataSize: 0,
      containerCount: sessionData.containerCount || 0,
      status: 'active'
    };

    res.status(200).json(session);
  } catch (error) {
    console.error('Failed to start incognito session:', error);
    res.status(500).json({ error: 'Failed to start incognito session' });
  }
}
