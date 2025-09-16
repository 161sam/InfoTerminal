"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Container, 
  HardDrive, 
  Clock, 
  Activity,
  RefreshCw,
  Trash2
} from 'lucide-react';

interface EphemeralContainer {
  id: string;
  name: string;
  image: string;
  status: 'running' | 'stopped' | 'created';
  created: number;
  memoryUsage: number;
  memoryLimit: number;
  ephemeral: boolean;
}

interface EphemeralSessionProps {
  sessionId?: string;
  className?: string;
}

export function EphemeralSession({ sessionId, className }: EphemeralSessionProps) {
  const [containers, setContainers] = useState<EphemeralContainer[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [lastRefresh, setLastRefresh] = useState<number>(Date.now());

  useEffect(() => {
    if (sessionId) {
      loadContainers();
      // Auto-refresh every 10 seconds
      const interval = setInterval(loadContainers, 10000);
      return () => clearInterval(interval);
    }
  }, [sessionId]);

  const loadContainers = async () => {
    if (!sessionId) return;
    
    try {
      const response = await fetch(`/api/security/incognito/${sessionId}/containers`);
      if (response.ok) {
        const data = await response.json();
        setContainers(data.containers || []);
        setLastRefresh(Date.now());
      }
    } catch (error) {
      console.error('Failed to load containers:', error);
    }
  };

  const handleRefresh = async () => {
    setIsLoading(true);
    await loadContainers();
    setIsLoading(false);
  };

  const handleRestartContainer = async (containerId: string) => {
    try {
      const response = await fetch(`/api/security/containers/${containerId}/restart`, {
        method: 'POST'
      });
      
      if (response.ok) {
        await loadContainers();
      }
    } catch (error) {
      console.error('Failed to restart container:', error);
    }
  };

  const handleStopContainer = async (containerId: string) => {
    try {
      const response = await fetch(`/api/security/containers/${containerId}/stop`, {
        method: 'POST'
      });
      
      if (response.ok) {
        await loadContainers();
      }
    } catch (error) {
      console.error('Failed to stop container:', error);
    }
  };

  const formatMemoryUsage = (bytes: number): string => {
    const mb = bytes / (1024 * 1024);
    return `${mb.toFixed(1)} MB`;
  };

  const formatUptime = (created: number): string => {
    const uptime = Date.now() - created;
    const minutes = Math.floor(uptime / 60000);
    const hours = Math.floor(minutes / 60);
    
    if (hours > 0) {
      return `${hours}h ${minutes % 60}m`;
    }
    return `${minutes}m`;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-green-500';
      case 'stopped': return 'bg-red-500';
      case 'created': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusVariant = (status: string) => {
    switch (status) {
      case 'running': return 'default';
      case 'stopped': return 'destructive';
      case 'created': return 'secondary';
      default: return 'outline';
    }
  };

  if (!sessionId) {
    return (
      <Card className={className}>
        <CardContent className="p-6">
          <div className="text-center text-muted-foreground">
            No active incognito session
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Container className="h-5 w-5" />
            <CardTitle>Ephemeral Containers</CardTitle>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">
              Last updated: {new Date(lastRefresh).toLocaleTimeString()}
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={handleRefresh}
              disabled={isLoading}
            >
              <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {containers.length === 0 ? (
          <Alert>
            <Container className="h-4 w-4" />
            <AlertDescription>
              No ephemeral containers found for this session.
            </AlertDescription>
          </Alert>
        ) : (
          <div className="space-y-3">
            {containers.map((container) => (
              <div
                key={container.id}
                className="p-4 border rounded-lg space-y-3"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${getStatusColor(container.status)}`} />
                    <div>
                      <p className="font-medium">{container.name}</p>
                      <p className="text-sm text-muted-foreground">{container.image}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {container.ephemeral && (
                      <Badge variant="outline" className="text-xs">
                        Ephemeral
                      </Badge>
                    )}
                    <Badge variant={getStatusVariant(container.status)}>
                      {container.status}
                    </Badge>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4 text-muted-foreground" />
                    <span>Uptime: {formatUptime(container.created)}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <HardDrive className="h-4 w-4 text-muted-foreground" />
                    <span>
                      Memory: {formatMemoryUsage(container.memoryUsage)} / {formatMemoryUsage(container.memoryLimit)}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Activity className="h-4 w-4 text-muted-foreground" />
                    <span>ID: {container.id.slice(0, 12)}</span>
                  </div>
                </div>

                {container.status === 'running' && (
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleRestartContainer(container.id)}
                      className="flex items-center gap-2"
                    >
                      <RefreshCw className="h-4 w-4" />
                      Restart
                    </Button>
                    <Button
                      variant="destructive"
                      size="sm"
                      onClick={() => handleStopContainer(container.id)}
                      className="flex items-center gap-2"
                    >
                      <Trash2 className="h-4 w-4" />
                      Stop
                    </Button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Session Statistics */}
        <div className="pt-4 border-t">
          <h4 className="font-medium mb-3">Session Statistics</h4>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <p className="text-muted-foreground">Total Containers</p>
              <p className="text-lg font-medium">{containers.length}</p>
            </div>
            <div>
              <p className="text-muted-foreground">Running</p>
              <p className="text-lg font-medium text-green-600">
                {containers.filter(c => c.status === 'running').length}
              </p>
            </div>
            <div>
              <p className="text-muted-foreground">Memory Usage</p>
              <p className="text-lg font-medium">
                {formatMemoryUsage(
                  containers.reduce((sum, c) => sum + c.memoryUsage, 0)
                )}
              </p>
            </div>
          </div>
        </div>

        {/* Ephemeral Features Info */}
        <div className="pt-4 border-t">
          <h4 className="font-medium mb-2">Ephemeral Features</h4>
          <div className="grid grid-cols-1 gap-1 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full" />
              <span>No persistent volumes mounted</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full" />
              <span>Temporary filesystem only</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full" />
              <span>Isolated network namespace</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full" />
              <span>Auto-cleanup on session end</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
