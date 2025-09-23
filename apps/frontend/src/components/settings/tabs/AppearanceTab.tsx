import React from 'react';
import Panel from '@/components/layout/Panel';
import { toast } from '@/components/ui/toast';
import SettingsGraphDeepLink from '@/components/settings/SettingsGraphDeepLink';
import { useTheme } from '@/lib/theme-provider';

interface Theme {
  id: string;
  name: string;
  description: string;
}

const THEMES: Theme[] = [
  { id: 'light', name: 'Light Mode', description: 'Clean light interface' },
  { id: 'dark', name: 'Dark Mode', description: 'Easy on the eyes' },
  { id: 'system', name: 'System Default', description: 'Follow system preference' }
];

export const AppearanceTab: React.FC = () => {
  const { theme, setTheme } = useTheme();

  const handleThemeChange = (newTheme: string) => {
    setTheme(newTheme as 'light' | 'dark' | 'system');
    toast(`Theme changed to ${newTheme}`, { variant: 'success' });
  };

  return (
    <div className="space-y-6">
      <Panel>
        <div className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-2">Theme Preferences</h3>
            <p className="text-sm text-gray-600 dark:text-slate-400">Customize the look and feel of your dashboard</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {THEMES.map((themeOption) => (
              <button
                key={themeOption.id}
                onClick={() => handleThemeChange(themeOption.id)}
                className={`p-4 text-left rounded-lg border-2 transition-colors ${
                  theme === themeOption.id
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                    : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                }`}
              >
                <div className="font-medium text-gray-900 dark:text-slate-100">{themeOption.name}</div>
                <div className="text-sm text-gray-600 dark:text-slate-400 mt-1">{themeOption.description}</div>
              </button>
            ))}
          </div>
          
          {/* Current Theme Status */}
          <div className="mt-4 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <div className="text-sm">
              <span className="text-gray-600 dark:text-gray-400">Current theme: </span>
              <span className="font-medium text-gray-900 dark:text-slate-100">
                {THEMES.find(t => t.id === theme)?.name || 'Unknown'}
              </span>
            </div>
          </div>
        </div>
      </Panel>
      
      <Panel>
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100">Graph Visualization</h3>
          <SettingsGraphDeepLink />
        </div>
      </Panel>
    </div>
  );
};

export default AppearanceTab;
