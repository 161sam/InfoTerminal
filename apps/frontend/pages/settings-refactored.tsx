import { useCallback } from "react";
import {
  Settings, 
  Server, 
  CheckCircle, 
  Info, 
  Monitor, 
  Globe,
  Shield,
  Palette,
  Bell,
  User,
  Search,
  Database,
  Brain,
  Eye,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { useRouter } from "next/router";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import SettingsGateway from "@/components/settings/SettingsGateway";
import OpsTab from "@/components/settings/OpsTab";
import UserManagementTab from "@/components/settings/UserManagementTab";
import SecurityPanel from "@/components/settings/SecurityPanel";
import { EndpointsTab, AppearanceTab, NotificationsTab, AboutTab } from "@/components/settings/tabs";
import { loadEndpoints, EndpointSettings } from "@/lib/endpoints";
import { useActiveTab } from "@/hooks/useActiveTab";

type SettingsTab =
  | 'endpoints'
  | 'ops'
  | 'gateway'
  | 'appearance'
  | 'notifications'
  | 'security'
  | 'user-management'
  | 'about';

const SETTINGS_TABS: SettingsTab[] = [
  'endpoints',
  'ops',
  'gateway',
  'appearance',
  'notifications',
  'security',
  'user-management',
  'about',
];

const SETTINGS_TAB_PARAM = 'tab';

interface ServiceEndpoint {
  key: keyof EndpointSettings;
  label: string;
  description: string;
  icon: LucideIcon;
  required: boolean;
  defaultPort?: string;
}

const SERVICE_ENDPOINTS: ServiceEndpoint[] = [
  {
    key: "SEARCH_API",
    label: "Search API",
    description: "Full-text search and document indexing service",
    icon: Search,
    required: true,
    defaultPort: "8001"
  },
  {
    key: "GRAPH_API",
    label: "Graph Database API",
    description: "Neo4j graph database for relationship analysis",
    icon: Database,
    required: true,
    defaultPort: "7474"
  },
  {
    key: "DOCENTITIES_API",
    label: "Document Entities API",
    description: "NLP service for entity extraction and document processing",
    icon: Brain,
    required: true,
    defaultPort: "8003"
  },
  {
    key: "VIEWS_API",
    label: "Views API",
    description: "Data visualization and analytics service",
    icon: Eye,
    required: false,
    defaultPort: "8004"
  },
  {
    key: "NLP_API",
    label: "NLP Processing API",
    description: "Advanced natural language processing capabilities",
    icon: Brain,
    required: false,
    defaultPort: "8005"
  }
];

const isSettingsTab = (value: string): value is SettingsTab =>
  SETTINGS_TABS.includes(value as SettingsTab);

export default function SettingsPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useActiveTab<SettingsTab>({
    defaultTab: 'endpoints',
    validTabs: SETTINGS_TABS,
    urlParam: SETTINGS_TAB_PARAM,
    router
  });

  const handleTabSelect = useCallback((tab: SettingsTab) => {
    setActiveTab(tab);
  }, [setActiveTab]);

  const TabButton = ({ id, label, icon: Icon }: { id: SettingsTab; label: string; icon: LucideIcon }) => (
    <button
      onClick={() => handleTabSelect(id)}
      className={`inline-flex items-center gap-2 px-4 py-3 text-sm rounded-lg transition-colors ${
        activeTab === id
          ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
          : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200 hover:bg-gray-100 dark:hover:bg-gray-800'
      }`}
    >
      <Icon size={16} />
      {label}
    </button>
  );

  const getEndpointSummary = () => {
    const endpoints = loadEndpoints();
    const total = SERVICE_ENDPOINTS.length;
    const configured = SERVICE_ENDPOINTS.filter(ep => endpoints[ep.key]).length;
    return { total, configured, healthy: 0 }; // Health status would be managed in EndpointsTab
  };

  return (
    <DashboardLayout title="Settings" subtitle="Configure your intelligence platform">
      <div className="max-w-6xl mx-auto space-y-6">
        
        {/* Settings Overview */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-900/30">
            <div className="flex items-center gap-3">
              <Server size={20} className="text-blue-600 dark:text-blue-400" />
              <div>
                <div className="text-sm text-blue-600 dark:text-blue-400 font-medium">Services</div>
                <div className="text-lg font-bold text-blue-800 dark:text-blue-300">
                  {getEndpointSummary().configured}/{getEndpointSummary().total}
                </div>
              </div>
            </div>
          </div>
          
          <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-900/30">
            <div className="flex items-center gap-3">
              <CheckCircle size={20} className="text-green-600 dark:text-green-400" />
              <div>
                <div className="text-sm text-green-600 dark:text-green-400 font-medium">Healthy</div>
                <div className="text-lg font-bold text-green-800 dark:text-green-300">
                  {getEndpointSummary().healthy}
                </div>
              </div>
            </div>
          </div>
          
          <div className="p-4 bg-amber-50 dark:bg-amber-900/20 rounded-lg border border-amber-200 dark:border-amber-900/30">
            <div className="flex items-center gap-3">
              <Monitor size={20} className="text-amber-600 dark:text-amber-400" />
              <div>
                <div className="text-sm text-amber-600 dark:text-amber-400 font-medium">Operations</div>
                <div className="text-lg font-bold text-amber-800 dark:text-amber-300">
                  Active
                </div>
              </div>
            </div>
          </div>
          
          <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-900/30">
            <div className="flex items-center gap-3">
              <Palette size={20} className="text-purple-600 dark:text-purple-400" />
              <div>
                <div className="text-sm text-purple-600 dark:text-purple-400 font-medium">Theme</div>
                <div className="text-lg font-bold text-purple-800 dark:text-purple-300 capitalize">
                  System
                </div>
              </div>
            </div>
          </div>
          
          <div className="p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-900/30">
            <div className="flex items-center gap-3">
              <Globe size={20} className="text-orange-600 dark:text-orange-400" />
              <div>
                <div className="text-sm text-orange-600 dark:text-orange-400 font-medium">Runtime</div>
                <div className="text-lg font-bold text-orange-800 dark:text-orange-300">
                  {typeof window === "undefined" ? "Server" : "Client"}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex flex-wrap gap-2 bg-gray-50 dark:bg-gray-800 p-2 rounded-lg">
          <TabButton id="endpoints" label="API Endpoints" icon={Server} />
          <TabButton id="ops" label="Operations" icon={Monitor} />
          <TabButton id="gateway" label="Gateway" icon={Settings} />
          <TabButton id="appearance" label="Appearance" icon={Palette} />
          <TabButton id="notifications" label="Notifications" icon={Bell} />
          <TabButton id="security" label="Security" icon={Shield} />
          <TabButton id="user-management" label="User Management" icon={User} />
          <TabButton id="about" label="About" icon={Info} />
        </div>

        {/* Tab Content */}
        <div className="space-y-6">
          {activeTab === 'endpoints' && (
            <EndpointsTab serviceEndpoints={SERVICE_ENDPOINTS} />
          )}

          {activeTab === 'ops' && (
            <Panel>
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-2">Operations Dashboard</h3>
                  <p className="text-sm text-gray-600 dark:text-slate-400">Monitor system performance and manage operational tasks</p>
                </div>
                <OpsTab />
              </div>
            </Panel>
          )}

          {activeTab === 'gateway' && (
            <Panel>
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-2">API Gateway Configuration</h3>
                  <p className="text-sm text-gray-600 dark:text-slate-400">Configure routing and load balancing for your services</p>
                </div>
                <SettingsGateway />
              </div>
            </Panel>
          )}

          {activeTab === 'appearance' && <AppearanceTab />}
          {activeTab === 'notifications' && <NotificationsTab />}
          {activeTab === 'security' && <SecurityPanel />}
          {activeTab === 'user-management' && <UserManagementTab mode="demo" />}
          {activeTab === 'about' && <AboutTab />}
        </div>
      </div>
    </DashboardLayout>
  );
}
