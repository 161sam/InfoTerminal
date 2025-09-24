import { useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/router";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import SettingsGateway from "@/components/settings/SettingsGateway";
import OpsTab from "@/components/settings/OpsTab";
import UserManagementTab from "@/components/settings/UserManagementTab";
import SecurityPanel from "@/components/settings/SecurityPanel";
import {
  EndpointsTab,
  AppearanceTab,
  NotificationsTab,
  AboutTab,
} from "@/components/settings/tabs";
import SettingsOverview from "@/components/settings/overview/SettingsOverview";
import SettingsTabNavigation from "@/components/settings/navigation/SettingsTabNavigation";
import type { SettingsTab } from "@/components/settings/navigation/SettingsTabNavigation";
import { loadEndpoints, defaultEndpoints } from "@/lib/endpoints";
import { SERVICE_ENDPOINTS, calculateEndpointSummary } from "@/lib/settings/serviceEndpoints";
import { useActiveTab } from "@/hooks/useActiveTab";

const SETTINGS_TABS: SettingsTab[] = [
  "endpoints",
  "ops",
  "gateway",
  "appearance",
  "notifications",
  "security",
  "user-management",
  "about",
];

const SETTINGS_TAB_PARAM = "tab";

export default function SettingsPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useActiveTab<SettingsTab>({
    defaultTab: "endpoints",
    validTabs: SETTINGS_TABS,
    urlParam: SETTINGS_TAB_PARAM,
    router,
  });
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  const handleTabSelect = useCallback(
    (tab: SettingsTab) => {
      setActiveTab(tab);
    },
    [setActiveTab],
  );

  const overviewMetrics = useMemo(() => {
    const endpoints = isClient ? loadEndpoints() : defaultEndpoints;
    const endpointSummary = calculateEndpointSummary(endpoints);

    return {
      services: {
        configured: endpointSummary.configured,
        total: endpointSummary.total,
      },
      healthy: endpointSummary.healthy,
      operationsStatus: "Active" as const,
      theme: "System",
      runtime: isClient ? "Client" : "Server",
    };
  }, [isClient]);

  const renderTabContent = () => {
    switch (activeTab) {
      case "endpoints":
        return <EndpointsTab serviceEndpoints={SERVICE_ENDPOINTS} />;

      case "ops":
        return (
          <Panel>
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-2">
                  Operations Dashboard
                </h3>
                <p className="text-sm text-gray-600 dark:text-slate-400">
                  Monitor system performance and manage operational tasks
                </p>
              </div>
              <OpsTab />
            </div>
          </Panel>
        );

      case "gateway":
        return (
          <Panel>
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-2">
                  API Gateway Configuration
                </h3>
                <p className="text-sm text-gray-600 dark:text-slate-400">
                  Configure routing and load balancing for your services
                </p>
              </div>
              <SettingsGateway />
            </div>
          </Panel>
        );

      case "appearance":
        return <AppearanceTab />;

      case "notifications":
        return <NotificationsTab />;

      case "security":
        return <SecurityPanel />;

      case "user-management":
        return <UserManagementTab mode="demo" />;

      case "about":
        return <AboutTab />;

      default:
        return <EndpointsTab serviceEndpoints={SERVICE_ENDPOINTS} />;
    }
  };

  return (
    <DashboardLayout title="Settings" subtitle="Configure your intelligence platform">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Settings Overview */}
        <SettingsOverview metrics={overviewMetrics} />

        {/* Tab Navigation */}
        <SettingsTabNavigation activeTab={activeTab} onTabSelect={handleTabSelect} />

        {/* Tab Content */}
        <div className="space-y-6">{renderTabContent()}</div>
      </div>
    </DashboardLayout>
  );
}
