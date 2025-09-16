import { useState, useEffect } from 'react';
import { 
  Shield, 
  Globe, 
  EyeOff, 
  Container,
  AlertTriangle,
  CheckCircle,
  Activity,
  RefreshCw
} from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Panel from '@/components/layout/Panel';
import { IncognitoMode } from '@/components/security/IncognitoMode';
import { EphemeralSession } from '@/components/security/EphemeralSession';
import { DataWipeControls } from '@/components/security/DataWipeControls';

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

export default function SecurityPage() {
  const [activeTab, setActiveTab] = useState<'overview' | 'incognito' | 'containers' | 'wipe'>('overview');
  const [securityStatus, setSecurityStatus] = useState<SecurityStatus | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [lastRefresh, setLastRefresh] = useState<number>(Date.now());

  useEffect(() => {
    loadSecurityStatus();
    // Auto-refresh every 30 seconds
    const interval = setInterval(loadSecurityStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadSecurityStatus = async () => {
    try {
      const response = await fetch('/api/security/status');
      if (response.ok) {
        const status = await response.json();
        setSecurityStatus(status);
      } else {
        // Fallback mock data for development
        setSecurityStatus({
          egressGateway: {
            status: 'healthy',
            torAvailable: true,
            vpnCount: 3,
            proxyCount: 5,
            anonymityLevel: 'high'
          },
          incognitoMode: {
            active: false
          },
          dataProtection: {
            ephemeralContainers: 0,
            memoryOnlyMode: false,
            autoWipeEnabled: true
          }
        });
      }
      setLastRefresh(Date.now());
    } catch (error) {
      console.error('Failed to load security status:', error);
      // Fallback mock data
      setSecurityStatus({
        egressGateway: {
          status: 'offline',
          torAvailable: false,
          vpnCount: 0,
          proxyCount: 0,
          anonymityLevel: 'none'
        },
        incognitoMode: {
          active: false
        },
        dataProtection: {
          ephemeralContainers: 0,
          memoryOnlyMode: false,
          autoWipeEnabled: false
        }
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleRefresh = async () => {
    setIsLoading(true);
    await loadSecurityStatus();
    setIsLoading(false);
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy': return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'degraded': return <AlertTriangle className="h-4 w-4 text-yellow-500" />;
      case 'offline': return <AlertTriangle className="h-4 w-4 text-red-500" />;
      default: return <Activity className="h-4 w-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-900/30 text-green-800 dark:text-green-300';
      case 'degraded': return 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-900/30 text-yellow-800 dark:text-yellow-300';
      case 'offline': return 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-900/30 text-red-800 dark:text-red-300';
      default: return 'bg-gray-50 dark:bg-gray-900/20 border-gray-200 dark:border-gray-900/30 text-gray-800 dark:text-gray-300';
    }
  };

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Shield },
    { id: 'incognito', label: 'Incognito Mode', icon: EyeOff },
    { id: 'containers', label: 'Ephemeral Sessions', icon: Container },
    { id: 'wipe', label: 'Data Wipe', icon: Shield }
  ];

  if (isLoading && !securityStatus) {
    return (
      <DashboardLayout title="Security Dashboard" subtitle="Anonymous research and data protection controls">
        <div className="p-6">
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full" />
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="Security Dashboard" subtitle="Anonymous research and data protection controls">
      <div className="p-6">
        <div className="max-w-7xl space-y-6">
          
          {/* Tab Navigation */}
          <div className="flex flex-wrap gap-2 border-b border-gray-200 dark:border-gray-800">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-t-lg border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? 'text-blue-600 border-blue-600 bg-blue-50 dark:bg-blue-900/20'
                      : 'text-gray-500 border-transparent hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  {tab.label}
                </button>
              );
            })}
            
            <div className="ml-auto flex items-center gap-2">
              <span className="text-sm text-gray-500">
                Last updated: {new Date(lastRefresh).toLocaleTimeString()}
              </span>
              <button
                onClick={handleRefresh}
                disabled={isLoading}
                className="p-2 text-gray-500 hover:text-gray-700 transition-colors"
              >
                <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
              </button>
            </div>
          </div>

          {/* Overview Tab */}
          {activeTab === 'overview' && securityStatus && (
            <div className="space-y-6">
              {/* Security Status Overview */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Egress Gateway Status */}
                <Panel>
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <Globe className="h-5 w-5 text-blue-500" />
                      <h3 className="text-lg font-semibold">Egress Gateway</h3>
                    </div>
                    <div className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(securityStatus.egressGateway.status)}`}>
                      {getStatusIcon(securityStatus.egressGateway.status)}
                      {securityStatus.egressGateway.status}
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Tor Available</span>
                      <span>{securityStatus.egressGateway.torAvailable ? 'Yes' : 'No'}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">VPN Pools</span>
                      <span>{securityStatus.egressGateway.vpnCount}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Proxy Pools</span>
                      <span>{securityStatus.egressGateway.proxyCount}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Anonymity Level</span>
                      <span className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded text-xs">
                        {securityStatus.egressGateway.anonymityLevel}
                      </span>
                    </div>
                  </div>
                </Panel>

                {/* Incognito Mode Status */}
                <Panel>
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <EyeOff className="h-5 w-5 text-purple-500" />
                      <h3 className="text-lg font-semibold">Incognito Mode</h3>
                    </div>
                    <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                      securityStatus.incognitoMode.active 
                        ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300' 
                        : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
                    }`}>
                      {securityStatus.incognitoMode.active ? 'Active' : 'Inactive'}
                    </div>
                  </div>
                  <div className="space-y-2">
                    {securityStatus.incognitoMode.active ? (
                      <>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-500">Session ID</span>
                          <span className="font-mono text-xs">
                            {securityStatus.incognitoMode.sessionId?.slice(0, 8)}...
                          </span>
                        </div>
                        {securityStatus.incognitoMode.timeRemaining && (
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-500">Time Remaining</span>
                            <span>
                              {Math.floor(securityStatus.incognitoMode.timeRemaining / 60000)}m
                            </span>
                          </div>
                        )}
                      </>
                    ) : (
                      <p className="text-sm text-gray-500">
                        No active incognito session
                      </p>
                    )}
                  </div>
                </Panel>

                {/* Data Protection Status */}
                <Panel>
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <Container className="h-5 w-5 text-green-500" />
                      <h3 className="text-lg font-semibold">Data Protection</h3>
                    </div>
                    <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                      securityStatus.dataProtection.memoryOnlyMode 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300' 
                        : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
                    }`}>
                      {securityStatus.dataProtection.memoryOnlyMode ? 'Secured' : 'Standard'}
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Ephemeral Containers</span>
                      <span>{securityStatus.dataProtection.ephemeralContainers}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Memory-Only Mode</span>
                      <span>{securityStatus.dataProtection.memoryOnlyMode ? 'Enabled' : 'Disabled'}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Auto-Wipe</span>
                      <span>{securityStatus.dataProtection.autoWipeEnabled ? 'Enabled' : 'Disabled'}</span>
                    </div>
                  </div>
                </Panel>
              </div>

              {/* Security Features Overview */}
              <Panel>
                <div className="flex items-center gap-3 mb-6">
                  <Shield className="h-6 w-6 text-blue-500" />
                  <h3 className="text-xl font-semibold">InfoTerminal v0.2.0 Security Features</h3>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div className="p-4 border rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Globe className="h-5 w-5 text-blue-500" />
                      <h4 className="font-medium">Anonymous Egress</h4>
                    </div>
                    <p className="text-sm text-gray-600">Tor, VPN, and proxy routing for anonymous OSINT research</p>
                  </div>
                  
                  <div className="p-4 border rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <EyeOff className="h-5 w-5 text-purple-500" />
                      <h4 className="font-medium">Incognito Mode</h4>
                    </div>
                    <p className="text-sm text-gray-600">Ephemeral sessions with automatic data wiping</p>
                  </div>
                  
                  <div className="p-4 border rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Container className="h-5 w-5 text-green-500" />
                      <h4 className="font-medium">Isolated Containers</h4>
                    </div>
                    <p className="text-sm text-gray-600">Secure, ephemeral containers for sensitive operations</p>
                  </div>
                </div>
              </Panel>
            </div>
          )}

          {/* Incognito Mode Tab */}
          {activeTab === 'incognito' && (
            <IncognitoMode />
          )}

          {/* Containers Tab */}
          {activeTab === 'containers' && (
            <EphemeralSession 
              sessionId={securityStatus?.incognitoMode.sessionId} 
            />
          )}

          {/* Data Wipe Tab */}
          {activeTab === 'wipe' && (
            <DataWipeControls 
              sessionId={securityStatus?.incognitoMode.sessionId} 
            />
          )}

        </div>
      </div>
    </DashboardLayout>
  );
}
