// apps/frontend/pages/entities.tsx - Entity Management Page

import { useState, useEffect } from 'react';
import { 
  User, 
  Building2, 
  MapPin, 
  Mail, 
  Globe, 
  Network,
  Search,
  Filter,
  Download,
  Eye,
  Edit,
  Trash2
} from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { DataTable, Column, TableAction } from '@/components/ui/DataTable';
import EntityBadge from '@/components/entities/EntityBadge';
import { EntityLabel, normalizeLabel } from '@/lib/entities';

interface Entity {
  id: string;
  name: string;
  type: EntityLabel;
  mentions: number;
  confidence: number;
  firstSeen: string;
  lastSeen: string;
  sources: string[];
  verified: boolean;
}

const MOCK_ENTITIES: Entity[] = [
  {
    id: '1',
    name: 'John Smith',
    type: 'Person',
    mentions: 156,
    confidence: 0.95,
    firstSeen: '2024-01-15',
    lastSeen: '2024-03-01',
    sources: ['document-1', 'document-5'],
    verified: true
  },
  {
    id: '2',
    name: 'ACME Corporation',
    type: 'Organization',
    mentions: 243,
    confidence: 0.98,
    firstSeen: '2024-01-10',
    lastSeen: '2024-03-02',
    sources: ['document-2', 'document-3', 'document-8'],
    verified: true
  },
  {
    id: '3',
    name: 'London',
    type: 'Location',
    mentions: 89,
    confidence: 0.92,
    firstSeen: '2024-01-20',
    lastSeen: '2024-02-28',
    sources: ['document-4'],
    verified: false
  },
  {
    id: '4',
    name: 'john.smith@acme.com',
    type: 'Email',
    mentions: 67,
    confidence: 0.99,
    firstSeen: '2024-02-01',
    lastSeen: '2024-03-01',
    sources: ['document-1', 'document-6'],
    verified: false
  },
  {
    id: '5',
    name: 'acme.com',
    type: 'Domain',
    mentions: 45,
    confidence: 0.87,
    firstSeen: '2024-01-25',
    lastSeen: '2024-02-29',
    sources: ['document-2'],
    verified: true
  }
];

export default function EntitiesPage() {
  const [entities, setEntities] = useState<Entity[]>(MOCK_ENTITIES);
  const [loading, setLoading] = useState(false);
  const [selectedType, setSelectedType] = useState<string>('all');

  const columns: Column<Entity>[] = [
    {
      key: 'name',
      header: 'Entity Name',
      sortable: true,
      filterable: true,
      render: (value, row) => (
        <div className="flex items-center gap-3">
          <EntityBadge label={row.type} size="sm" />
          <div>
            <div className="font-medium text-gray-900">{value}</div>
            <div className="text-sm text-gray-500">{row.type}</div>
          </div>
        </div>
      )
    },
    {
      key: 'mentions',
      header: 'Mentions',
      sortable: true,
      align: 'center',
      render: (value) => (
        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
          {value}
        </span>
      )
    },
    {
      key: 'confidence',
      header: 'Confidence',
      sortable: true,
      align: 'center',
      render: (value) => (
        <div className="flex items-center gap-2">
          <div className="w-16 bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full ${
                value >= 0.9 ? 'bg-green-500' : value >= 0.7 ? 'bg-yellow-500' : 'bg-red-500'
              }`}
              style={{ width: `${value * 100}%` }}
            />
          </div>
          <span className="text-sm text-gray-600">{Math.round(value * 100)}%</span>
        </div>
      )
    },
    {
      key: 'verified',
      header: 'Status',
      sortable: true,
      align: 'center',
      render: (value) => (
        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
          value 
            ? 'bg-green-100 text-green-800' 
            : 'bg-gray-100 text-gray-800'
        }`}>
          {value ? 'Verified' : 'Pending'}
        </span>
      )
    },
    {
      key: 'sources',
      header: 'Sources',
      align: 'center',
      render: (value) => (
        <span className="text-sm text-gray-600">{value.length}</span>
      )
    },
    {
      key: 'lastSeen',
      header: 'Last Seen',
      sortable: true,
      render: (value) => new Date(value).toLocaleDateString()
    }
  ];

  const actions: TableAction<Entity>[] = [
    {
      label: 'View Details',
      icon: Eye as any,
      onClick: (row) => {
        // Navigate to entity detail page
        console.log('View entity:', row.id);
      }
    },
    {
      label: 'Edit Entity',
      icon: Edit,
      onClick: (row) => {
        // Open edit modal
        console.log('Edit entity:', row.id);
      }
    },
    {
      label: 'View in Graph',
      icon: Network,
      onClick: (row) => {
        window.open(`/graphx?focus=${encodeURIComponent(row.name)}`, '_blank');
      }
    },
    {
      label: 'Delete Entity',
      icon: Trash2,
      color: 'danger',
      onClick: (row) => {
        if (confirm(`Are you sure you want to delete "${row.name}"?`)) {
          setEntities(prev => prev.filter(e => e.id !== row.id));
        }
      }
    }
  ];

  const filteredEntities = selectedType === 'all' 
    ? entities 
    : entities.filter(e => e.type === selectedType);

  const entityStats = {
    total: entities.length,
    verified: entities.filter(e => e.verified).length,
    pending: entities.filter(e => !e.verified).length,
    types: {
      Person: entities.filter(e => e.type === 'Person').length,
      Organization: entities.filter(e => e.type === 'Organization').length,
      Location: entities.filter(e => e.type === 'Location').length,
      Email: entities.filter(e => e.type === 'Email').length,
      Domain: entities.filter(e => e.type === 'Domain').length,
    }
  };

  const handleExport = () => {
    const csv = entities.map(e => [
      e.name,
      e.type,
      e.mentions,
      e.confidence,
      e.verified ? 'Verified' : 'Pending',
      e.sources.length,
      e.firstSeen,
      e.lastSeen
    ].join(',')).join('\n');
    
    const headers = ['Name', 'Type', 'Mentions', 'Confidence', 'Status', 'Sources', 'First Seen', 'Last Seen'];
    const fullCsv = headers.join(',') + '\n' + csv;
    
    const blob = new Blob([fullCsv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'entities.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <DashboardLayout title="Entities" subtitle="Manage and explore detected entities">
      <div className="p-6 space-y-6">
        
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Entities</p>
                <p className="text-2xl font-bold text-gray-900">{entityStats.total}</p>
              </div>
              <User size={24} className="text-blue-500" />
            </div>
          </div>
          
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Verified</p>
                <p className="text-2xl font-bold text-green-600">{entityStats.verified}</p>
              </div>
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Pending</p>
                <p className="text-2xl font-bold text-yellow-600">{entityStats.pending}</p>
              </div>
              <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Organizations</p>
                <p className="text-2xl font-bold text-purple-600">{entityStats.types.Organization}</p>
              </div>
              <Building2 size={24} className="text-purple-500" />
            </div>
          </div>
          
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">People</p>
                <p className="text-2xl font-bold text-indigo-600">{entityStats.types.Person}</p>
              </div>
              <User size={24} className="text-indigo-500" />
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Filter size={16} className="text-gray-500" />
              <select 
                value={selectedType} 
                onChange={(e) => setSelectedType(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500"
              >
                <option value="all">All Types</option>
                <option value="Person">Person</option>
                <option value="Organization">Organization</option>
                <option value="Location">Location</option>
                <option value="Email">Email</option>
                <option value="Domain">Domain</option>
              </select>
            </div>
          </div>
          
          <button 
            onClick={handleExport}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700"
          >
            <Download size={16} />
            Export
          </button>
        </div>

        {/* Entity Type Distribution */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Entity Distribution</h3>
          <div className="flex flex-wrap gap-3">
            {Object.entries(entityStats.types).map(([type, count]) => (
              <EntityBadge 
                key={type}
                label={type as EntityLabel}
                value={`${count} entities`}
                onClick={() => setSelectedType(type)}
                clickable
              />
            ))}
          </div>
        </div>

        {/* Entities Table */}
        <DataTable
          data={filteredEntities}
          columns={columns}
          actions={actions}
          loading={loading}
          searchable
          exportable
          selectable
          onRowClick={(entity) => {
            // Navigate to entity detail or expand inline
            console.log('Selected entity:', entity);
          }}
          emptyState={
            <div className="text-center py-8">
              <User size={48} className="mx-auto text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No entities found</h3>
              <p className="text-gray-500">
                {selectedType === 'all' 
                  ? 'Upload some documents to start detecting entities.'
                  : `No ${selectedType.toLowerCase()} entities found.`
                }
              </p>
            </div>
          }
        />
      </div>
    </DashboardLayout>
  );
}
