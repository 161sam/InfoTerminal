// pages/api/security/status.ts
import type { NextApiRequest, NextApiResponse } from 'next';

interface SecurityStatus {
  egressGateway: {
    status: 'healthy' | 'degraded' | 'offline';
    torAvailable: boolean;
    vpnCount: number;
    proxyCount: number;
    anonymityLevel: string;
  };
  incognitoMode: {
    active: boolean;
    sessionId?: string;
    timeRemaining?: number;
  };
  dataProtection: {
    ephemeralContainers: number;
    memoryOnlyMode: boolean;
    autoWipeEnabled: boolean;
  };
}

// Helper function to create fetch with timeout using AbortController
async function fetchWithTimeout(url: string, timeoutMs: number = 5000): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  
  try {
    const response = await fetch(url, {
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json'
      }
    });
    return response;
  } finally {
    clearTimeout(timeoutId);
  }
}

async function checkEgressGateway() {
  try {
    const egressGatewayUrl = process.env.EGRESS_GATEWAY_URL || 'http://localhost:8615';
    // Use fetchWithTimeout instead of direct fetch with timeout property
    const response = await fetchWithTimeout(`${egressGatewayUrl}/proxy/status`, 5000);

    if (response.ok) {
      const data = await response.json();
      return {
        status: 'healthy' as const,
        torAvailable: data.tor_available || false,
        vpnCount: data.vpn_pools?.length || 0,
        proxyCount: data.proxy_pools?.length || 0,
        anonymityLevel: data.anonymity_level || 'none'
      };
    } else {
      throw new Error('Egress gateway not responding');
    }
  } catch (error) {
    console.warn('Egress gateway unavailable:', error);
    return {
      status: 'offline' as const,
      torAvailable: false,
      vpnCount: 0,
      proxyCount: 0,
      anonymityLevel: 'none'
    };
  }
}

async function checkIncognitoMode() {
  try {
    // Check if there's an active incognito session
    const opsControllerUrl = process.env.OPS_CONTROLLER_URL || 'http://localhost:8618';
    const response = await fetchWithTimeout(`${opsControllerUrl}/api/security/incognito/status`, 5000);

    if (response.ok) {
      const data = await response.json();
      return {
        active: data.active || false,
        sessionId: data.sessionId,
        timeRemaining: data.timeRemaining
      };
    } else {
      throw new Error('Ops controller not responding');
    }
  } catch (error) {
    console.warn('Ops controller unavailable, using fallback state:', error);
    return {
      active: false
    };
  }
}

async function checkDataProtection() {
  try {
    const opsControllerUrl = process.env.OPS_CONTROLLER_URL || 'http://localhost:8618';
    const response = await fetchWithTimeout(`${opsControllerUrl}/api/security/containers/status`, 5000);

    if (response.ok) {
      const data = await response.json();
      return {
        ephemeralContainers: data.ephemeralContainers || 0,
        memoryOnlyMode: data.memoryOnlyMode || false,
        autoWipeEnabled: data.autoWipeEnabled || false
      };
    } else {
      throw new Error('Ops controller not responding');
    }
  } catch (error) {
    console.warn('Ops controller unavailable for data protection status:', error);
    return {
      ephemeralContainers: 0,
      memoryOnlyMode: false,
      autoWipeEnabled: false
    };
  }
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<SecurityStatus | { error: string }>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Check all security components in parallel with proper error handling
    const [egressStatus, incognitoStatus, dataProtectionStatus] = await Promise.allSettled([
      checkEgressGateway(),
      checkIncognitoMode(),
      checkDataProtection()
    ]);

    const status: SecurityStatus = {
      egressGateway: egressStatus.status === 'fulfilled' ? egressStatus.value : {
        status: 'offline' as const,
        torAvailable: false,
        vpnCount: 0,
        proxyCount: 0,
        anonymityLevel: 'none'
      },
      incognitoMode: incognitoStatus.status === 'fulfilled' ? incognitoStatus.value : {
        active: false
      },
      dataProtection: dataProtectionStatus.status === 'fulfilled' ? dataProtectionStatus.value : {
        ephemeralContainers: 0,
        memoryOnlyMode: false,
        autoWipeEnabled: false
      }
    };

    res.status(200).json(status);
  } catch (error) {
    console.error('Failed to get security status:', error);
    res.status(500).json({ error: 'Failed to get security status' });
  }
}
