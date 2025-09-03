// apps/frontend/pages/data.tsx - Data Management Page
import { useState, useEffect } from 'react';
import { 
  Database, 
  Upload, 
  Download, 
  RefreshCw, 
  Trash2, 
  AlertTriangle,
  CheckCircle,
  Clock,
  HardDrive,
  FileText,
  Users,
  BarChart3
} from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';

interface DataSource {
  id: string;
  name: string;
  type: string;
  status: 'active' | 'inactive' | 'syncing' | 'error';
  documents: number;
  lastSync: string;
  size: string;
}

interface StorageInfo {
  used: number;
  total: number;
  documents: number;
  entities: number;
  indices: number;
}

const MOCK_DATA_SOURCES: DataSource[] = [
  {
    id: '1',
    name: 'Document Storage',
    type: 'Elasticsearch',
    status: 'active',
    documents: 12847,
    lastSync: '2024-03-01 10:30:00',
    size: '2.4 GB'
  },
  {
    id: '2',
    name: 'Entity Database',
    type: 'Neo4j',
    status: 'active',
    documents: 45621,
    lastSync: '2024-03-01 10:25:00',
    size: '1.8 GB'
  },
  {
    id: '3',
    name: 'Aleph Integration',
    type: 'External API',
    status: 'inactive',
    documents: 0,
    lastSync: '2024-02-28 15:20:00',
    size: '0 MB'
  }
];

const MOCK_STORAGE: StorageInfo = {
  used: 4.2,
  total: 100,
  documents: 12847,
  entities: 45621,
  indices: 8
};

export default function DataPage() {
  const [dataSources, setDataSources] = useState<DataSource[]>(MOCK_DATA_SOURCES);
  const [storageInfo, setStorageInfo] = useState<StorageInfo>(MOCK_STORAGE);
  const [loading, setLoading] = useState(false);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100';
      case 'syncing': return 'text-blue-600 bg-blue-100';
      case 'error': return 'text-red-600 bg-red-100';
      case 'inactive': return 'text-gray-600 bg-gray-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <CheckCircle size={16} />;
      case 'syncing': return <RefreshCw size={16} className="animate-spin" />;
      case 'error': return <AlertTriangle size={16} />;
      case 'inactive': return <Clock size={16} />;
      default: return <Clock size={16} />;
    }
  };

  const handleSync = async (sourceId: string) => {
    setDataSources(prev => prev.map(source => 
      source.id === sourceId 
        ? { ...source, status: 'syncing' as const }
        : source
    ));

    // Simulate sync process
    setTimeout(() => {
      setDataSources(prev => prev.map(source => 
        source.id === sourceId 
          ? { 
              ...source, 
              status: 'active' as const, 
              lastSync: new Date().toISOString().slice(0, 19).replace('T', ' ')
            }
          : source
      ));
    }, 3000);
  };

  const handleExportData = () => {
    // Simulate data export
    const data = {
      dataSources,
      storageInfo,
      exportedAt: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'data-export.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <DashboardLayout title="Data Management" subtitle="Manage your data sources and storage">
      <div className="p-6 space-y-6">
        
        {/* Storage Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Storage Used</p>
                <p className="text-2xl font-bold text-gray-900">
                  {storageInfo.used} GB
                </p>
                <p className="text-xs text-gray-500">
                  of {storageInfo.total} GB total
                </p>
              </div>
              <HardDrive size={24} className="text-blue-500" />
            </div>
            <div className="mt-3">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-500 h-2 rounded-full" 
                  style={{ width: `${(storageInfo.used / storageInfo.total) * 100}%` }}
                />
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Documents</p>
                <p className="text-2xl font-bold text-gray-900">
                  {storageInfo.documents.toLocaleString()}
                </p>
              </div>
              <FileText size={24} className="text-green-500" />
            </div>
          </div>
          
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Entities</p>
                <p className="text-2xl font-bold text-gray-900">
                  {storageInfo.entities.toLocaleString()}
                </p>
              </div>
              <Users size={24} className="text-purple-500" />
            </div>
          </div>
          
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Indices</p>
                <p className="text-2xl font-bold text-gray-900">
                  {storageInfo.indices}
                </p>
              </div>
              <BarChart3 size={24} className="text-orange-500" />
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Data Sources */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold">Data Sources</h3>
                <button className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm">
                  Add Source
                </button>
              </div>
              
              <div className="space-y-4">
                {dataSources.map(source => (
                  <div key={source.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div className="flex items-center gap-4">
                      <Database size={20} className="text-gray-500" />
                      <div>
                        <h4 className="font-medium text-gray-900">{source.name}</h4>
                        <p className="text-sm text-gray-500">{source.type}</p>
                        <p className="text-xs text-gray-400">
                          {source.documents.toLocaleString()} documents • {source.size}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-3">
                      <div className="text-right">
                        <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(source.status)}`}>
                          {getStatusIcon(source.status)}
                          {source.status}
                        </div>
                        <p className="text-xs text-gray-500 mt-1">
                          Last sync: {new Date(source.lastSync).toLocaleString()}
                        </p>
                      </div>
                      
                      <div className="flex gap-1">
                        <button
                          onClick={() => handleSync(source.id)}
                          disabled={source.status === 'syncing'}
                          className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded disabled:opacity-50"
                        >
                          <RefreshCw size={16} className={source.status === 'syncing' ? 'animate-spin' : ''} />
                        </button>
                        <button className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded">
                          <Trash2 size={16} />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button className="w-full flex items-center gap-3 p-3 text-left bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors">
                  <Upload size={16} />
                  <div>
                    <div className="font-medium">Import Data</div>
                    <div className="text-xs text-blue-600">Upload documents or CSV</div>
                  </div>
                </button>
                
                <button 
                  onClick={handleExportData}
                  className="w-full flex items-center gap-3 p-3 text-left bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors"
                >
                  <Download size={16} />
                  <div>
                    <div className="font-medium">Export Data</div>
                    <div className="text-xs text-green-600">Download as JSON/CSV</div>
                  </div>
                </button>
                
                <button className="w-full flex items-center gap-3 p-3 text-left bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors">
                  <RefreshCw size={16} />
                  <div>
                    <div className="font-medium">Sync All</div>
                    <div className="text-xs text-purple-600">Refresh all data sources</div>
                  </div>
                </button>
                
                <button className="w-full flex items-center gap-3 p-3 text-left bg-orange-50 text-orange-700 rounded-lg hover:bg-orange-100 transition-colors">
                  <BarChart3 size={16} />
                  <div>
                    <div className="font-medium">Rebuild Index</div>
                    <div className="text-xs text-orange-600">Reindex search data</div>
                  </div>
                </button>
              </div>
            </div>

            {/* Data Health */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold mb-4">Data Health</h3>
              
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Search Index</span>
                  <div className="flex items-center gap-2">
                    <CheckCircle size={16} className="text-green-500" />
                    <span className="text-sm font-medium text-green-600">Healthy</span>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Entity Resolution</span>
                  <div className="flex items-center gap-2">
                    <CheckCircle size={16} className="text-green-500" />
                    <span className="text-sm font-medium text-green-600">Optimal</span>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Graph Database</span>
                  <div className="flex items-center gap-2">
                    <AlertTriangle size={16} className="text-yellow-500" />
                    <span className="text-sm font-medium text-yellow-600">Warning</span>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Backup Status</span>
                  <div className="flex items-center gap-2">
                    <Clock size={16} className="text-blue-500" />
                    <span className="text-sm font-medium text-blue-600">2h ago</span>
                  </div>
                </div>
              </div>
              
              <div className="mt-4 pt-4 border-t border-gray-200">
                <button className="w-full px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200">
                  View Detailed Report
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
          
          <div className="space-y-3">
            <div className="flex items-center gap-3 text-sm">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-gray-500">2 minutes ago</span>
              <span>Document batch imported: 45 new documents</span>
            </div>
            <div className="flex items-center gap-3 text-sm">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span className="text-gray-500">15 minutes ago</span>
              <span>Entity extraction completed for document batch #1247</span>
            </div>
            <div className="flex items-center gap-3 text-sm">
              <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
              <span className="text-gray-500">1 hour ago</span>
              <span>Search index optimized: 12% performance improvement</span>
            </div>
            <div className="flex items-center gap-3 text-sm">
              <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
              <span className="text-gray-500">3 hours ago</span>
              <span>Automated backup completed: 2.4 GB backed up</span>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
