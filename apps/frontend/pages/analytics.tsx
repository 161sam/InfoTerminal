// apps/frontend/pages/analytics.tsx - Analytics Dashboard

import { useState, useEffect } from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  FileText, 
  Network,
  Activity,
  Download,
  Filter,
  Calendar
} from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { TimeSeriesChart, MultiSeriesChart, DonutChart, MetricCard } from '@/components/charts';

interface AnalyticsData {
  overview: {
    totalDocuments: number;
    totalEntities: number;
    totalSearches: number;
    activeUsers: number;
    trends: {
      documents: number;
      entities: number;
      searches: number;
      users: number;
    };
  };
  documentStats: Array<{ date: string; count: number; size: number }>;
  entityTypes: Array<{ type: string; count: number }>;
  searchActivity: Array<{ date: string; queries: number; users: number }>;
  topEntities: Array<{ name: string; type: string; mentions: number }>;
}

const MOCK_DATA: AnalyticsData = {
  overview: {
    totalDocuments: 12847,
    totalEntities: 45621,
    totalSearches: 8934,
    activeUsers: 156,
    trends: { documents: 12, entities: 8, searches: 23, users: -5 }
  },
  documentStats: Array.from({ length: 30 }, (_, i) => ({
    date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    count: Math.floor(Math.random() * 50) + 20,
    size: Math.floor(Math.random() * 1000) + 500
  })),
  entityTypes: [
    { type: 'Person', count: 15234 },
    { type: 'Organization', count: 12456 },
    { type: 'Location', count: 9876 },
    { type: 'Email', count: 6789 },
    { type: 'Domain', count: 4321 }
  ],
  searchActivity: Array.from({ length: 24 }, (_, i) => ({
    date: `${i.toString().padStart(2, '0')}:00`,
    queries: Math.floor(Math.random() * 100) + 20,
    users: Math.floor(Math.random() * 50) + 10
  })),
  topEntities: [
    { name: 'ACME Corp', type: 'Organization', mentions: 1234 },
    { name: 'John Smith', type: 'Person', mentions: 987 },
    { name: 'London', type: 'Location', mentions: 756 },
    { name: 'contact@acme.com', type: 'Email', mentions: 543 },
    { name: 'New York', type: 'Location', mentions: 432 }
  ]
};

export default function AnalyticsPage() {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('30d');

  useEffect(() => {
    // Simulate API call
    const timer = setTimeout(() => {
      setData(MOCK_DATA);
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, [timeRange]);

  const handleExport = () => {
    // Export analytics data
    const csv = generateCSV(data);
    downloadCSV(csv, 'analytics-report.csv');
  };

  if (loading || !data) {
    return (
      <DashboardLayout title="Analytics" subtitle="System performance and usage insights">
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="bg-white dark:bg-gray-900 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-800 animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-1/2 mb-4"></div>
                <div className="h-3 bg-gray-200 rounded w-full"></div>
              </div>
            ))}
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="Analytics" subtitle="System performance and usage insights">
      <div className="p-6 space-y-8">
        
        {/* Controls */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Calendar size={16} className="text-gray-500" />
              <select 
                value={timeRange} 
                onChange={(e) => setTimeRange(e.target.value)}
                className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              >
                <option value="7d">Last 7 days</option>
                <option value="30d">Last 30 days</option>
                <option value="90d">Last 90 days</option>
                <option value="1y">Last year</option>
              </select>
            </div>
            <button className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
              <Filter size={16} />
              Filters
            </button>
          </div>
          
          <button 
            onClick={handleExport}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700"
          >
            <Download size={16} />
            Export Report
          </button>
        </div>

        {/* Overview Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <MetricCard
            title="Documents"
            value={data.overview.totalDocuments.toLocaleString()}
            change={{ value: data.overview.trends.documents, period: 'vs last month' }}
            chart={{
              data: data.documentStats.slice(-7),
              dataKey: 'count',
              color: '#0ea5e9'
            }}
            icon={FileText}
          />
          
          <MetricCard
            title="Entities"
            value={data.overview.totalEntities.toLocaleString()}
            change={{ value: data.overview.trends.entities, period: 'vs last month' }}
            icon={Users}
          />
          
          <MetricCard
            title="Searches"
            value={data.overview.totalSearches.toLocaleString()}
            change={{ value: data.overview.trends.searches, period: 'vs last month' }}
            icon={BarChart3}
          />
          
          <MetricCard
            title="Active Users"
            value={data.overview.activeUsers.toLocaleString()}
            change={{ value: data.overview.trends.users, period: 'vs last month' }}
            icon={Activity}
          />
        </div>

        {/* Charts Row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Document Activity */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">Document Activity</h3>
            <MultiSeriesChart
              data={data.documentStats}
              xKey="date"
              series={[
                { key: 'count', name: 'Documents Added', color: '#0ea5e9', type: 'line' },
                { key: 'size', name: 'Storage (MB)', color: '#8b5cf6', type: 'area' }
              ]}
              height={300}
              showLegend
            />
          </div>

          {/* Entity Distribution */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">Entity Types</h3>
            <DonutChart
              data={data.entityTypes}
              valueKey="count"
              nameKey="type"
              height={300}
              centerLabel="Total"
              centerValue={data.entityTypes.reduce((sum, item) => sum + item.count, 0).toLocaleString()}
            />
          </div>
        </div>

        {/* Charts Row 2 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Search Activity */}
          <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">Search Activity (24h)</h3>
            <MultiSeriesChart
              data={data.searchActivity}
              xKey="date"
              series={[
                { key: 'queries', name: 'Queries', color: '#22c55e', type: 'line' },
                { key: 'users', name: 'Active Users', color: '#f59e0b', type: 'area' }
              ]}
              height={280}
              showLegend
            />
          </div>

          {/* Top Entities */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">Top Entities</h3>
            <div className="space-y-4">
              {data.topEntities.map((entity, index) => (
                <div key={entity.name} className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-medium text-gray-500 bg-gray-100 px-2 py-1 rounded">
                        {entity.type}
                      </span>
                    </div>
                    <p className="text-sm font-medium text-gray-900 truncate mt-1">
                      {entity.name}
                    </p>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-sm text-gray-600">
                      {entity.mentions.toLocaleString()}
                    </span>
                    <div className="w-16 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-primary-600 h-2 rounded-full"
                        style={{
                          width: `${(entity.mentions / data.topEntities[0].mentions) * 100}%`
                        }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Performance Metrics */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">System Performance</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600 mb-1">98.5%</div>
              <div className="text-sm text-gray-600">Uptime</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600 mb-1">245ms</div>
              <div className="text-sm text-gray-600">Avg Query Time</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600 mb-1">1.2GB</div>
              <div className="text-sm text-gray-600">Index Size</div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

function generateCSV(data: AnalyticsData | null): string {
  if (!data) return '';
  
  const rows = [
    ['Metric', 'Value', 'Trend'],
    ['Total Documents', data.overview.totalDocuments.toString(), `${data.overview.trends.documents}%`],
    ['Total Entities', data.overview.totalEntities.toString(), `${data.overview.trends.entities}%`],
    ['Total Searches', data.overview.totalSearches.toString(), `${data.overview.trends.searches}%`],
    ['Active Users', data.overview.activeUsers.toString(), `${data.overview.trends.users}%`],
  ];
  
  return rows.map(row => row.join(',')).join('\n');
}

function downloadCSV(csv: string, filename: string) {
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
