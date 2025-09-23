import React from "react";
import {
  Settings, 
  Server, 
  Info, 
  Monitor, 
  Shield,
  Palette,
  Bell,
  User,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';

export type SettingsTab =
  | 'endpoints'
  | 'ops'
  | 'gateway'
  | 'appearance'
  | 'notifications'
  | 'security'
  | 'user-management'
  | 'about';

interface TabConfig {
  id: SettingsTab;
  label: string;
  icon: LucideIcon;
}

const SETTINGS_TAB_CONFIG: TabConfig[] = [
  { id: 'endpoints', label: 'API Endpoints', icon: Server },
  { id: 'ops', label: 'Operations', icon: Monitor },
  { id: 'gateway', label: 'Gateway', icon: Settings },
  { id: 'appearance', label: 'Appearance', icon: Palette },
  { id: 'notifications', label: 'Notifications', icon: Bell },
  { id: 'security', label: 'Security', icon: Shield },
  { id: 'user-management', label: 'User Management', icon: User },
  { id: 'about', label: 'About', icon: Info },
];

interface SettingsTabNavigationProps {
  activeTab: SettingsTab;
  onTabSelect: (tab: SettingsTab) => void;
}

interface TabButtonProps {
  config: TabConfig;
  isActive: boolean;
  onClick: () => void;
}

const TabButton = ({ config, isActive, onClick }: TabButtonProps) => (
  <button
    onClick={onClick}
    className={`inline-flex items-center gap-2 px-4 py-3 text-sm rounded-lg transition-colors ${
      isActive
        ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
        : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200 hover:bg-gray-100 dark:hover:bg-gray-800'
    }`}
  >
    <config.icon size={16} />
    {config.label}
  </button>
);

export default function SettingsTabNavigation({ activeTab, onTabSelect }: SettingsTabNavigationProps) {
  return (
    <div className="flex flex-wrap gap-2 bg-gray-50 dark:bg-gray-800 p-2 rounded-lg">
      {SETTINGS_TAB_CONFIG.map((config) => (
        <TabButton
          key={config.id}
          config={config}
          isActive={activeTab === config.id}
          onClick={() => onTabSelect(config.id)}
        />
      ))}
    </div>
  );
}

export { SETTINGS_TAB_CONFIG };
export type { TabConfig };
