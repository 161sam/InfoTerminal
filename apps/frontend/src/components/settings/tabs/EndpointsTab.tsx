import React, { useState } from 'react';
import { Save, RefreshCw } from 'lucide-react';
import Panel from '@/components/layout/Panel';
import Button from '@/components/ui/button';
import Field from '@/components/ui/Field';
import StatusPill, { Status } from '@/components/ui/StatusPill';
import { toast } from '@/components/ui/toast';
import {
  loadEndpoints,
  saveEndpoints,
  sanitizeUrl,
  validateUrl,
  EndpointSettings,
} from '@/lib/endpoints';

interface ServiceEndpoint {
  key: keyof EndpointSettings;
  label: string;
  description: string;
  icon: React.ComponentType<{ size?: number; className?: string }>;
  required: boolean;
  defaultPort?: string;
}

interface EndpointsTabProps {
  serviceEndpoints: ServiceEndpoint[];
}

async function testEndpoint(url: string): Promise<{ status: Status; latency?: number; info?: any }> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);
  const start = performance.now();
  
  try {
    const response = await fetch(url + "/healthz", { signal: controller.signal });
    const latency = Math.round(performance.now() - start);
    clearTimeout(timeout);
    
    if (!response.ok) {
      return { status: "fail", latency };
    }
    
    const info = await response.json().catch(() => ({}));
    let status: Status = "ok";
    
    if (info.status === 'degraded') status = 'degraded';
    else if (info.status === 'fail') status = 'fail';
    else if (info.status !== 'ok' && info.status) status = 'fail';
    
    return { status, latency, info };
  } catch (error) {
    clearTimeout(timeout);
    return { status: "fail" };
  }
}

export const EndpointsTab: React.FC<EndpointsTabProps> = ({ serviceEndpoints }) => {
  const [endpointValues, setEndpointValues] = useState<EndpointSettings>(loadEndpoints());
  const [endpointStatus, setEndpointStatus] = useState<Record<string, { status: Status; latency?: number; info?: any }>>({});
  const [isSaving, setIsSaving] = useState(false);
  const [testingEndpoint, setTestingEndpoint] = useState<string | null>(null);

  const handleEndpointTest = async (endpoint: ServiceEndpoint) => {
    const url = sanitizeUrl(endpointValues[endpoint.key] || '');
    if (!url) {
      toast(`No URL configured for ${endpoint.label}`, { variant: 'error' });
      return;
    }

    if (!validateUrl(url)) {
      toast(`Invalid URL for ${endpoint.label}`, { variant: 'error' });
      return;
    }

    setTestingEndpoint(String(endpoint.key));
    setEndpointStatus((prev) => ({
      ...prev,
      [String(endpoint.key)]: { status: "loading" as Status },
    }));

    try {
      const result = await testEndpoint(url);
      setEndpointStatus(prev => ({ ...prev, [endpoint.key]: result }));
      
      if (result.status === 'ok') {
        toast(`${endpoint.label} is healthy${result.latency ? ` (${result.latency}ms)` : ''}`, { variant: 'success' });
      } else {
        toast(`${endpoint.label} connection failed`, { variant: 'error' });
      }
    } catch (error) {
      setEndpointStatus((prev) => ({
        ...prev,
        [String(endpoint.key)]: { status: "fail" as Status },
      }));
      toast(`${endpoint.label} test failed`, { variant: 'error' });
    } finally {
      setTestingEndpoint(null);
    }
  };

  const handleTestAllEndpoints = async () => {
    const configuredEndpoints = serviceEndpoints.filter(ep => endpointValues[ep.key]);
    
    if (configuredEndpoints.length === 0) {
      toast('No endpoints configured to test', { variant: 'error' });
      return;
    }

    setTestingEndpoint('all');
    
    const results = await Promise.allSettled(
      configuredEndpoints.map(async (endpoint) => {
        const url = sanitizeUrl(endpointValues[endpoint.key] || '');
        const result = await testEndpoint(url);
        return { endpoint: endpoint.key, result };
      })
    );

    const newStatus: Record<string, any> = {};
    results.forEach((result, index) => {
      if (result.status === 'fulfilled') {
        newStatus[result.value.endpoint] = result.value.result;
      } else {
        newStatus[configuredEndpoints[index].key] = { status: 'fail' };
      }
    });

    setEndpointStatus(prev => ({ ...prev, ...newStatus }));
    setTestingEndpoint(null);

    const successCount = Object.values(newStatus).filter(r => r.status === 'ok').length;
    toast(`Tested ${configuredEndpoints.length} endpoints: ${successCount} healthy, ${configuredEndpoints.length - successCount} failed`, {
      variant: successCount === configuredEndpoints.length ? 'success' : 'error'
    });
  };

  const handleSaveEndpoints = async () => {
    setIsSaving(true);
    
    try {
      const sanitized: EndpointSettings = {} as any;
      
      for (const [key, value] of Object.entries(endpointValues)) {
        const sanitizedUrl = sanitizeUrl(value || '');
        if (sanitizedUrl && !validateUrl(sanitizedUrl)) {
          toast(`Invalid URL for ${key}`, { variant: 'error' });
          setIsSaving(false);
          return;
        }
        sanitized[key as keyof EndpointSettings] = sanitizedUrl;
      }
      
      saveEndpoints(sanitized);
      toast("Settings saved successfully", { variant: 'success' });
    } catch (error) {
      toast("Failed to save settings", { variant: 'error' });
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <>
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100">Service Endpoints</h3>
          <p className="text-sm text-gray-600 dark:text-slate-400">Configure connections to your backend services</p>
        </div>
        
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            onClick={handleTestAllEndpoints}
            disabled={testingEndpoint !== null}
          >
            {testingEndpoint === 'all' ? (
              <RefreshCw size={16} className="animate-spin mr-2" />
            ) : (
              <RefreshCw size={16} className="mr-2" />
            )}
            Test All
          </Button>
          
          <Button
            onClick={handleSaveEndpoints}
            disabled={isSaving}
          >
            {isSaving ? (
              <RefreshCw size={16} className="animate-spin mr-2" />
            ) : (
              <Save size={16} className="mr-2" />
            )}
            Save
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {serviceEndpoints.map((endpoint) => (
          <Panel key={endpoint.key} className={endpoint.required ? 'border-l-4 border-l-blue-500' : ''}>
            <div className="flex items-start gap-4">
              <div className="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <endpoint.icon size={24} className="text-gray-600 dark:text-slate-400" />
              </div>
              
              <div className="flex-1 space-y-4">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="font-semibold text-gray-900 dark:text-slate-100">{endpoint.label}</h4>
                    {endpoint.required && (
                      <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">Required</span>
                    )}
                  </div>
                  <p className="text-sm text-gray-600 dark:text-slate-400">{endpoint.description}</p>
                  {endpoint.defaultPort && (
                    <p className="text-xs text-gray-500 dark:text-slate-500 mt-1">
                      Default port: {endpoint.defaultPort}
                    </p>
                  )}
                </div>
                
                <div className="flex items-center gap-2">
                  <Field
                    label=""
                    name={`endpoint-${String(endpoint.key).toLowerCase()}`}
                    id={`endpoint-${String(endpoint.key).toLowerCase()}`}
                    value={endpointValues[endpoint.key] || ''}
                    onChange={(e) => setEndpointValues(prev => ({ 
                      ...prev, 
                      [endpoint.key]: e.target.value 
                    }))}
                    placeholder={`http://localhost:${endpoint.defaultPort || '8000'}`}
                    className="flex-1"
                  />
                  
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleEndpointTest(endpoint)}
                    disabled={testingEndpoint !== null || !endpointValues[endpoint.key]}
                  >
                    {testingEndpoint === String(endpoint.key) ? (
                      <RefreshCw size={14} className="animate-spin" />
                    ) : (
                      'Test'
                    )}
                  </Button>
                  
                  {endpointStatus[endpoint.key] && (
                    <div className="flex items-center gap-2">
                      <StatusPill status={endpointStatus[endpoint.key].status} />
                      {endpointStatus[endpoint.key].latency && (
                        <span className="text-xs text-gray-500">
                          {endpointStatus[endpoint.key].latency}ms
                        </span>
                      )}
                    </div>
                  )}
                </div>
                
                {endpointStatus[endpoint.key]?.info && Object.keys(endpointStatus[endpoint.key].info).length > 0 && (
                  <details className="text-xs">
                    <summary className="cursor-pointer text-gray-600 dark:text-slate-400">Service Info</summary>
                    <pre className="mt-1 p-2 bg-gray-50 dark:bg-gray-900 rounded overflow-auto">
                      {JSON.stringify(endpointStatus[endpoint.key].info, null, 2)}
                    </pre>
                  </details>
                )}
              </div>
            </div>
          </Panel>
        ))}
      </div>
    </>
  );
};

export default EndpointsTab;
