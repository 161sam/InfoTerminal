"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  EyeOff, 
  Shield, 
  Timer, 
  Trash2, 
  AlertTriangle,
  Lock,
  Unlock
} from 'lucide-react';

interface IncognitoSession {
  id: string;
  started: number;
  autoWipeAt: number;
  dataSize: number;
  containerCount: number;
  status: 'active' | 'expired' | 'wiped';
}

interface IncognitoModeProps {
  className?: string;
}

export function IncognitoMode({ className }: IncognitoModeProps) {
  const [isIncognitoActive, setIsIncognitoActive] = useState(false);
  const [currentSession, setCurrentSession] = useState<IncognitoSession | null>(null);
  const [autoWipeEnabled, setAutoWipeEnabled] = useState(true);
  const [wipeTimerMinutes, setWipeTimerMinutes] = useState(60);
  const [isLoading, setIsLoading] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState<number | null>(null);

  // Timer for countdown
  useEffect(() => {
    if (!currentSession || currentSession.status !== 'active') return;

    const interval = setInterval(() => {
      const now = Date.now();
      const remaining = Math.max(0, currentSession.autoWipeAt - now);
      
      if (remaining <= 0) {
        handleAutoWipe();
      } else {
        setTimeRemaining(remaining);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [currentSession]);

  const handleToggleIncognito = async () => {
    setIsLoading(true);
    
    try {
      if (isIncognitoActive) {
        // Stop incognito mode
        await stopIncognitoMode();
      } else {
        // Start incognito mode
        await startIncognitoMode();
      }
    } catch (error) {
      console.error('Failed to toggle incognito mode:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const startIncognitoMode = async () => {
    const response = await fetch('/api/security/incognito/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        autoWipeMinutes: autoWipeEnabled ? wipeTimerMinutes : null,
        memoryOnlyMode: true,
        isolatedContainers: true
      })
    });

    if (!response.ok) {
      throw new Error('Failed to start incognito mode');
    }

    const session = await response.json();
    setCurrentSession(session);
    setIsIncognitoActive(true);
  };

  const stopIncognitoMode = async () => {
    if (!currentSession) return;

    const response = await fetch(`/api/security/incognito/${currentSession.id}/stop`, {
      method: 'POST'
    });

    if (!response.ok) {
      throw new Error('Failed to stop incognito mode');
    }

    setCurrentSession(null);
    setIsIncognitoActive(false);
    setTimeRemaining(null);
  };

  const handleManualWipe = async () => {
    if (!currentSession) return;

    setIsLoading(true);
    
    try {
      const response = await fetch(`/api/security/incognito/${currentSession.id}/wipe`, {
        method: 'POST'
      });

      if (!response.ok) {
        throw new Error('Failed to wipe session data');
      }

      setCurrentSession(prev => prev ? { ...prev, status: 'wiped' } : null);
      setIsIncognitoActive(false);
    } catch (error) {
      console.error('Failed to wipe session:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAutoWipe = async () => {
    await handleManualWipe();
  };

  const formatTime = (ms: number): string => {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const formatDataSize = (bytes: number): string => {
    const mb = bytes / (1024 * 1024);
    return `${mb.toFixed(1)} MB`;
  };

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <EyeOff className="h-5 w-5" />
            <CardTitle>Incognito Mode</CardTitle>
          </div>
          <div className="flex items-center gap-2">
            {isIncognitoActive ? (
              <Badge variant="destructive" className="flex items-center gap-1">
                <Lock className="h-3 w-3" />
                Active
              </Badge>
            ) : (
              <Badge variant="secondary" className="flex items-center gap-1">
                <Unlock className="h-3 w-3" />
                Inactive
              </Badge>
            )}
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Warning Alert */}
        <Alert>
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            Incognito mode creates ephemeral containers and memory-only storage. 
            All investigation data will be automatically wiped when the session ends.
          </AlertDescription>
        </Alert>

        {/* Main Toggle */}
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <p className="font-medium">Enable Incognito Mode</p>
            <p className="text-sm text-muted-foreground">
              Ephemeral session with automatic data wiping
            </p>
          </div>
          <Switch
            checked={isIncognitoActive}
            onCheckedChange={handleToggleIncognito}
            disabled={isLoading}
          />
        </div>

        {/* Session Configuration */}
        {!isIncognitoActive && (
          <div className="space-y-4 p-4 border rounded-lg">
            <h4 className="font-medium">Session Configuration</h4>
            
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <p className="text-sm font-medium">Auto-wipe Timer</p>
                <p className="text-xs text-muted-foreground">
                  Automatically wipe data after timeout
                </p>
              </div>
              <Switch
                checked={autoWipeEnabled}
                onCheckedChange={setAutoWipeEnabled}
              />
            </div>

            {autoWipeEnabled && (
              <div className="space-y-2">
                <label className="text-sm font-medium">Wipe Timer (minutes)</label>
                <select
                  value={wipeTimerMinutes}
                  onChange={(e) => setWipeTimerMinutes(Number(e.target.value))}
                  className="w-full p-2 border rounded"
                >
                  <option value={15}>15 minutes</option>
                  <option value={30}>30 minutes</option>
                  <option value={60}>1 hour</option>
                  <option value={120}>2 hours</option>
                  <option value={240}>4 hours</option>
                </select>
              </div>
            )}
          </div>
        )}

        {/* Active Session Status */}
        {isIncognitoActive && currentSession && (
          <div className="space-y-4 p-4 border rounded-lg bg-red-50 dark:bg-red-950/20">
            <div className="flex items-center gap-2">
              <Shield className="h-4 w-4 text-red-600" />
              <h4 className="font-medium text-red-600">Active Incognito Session</h4>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-muted-foreground">Session ID</p>
                <p className="text-sm font-mono">{currentSession.id.slice(0, 8)}...</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground">Data Size</p>
                <p className="text-sm">{formatDataSize(currentSession.dataSize)}</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground">Containers</p>
                <p className="text-sm">{currentSession.containerCount}</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground">Status</p>
                <p className="text-sm capitalize">{currentSession.status}</p>
              </div>
            </div>

            {timeRemaining !== null && autoWipeEnabled && (
              <div className="flex items-center gap-2 p-2 bg-yellow-100 dark:bg-yellow-900/20 rounded">
                <Timer className="h-4 w-4 text-yellow-600" />
                <span className="text-sm">
                  Auto-wipe in: <span className="font-mono">{formatTime(timeRemaining)}</span>
                </span>
              </div>
            )}

            <div className="flex gap-2">
              <Button
                variant="destructive"
                size="sm"
                onClick={handleManualWipe}
                disabled={isLoading}
                className="flex items-center gap-2"
              >
                <Trash2 className="h-4 w-4" />
                Wipe Now
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsIncognitoActive(false)}
                disabled={isLoading}
              >
                Stop Session
              </Button>
            </div>
          </div>
        )}

        {/* Security Features */}
        <div className="space-y-3">
          <h4 className="font-medium">Security Features</h4>
          <div className="grid grid-cols-1 gap-2 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full" />
              <span>Ephemeral filesystem containers</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full" />
              <span>Memory-only data storage</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full" />
              <span>Isolated network containers</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full" />
              <span>Automatic data wiping</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full" />
              <span>Minimal audit logging</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
