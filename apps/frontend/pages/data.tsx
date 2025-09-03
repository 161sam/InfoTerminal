// apps/frontend/pages/data.tsx - Data Management Page
import { useState } from 'react';
import { Database, Upload, Download, RefreshCw, Trash2, AlertTriangle } from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';

export default function DataPage() {
  return (
    <DashboardLayout title="Data Management" subtitle="Manage your data sources and storage">
      <div className="p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold mb-4">Data Sources</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Database size={20} className="text-blue-500" />
                    <div>
                      <p className="font-medium">Document Storage</p>
                      <p className="text-sm text-gray-500">12,847 documents indexed</p>
                    </div>
                  </div>
                  <span className="text-green-600 text-sm font-medium">Active</span>
                </div>
              </div>
            </div>
          </div>
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button className="w-full flex items-center gap-2 p-3 text-left bg-gray-50 rounded-lg hover:bg-gray-100">
                  <Upload size={16} />
                  Import Data
                </button>
                <button className="w-full flex items-center gap-2 p-3 text-left bg-gray-50 rounded-lg hover:bg-gray-100">
                  <Download size={16} />
                  Export Data
                </button>
                <button className="w-full flex items-center gap-2 p-3 text-left bg-gray-50 rounded-lg hover:bg-gray-100">
                  <RefreshCw size={16} />
                  Sync Data
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

// apps/frontend/pages/security.tsx - Security Settings Page
export function SecurityPage() {
  return (
    <DashboardLayout title="Security" subtitle="Manage security settings and access control">
      <div className="p-6">
        <div className="max-w-4xl space-y-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-4">
              <AlertTriangle size={20} className="text-orange-500" />
              <h3 className="text-lg font-semibold">Security Overview</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                <div className="text-sm text-green-600 font-medium mb-1">System Status</div>
                <div className="text-lg font-bold text-green-800">Secure</div>
              </div>
              <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                <div className="text-sm text-blue-600 font-medium mb-1">Active Sessions</div>
                <div className="text-lg font-bold text-blue-800">3</div>
              </div>
              <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                <div className="text-sm text-purple-600 font-medium mb-1">Last Audit</div>
                <div className="text-lg font-bold text-purple-800">2 days ago</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

// apps/frontend/pages/settings.tsx - Settings Page
export function SettingsPage() {
  const [notifications, setNotifications] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  
  return (
    <DashboardLayout title="Settings" subtitle="Configure your application preferences">
      <div className="p-6">
        <div className="max-w-4xl space-y-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold mb-6">Preferences</h3>
            
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700">Notifications</label>
                  <p className="text-sm text-gray-500">Receive email notifications for updates</p>
                </div>
                <button
                  onClick={() => setNotifications(!notifications)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full ${
                    notifications ? 'bg-blue-600' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                      notifications ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700">Dark Mode</label>
                  <p className="text-sm text-gray-500">Use dark theme interface</p>
                </div>
                <button
                  onClick={() => setDarkMode(!darkMode)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full ${
                    darkMode ? 'bg-blue-600' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                      darkMode ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold mb-6">API Settings</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Search API Endpoint
                </label>
                <input 
                  type="text" 
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  defaultValue="http://localhost:8001"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Graph API Endpoint
                </label>
                <input 
                  type="text" 
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  defaultValue="http://localhost:8002"
                />
              </div>
            </div>
            
            <div className="mt-6 pt-6 border-t border-gray-200">
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                Save Settings
              </button>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

// Export all components
export { SecurityPage as Security, SettingsPage as Settings };
