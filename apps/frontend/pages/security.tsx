// apps/frontend/pages/security.tsx - Security Settings Page
import { useState } from 'react';
import { 
  AlertTriangle, 
  Shield, 
  Key, 
  Users, 
  Activity, 
  Lock,
  CheckCircle,
  XCircle,
  Clock
} from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';

export default function SecurityPage() {
  const [auditLogs, setAuditLogs] = useState([
    { id: 1, action: 'User login', user: 'admin', timestamp: '2024-03-01 10:30:00', status: 'success' },
    { id: 2, action: 'Document access', user: 'john.doe', timestamp: '2024-03-01 10:25:00', status: 'success' },
    { id: 3, action: 'Failed login', user: 'unknown', timestamp: '2024-03-01 10:20:00', status: 'failed' },
  ]);

  return (
    <DashboardLayout title="Security" subtitle="Manage security settings and access control">
      <div className="p-6">
        <div className="max-w-6xl space-y-6">
          
          {/* Security Overview */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-6">
              <Shield size={24} className="text-blue-500" />
              <h3 className="text-lg font-semibold">Security Overview</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-sm text-green-600 font-medium">System Status</div>
                  <CheckCircle size={16} className="text-green-600" />
                </div>
                <div className="text-lg font-bold text-green-800">Secure</div>
              </div>
              
              <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-sm text-blue-600 font-medium">Active Sessions</div>
                  <Users size={16} className="text-blue-600" />
                </div>
                <div className="text-lg font-bold text-blue-800">3</div>
              </div>
              
              <div className="p-4 bg-orange-50 rounded-lg border border-orange-200">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-sm text-orange-600 font-medium">Failed Attempts</div>
                  <AlertTriangle size={16} className="text-orange-600" />
                </div>
                <div className="text-lg font-bold text-orange-800">2</div>
              </div>
              
              <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-sm text-purple-600 font-medium">Last Audit</div>
                  <Clock size={16} className="text-purple-600" />
                </div>
                <div className="text-lg font-bold text-purple-800">2 days ago</div>
              </div>
            </div>
          </div>

          {/* Security Settings Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Authentication Settings */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center gap-3 mb-4">
                <Key size={20} className="text-indigo-500" />
                <h3 className="text-lg font-semibold">Authentication</h3>
              </div>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Two-Factor Authentication</label>
                    <p className="text-sm text-gray-500">Add an extra layer of security</p>
                  </div>
                  <button className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700">
                    Enable
                  </button>
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Session Timeout</label>
                    <p className="text-sm text-gray-500">Auto logout after inactivity</p>
                  </div>
                  <select className="px-3 py-1 text-sm border border-gray-300 rounded">
                    <option>30 minutes</option>
                    <option>1 hour</option>
                    <option>2 hours</option>
                    <option>Never</option>
                  </select>
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Password Policy</label>
                    <p className="text-sm text-gray-500">Minimum 8 characters, mixed case</p>
                  </div>
                  <span className="text-green-600 text-sm">✓ Active</span>
                </div>
              </div>
            </div>

            {/* Access Control */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center gap-3 mb-4">
                <Lock size={20} className="text-red-500" />
                <h3 className="text-lg font-semibold">Access Control</h3>
              </div>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">IP Whitelisting</label>
                    <p className="text-sm text-gray-500">Restrict access to specific IPs</p>
                  </div>
                  <button className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50">
                    Configure
                  </button>
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">API Rate Limiting</label>
                    <p className="text-sm text-gray-500">Limit requests per minute</p>
                  </div>
                  <select className="px-3 py-1 text-sm border border-gray-300 rounded">
                    <option>100/min</option>
                    <option>500/min</option>
                    <option>1000/min</option>
                    <option>Unlimited</option>
                  </select>
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Document Encryption</label>
                    <p className="text-sm text-gray-500">Encrypt sensitive documents</p>
                  </div>
                  <span className="text-green-600 text-sm">✓ Enabled</span>
                </div>
              </div>
            </div>
          </div>

          {/* Audit Log */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <Activity size={20} className="text-gray-500" />
                <h3 className="text-lg font-semibold">Security Audit Log</h3>
              </div>
              <button className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200">
                Export Log
              </button>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-medium text-gray-700">Action</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">User</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">Timestamp</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {auditLogs.map(log => (
                    <tr key={log.id} className="border-b border-gray-100">
                      <td className="py-3 px-4">{log.action}</td>
                      <td className="py-3 px-4">{log.user}</td>
                      <td className="py-3 px-4">{log.timestamp}</td>
                      <td className="py-3 px-4">
                        <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${
                          log.status === 'success' 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {log.status === 'success' ? (
                            <CheckCircle size={12} />
                          ) : (
                            <XCircle size={12} />
                          )}
                          {log.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Security Alerts */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <AlertTriangle size={20} className="text-yellow-600" />
              <h3 className="text-lg font-semibold text-yellow-800">Security Recommendations</h3>
            </div>
            
            <ul className="space-y-2 text-sm text-yellow-700">
              <li>• Enable two-factor authentication for admin accounts</li>
              <li>• Review and update API access permissions</li>
              <li>• Consider implementing IP whitelisting for production</li>
              <li>• Schedule regular security audits</li>
            </ul>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
