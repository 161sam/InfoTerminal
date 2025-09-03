// apps/frontend/pages/index.tsx - Moderne Dashboard Homepage
import { useEffect, useState } from 'react';
import { 
  Search, 
  FileText, 
  Network, 
  TrendingUp, 
  Users, 
  Database,
  Activity,
  ArrowUpRight,
  ArrowDownRight,
  BarChart3,
  Clock,
  AlertTriangle
} from 'lucide-react';
import DashboardLayout from '../src/components/layout/DashboardLayout';
import { useHealth } from '../src/hooks/useHealth';

interface DashboardStats {
  totalDocuments: number;
  totalEntities: number;
  graphNodes: number;
  searchQueries: number;
  trends: {
    documents: number;
    entities: number;
    queries: number;
  };
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const { data: healthData } = useHealth();

  useEffect(() => {
    // Simulate fetching dashboard stats
    const mockStats: DashboardStats = {
      totalDocuments: 12847,
      totalEntities: 45621,
      graphNodes: 8934,
      searchQueries: 2341,
      trends: {
        documents: 12,
        entities: -3,
        queries: 28
      }
    };
    setStats(mockStats);
  }, []);

  return (
    <DashboardLayout title="Dashboard" subtitle="Intelligence Platform Overview">
      <div className="p-6 space-y-6">
        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatsCard
            title="Documents"
            value={stats?.totalDocuments.toLocaleString() || '0'}
            icon={FileText}
            trend={stats?.trends.documents}
            color="blue"
          />
          <StatsCard
            title="Entities"
            value={stats?.totalEntities.toLocaleString() || '0'}
            icon={Users}
            trend={stats?.trends.entities}
            color="purple"
          />
          <StatsCard
            title="Graph Nodes"
            value={stats?.graphNodes.toLocaleString() || '0'}
            icon={Network}
            trend={15}
            color="green"
          />
          <StatsCard
            title="Search Queries"
            value={stats?.searchQueries.toLocaleString() || '0'}
            icon={Search}
            trend={stats?.trends.queries}
            color="orange"
          />
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Quick Search */}
          <div className="lg:col-span-2">
            <QuickSearchWidget />
          </div>

          {/* System Health */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">System Health</h3>
              <Activity size={20} className="text-gray-400" />
            </div>
            
            {healthData && (
              <div className="space-y-3">
                {Object.entries(healthData.services).map(([name, service]) => (
                  <div key={name} className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700 capitalize">{name}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-gray-500">
                        {service.latencyMs ? `${service.latencyMs}ms` : '–'}
                      </span>
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                        service.state === 'ok' ? 'bg-green-100 text-green-800' :
                        service.state === 'degraded' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {service.state}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Recent Activity & Quick Actions */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          {/* Recent Activity */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
              <Clock size={20} className="text-gray-400" />
            </div>
            
            <div className="space-y-4">
              <ActivityItem
                type="search"
                title="Complex query executed"
                description="Search for 'financial connections ACME'"
                time="2 minutes ago"
                icon={Search}
              />
              <ActivityItem
                type="document"
                title="New document ingested"
                description="Financial report Q3-2024.pdf"
                time="15 minutes ago"
                icon={FileText}
              />
              <ActivityItem
                type="graph"
                title="Graph analysis completed"
                description="Network analysis for Organization cluster"
                time="1 hour ago"
                icon={Network}
              />
              <ActivityItem
                type="alert"
                title="Entity resolution match"
                description="High confidence match found for Person entity"
                time="2 hours ago"
                icon={AlertTriangle}
              />
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">Quick Actions</h3>
            
            <div className="grid grid-cols-2 gap-4">
              <QuickActionCard
                title="Advanced Search"
                description="Run complex queries"
                href="/search"
                icon={Search}
                color="blue"
              />
              <QuickActionCard
                title="Graph Explorer"
                description="Visualize connections"
                href="/graphx"
                icon={Network}
                color="green"
              />
              <QuickActionCard
                title="Upload Documents"
                description="Add new sources"
                href="/documents"
                icon={FileText}
                color="purple"
              />
              <QuickActionCard
                title="Analytics"
                description="View insights"
                href="/analytics"
                icon={BarChart3}
                color="orange"
              />
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

function StatsCard({ title, value, icon: Icon, trend, color }: {
  title: string;
  value: string;
  icon: React.ComponentType<{ size?: number; className?: string }>;
  trend?: number;
  color: 'blue' | 'purple' | 'green' | 'orange';
}) {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    purple: 'bg-purple-50 text-purple-600',
    green: 'bg-green-50 text-green-600',
    orange: 'bg-orange-50 text-orange-600'
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          <Icon size={24} />
        </div>
      </div>
      
      {trend !== undefined && (
        <div className="mt-4 flex items-center">
          <div className={`flex items-center ${trend >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {trend >= 0 ? <ArrowUpRight size={16} /> : <ArrowDownRight size={16} />}
            <span className="text-sm font-medium">{Math.abs(trend)}%</span>
          </div>
          <span className="text-sm text-gray-500 ml-2">vs last week</span>
        </div>
      )}
    </div>
  );
}

function QuickSearchWidget() {
  const [query, setQuery] = useState('');

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Search</h3>
      
      <div className="relative mb-4">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search across all data sources..."
          className="block w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        />
      </div>
      
      <div className="flex flex-wrap gap-2">
        {['Financial networks', 'Recent documents', 'Entity connections', 'Risk indicators'].map((suggestion) => (
          <button
            key={suggestion}
            onClick={() => setQuery(suggestion)}
            className="px-3 py-2 text-sm text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            {suggestion}
          </button>
        ))}
      </div>
    </div>
  );
}

function ActivityItem({ type, title, description, time, icon: Icon }: {
  type: string;
  title: string;
  description: string;
  time: string;
  icon: React.ComponentType<{ size?: number; className?: string }>;
}) {
  return (
    <div className="flex items-start gap-3">
      <div className="p-2 bg-gray-100 rounded-lg">
        <Icon size={16} className="text-gray-600" />
      </div>
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-900">{title}</p>
        <p className="text-sm text-gray-600">{description}</p>
        <p className="text-xs text-gray-500 mt-1">{time}</p>
      </div>
    </div>
  );
}

function QuickActionCard({ title, description, href, icon: Icon, color }: {
  title: string;
  description: string;
  href: string;
  icon: React.ComponentType<{ size?: number; className?: string }>;
  color: 'blue' | 'purple' | 'green' | 'orange';
}) {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600 hover:bg-blue-100',
    purple: 'bg-purple-50 text-purple-600 hover:bg-purple-100',
    green: 'bg-green-50 text-green-600 hover:bg-green-100',
    orange: 'bg-orange-50 text-orange-600 hover:bg-orange-100'
  };

  return (
    <a
      href={href}
      className={`block p-4 rounded-lg transition-colors ${colorClasses[color]}`}
    >
      <Icon size={20} className="mb-2" />
      <h4 className="text-sm font-semibold text-gray-900">{title}</h4>
      <p className="text-xs text-gray-600">{description}</p>
    </a>
  );
}