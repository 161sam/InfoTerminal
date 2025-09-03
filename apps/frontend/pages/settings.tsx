// apps/frontend/pages/settings.tsx - Application Settings Page
import { useState } from 'react';
import { 
  Settings as SettingsIcon, 
  Sun, 
  Moon, 
  Monitor,
  Bell, 
  Globe, 
  Database,
  Key,
  Palette,
  Save,
  RefreshCw
} from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { ThemeToggle, useTheme } from '@/lib/theme-provider';
import config from '@/lib/config';

export default function SettingsPage() {
  const { theme, setTheme } = useTheme();
  const [settings, setSettings] = useState({
    notifications: {
      email: true,
      push: true,
      updates: true,
      security: true
    },
    appearance: {
      theme: theme,
      compact: false,
      animations: true
    },
    api: {
      searchUrl: config.SEARCH_API,
      graphUrl: config.GRAPH_API,
      docsUrl: config.DOCENTITIES_API,
      nlpUrl: config.NLP_API
    },
    language: 'en',
    timezone: 'UTC',
    autoRefresh: true,
    refreshInterval: 30
  });

  const [saved, setSaved] = useState(false);

  const updateSetting = (section: string, key: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section as keyof typeof prev],
        [key]: value
      }
    }));
  };

  const handleSave = async () => {
    // In a real app, this would save to backend
    localStorage.setItem('user-settings', JSON.stringify(settings));
    
    // Update theme if changed
    if (settings.appearance.theme !== theme) {
      setTheme(settings.appearance.theme);
    }
    
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const resetToDefaults = () => {
    if (confirm('Are you sure you want to reset all settings to defaults?')) {
      setSettings({
        notifications: { email: true, push: true, updates: true, security: true },
        appearance: { theme: 'system', compact: false, animations: true },
        api: {
          searchUrl: 'http://localhost:8001',
          graphUrl: 'http://localhost:8002',
          docsUrl: 'http://localhost:8006',
          nlpUrl: 'http://localhost:8003'
        },
        language: 'en',
        timezone: 'UTC',
        autoRefresh: true,
        refreshInterval: 30
      });
    }
  };

  return (
    <DashboardLayout title="Settings" subtitle="Configure your application preferences">
      <div className="p-6">
        <div className="max-w-4xl space-y-8">
          
          {/* General Settings */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-6">
              <SettingsIcon size={20} className="text-gray-500" />
              <h3 className="text-lg font-semibold">General</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Language
                </label>
                <select 
                  value={settings.language}
                  onChange={(e) => updateSetting('', 'language', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                >
                  <option value="en">English</option>
                  <option value="de">Deutsch</option>
                  <option value="fr">Français</option>
                  <option value="es">Español</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Timezone
                </label>
                <select 
                  value={settings.timezone}
                  onChange={(e) => updateSetting('', 'timezone', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                >
                  <option value="UTC">UTC</option>
                  <option value="America/New_York">Eastern Time</option>
                  <option value="America/Los_Angeles">Pacific Time</option>
                  <option value="Europe/London">London</option>
                  <option value="Europe/Berlin">Berlin</option>
                  <option value="Asia/Tokyo">Tokyo</option>
                </select>
              </div>
            </div>
          </div>

          {/* Appearance Settings */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-6">
              <Palette size={20} className="text-purple-500" />
              <h3 className="text-lg font-semibold">Appearance</h3>
            </div>
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">Theme</label>
                <div className="flex items-center gap-4">
                  <button
                    onClick={() => updateSetting('appearance', 'theme', 'light')}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg border transition-colors ${
                      settings.appearance.theme === 'light'
                        ? 'border-primary-500 bg-primary-50 text-primary-700'
                        : 'border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    <Sun size={16} />
                    Light
                  </button>
                  <button
                    onClick={() => updateSetting('appearance', 'theme', 'dark')}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg border transition-colors ${
                      settings.appearance.theme === 'dark'
                        ? 'border-primary-500 bg-primary-50 text-primary-700'
                        : 'border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    <Moon size={16} />
                    Dark
                  </button>
                  <button
                    onClick={() => updateSetting('appearance', 'theme', 'system')}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg border transition-colors ${
                      settings.appearance.theme === 'system'
                        ? 'border-primary-500 bg-primary-50 text-primary-700'
                        : 'border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    <Monitor size={16} />
                    System
                  </button>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700">Compact Mode</label>
                  <p className="text-sm text-gray-500">Use smaller spacing and components</p>
                </div>
                <button
                  onClick={() => updateSetting('appearance', 'compact', !settings.appearance.compact)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.appearance.compact ? 'bg-primary-600' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                      settings.appearance.compact ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700">Animations</label>
                  <p className="text-sm text-gray-500">Enable smooth transitions and animations</p>
                </div>
                <button
                  onClick={() => updateSetting('appearance', 'animations', !settings.appearance.animations)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.appearance.animations ? 'bg-primary-600' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                      settings.appearance.animations ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
            </div>
          </div>

          {/* Notification Settings */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-6">
              <Bell size={20} className="text-blue-500" />
              <h3 className="text-lg font-semibold">Notifications</h3>
            </div>
            
            <div className="space-y-4">
              {Object.entries(settings.notifications).map(([key, value]) => (
                <div key={key} className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700 capitalize">{key} Notifications</label>
                    <p className="text-sm text-gray-500">
                      {key === 'email' && 'Receive notifications via email'}
                      {key === 'push' && 'Show browser notifications'}
                      {key === 'updates' && 'Product updates and announcements'}
                      {key === 'security' && 'Security alerts and warnings'}
                    </p>
                  </div>
                  <button
                    onClick={() => updateSetting('notifications', key, !value)}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      value ? 'bg-primary-600' : 'bg-gray-200'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                        value ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* API Configuration */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-6">
              <Database size={20} className="text-green-500" />
              <h3 className="text-lg font-semibold">API Configuration</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Search API Endpoint
                </label>
                <input 
                  type="text" 
                  value={settings.api.searchUrl}
                  onChange={(e) => updateSetting('api', 'searchUrl', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Graph API Endpoint
                </label>
                <input 
                  type="text" 
                  value={settings.api.graphUrl}
                  onChange={(e) => updateSetting('api', 'graphUrl', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Document Entities API
                </label>
                <input 
                  type="text" 
                  value={settings.api.docsUrl}
                  onChange={(e) => updateSetting('api', 'docsUrl', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  NLP API Endpoint
                </label>
                <input 
                  type="text" 
                  value={settings.api.nlpUrl}
                  onChange={(e) => updateSetting('api', 'nlpUrl', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </div>
          </div>

          {/* Data & Sync Settings */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-6">
              <RefreshCw size={20} className="text-orange-500" />
              <h3 className="text-lg font-semibold">Data & Sync</h3>
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700">Auto Refresh</label>
                  <p className="text-sm text-gray-500">Automatically refresh data in the background</p>
                </div>
                <button
                  onClick={() => updateSetting('', 'autoRefresh', !settings.autoRefresh)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.autoRefresh ? 'bg-primary-600' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                      settings.autoRefresh ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700">Refresh Interval</label>
                  <p className="text-sm text-gray-500">How often to refresh data (seconds)</p>
                </div>
                <select 
                  value={settings.refreshInterval}
                  onChange={(e) => updateSetting('', 'refreshInterval', parseInt(e.target.value))}
                  disabled={!settings.autoRefresh}
                  className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 disabled:bg-gray-100"
                >
                  <option value={10}>10 seconds</option>
                  <option value={30}>30 seconds</option>
                  <option value={60}>1 minute</option>
                  <option value={300}>5 minutes</option>
                </select>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-between pt-6">
            <button
              onClick={resetToDefaults}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Reset to Defaults
            </button>
            
            <div className="flex items-center gap-3">
              {saved && (
                <span className="text-green-600 text-sm font-medium">Settings saved!</span>
              )}
              <button
                onClick={handleSave}
                className="flex items-center gap-2 px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 focus:ring-2 focus:ring-primary-500"
              >
                <Save size={16} />
                Save Settings
              </button>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
