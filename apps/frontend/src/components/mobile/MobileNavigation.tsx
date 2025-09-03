// apps/frontend/src/components/mobile/MobileNavigation.tsx
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { 
  Home,
  Search,
  Network,
  FileText,
  BarChart3,
  Settings,
  Menu,
  X,
  Bell,
  User
} from 'lucide-react';
import { useNotifications } from '../../lib/notifications';

interface MobileNavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ size?: number; className?: string }>;
  badge?: number;
}

const navigationItems: MobileNavItem[] = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Search', href: '/search', icon: Search },
  { name: 'Graph', href: '/graphx', icon: Network },
  { name: 'Documents', href: '/documents', icon: FileText },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
];

export function MobileNavigation() {
  const router = useRouter();
  const { notifications } = useNotifications();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Close menu when route changes
  useEffect(() => {
    setIsMenuOpen(false);
  }, [router.pathname]);

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (isMenuOpen && !(event.target as Element).closest('.mobile-menu')) {
        setIsMenuOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isMenuOpen]);

  const unreadNotifications = notifications.filter(n => !n.persistent).length;

  return (
    <>
      {/* Mobile Header */}
      <header className="lg:hidden fixed top-0 left-0 right-0 z-40 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm">
        <div className="flex items-center justify-between px-4 py-3">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              {isMenuOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
            <h1 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              InfoTerminal
            </h1>
          </div>

          <div className="flex items-center gap-2">
            <button className="relative p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
              <Bell size={20} />
              {unreadNotifications > 0 && (
                <span className="absolute -top-1 -right-1 h-5 w-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                  {unreadNotifications > 9 ? '9+' : unreadNotifications}
                </span>
              )}
            </button>
            <div className="h-8 w-8 bg-primary-500 rounded-full flex items-center justify-center">
              <User size={16} className="text-white" />
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Menu Overlay */}
      {isMenuOpen && (
        <div className="lg:hidden fixed inset-0 z-50 bg-black bg-opacity-50">
          <div className="mobile-menu fixed top-0 left-0 h-full w-80 bg-white dark:bg-gray-800 shadow-xl transform transition-transform">
            
            {/* Menu Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Menu</h2>
              <button
                onClick={() => setIsMenuOpen(false)}
                className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 rounded-lg"
              >
                <X size={20} />
              </button>
            </div>

            {/* Navigation Items */}
            <nav className="p-4 space-y-2">
              {navigationItems.map((item) => {
                const isActive = router.pathname === item.href ||
                  (item.href !== '/' && router.pathname.startsWith(item.href));

                return (
                  <button
                    key={item.name}
                    onClick={() => router.push(item.href)}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors text-left ${
                      isActive
                        ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                    }`}
                  >
                    <item.icon size={20} />
                    <span className="font-medium">{item.name}</span>
                    {item.badge && (
                      <span className="ml-auto bg-red-100 text-red-800 text-xs font-medium px-2 py-0.5 rounded-full">
                        {item.badge}
                      </span>
                    )}
                  </button>
                );
              })}
            </nav>

            {/* Settings */}
            <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200 dark:border-gray-700">
              <button
                onClick={() => router.push('/settings')}
                className="w-full flex items-center gap-3 px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              >
                <Settings size={20} />
                <span className="font-medium">Settings</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Bottom Tab Navigation (Alternative) */}
      <nav className="lg:hidden fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 shadow-lg">
        <div className="flex items-center justify-around py-2">
          {navigationItems.slice(0, 4).map((item) => {
            const isActive = router.pathname === item.href ||
              (item.href !== '/' && router.pathname.startsWith(item.href));

            return (
              <button
                key={item.name}
                onClick={() => router.push(item.href)}
                className={`flex flex-col items-center gap-1 p-2 min-w-0 flex-1 transition-colors ${
                  isActive
                    ? 'text-primary-600 dark:text-primary-400'
                    : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                }`}
              >
                <item.icon size={20} />
                <span className="text-xs font-medium truncate">{item.name}</span>
                {item.badge && (
                  <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                    {item.badge > 9 ? '9+' : item.badge}
                  </span>
                )}
              </button>
            );
          })}
          
          {/* More Button */}
          <button
            onClick={() => setIsMenuOpen(true)}
            className="flex flex-col items-center gap-1 p-2 min-w-0 flex-1 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
          >
            <Menu size={20} />
            <span className="text-xs font-medium">More</span>
          </button>
        </div>
      </nav>

      {/* Content Spacer for Mobile */}
      <div className="lg:hidden h-16" /> {/* Top spacer */}
      <div className="lg:hidden h-16" /> {/* Bottom spacer */}
    </>
  );
}

// Settings Panel Component
import { useTheme } from '../../lib/theme-provider';

interface SettingsSection {
  title: string;
  items: SettingItem[];
}

interface SettingItem {
  key: string;
  label: string;
  type: 'toggle' | 'select' | 'range' | 'input';
  value: any;
  options?: { label: string; value: any }[];
  min?: number;
  max?: number;
  step?: number;
  description?: string;
  onChange: (value: any) => void;
}

export function SettingsPanel({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const { theme, setTheme, resolvedTheme } = useTheme();
  const [settings, setSettings] = useState({
    notifications: true,
    autoRefresh: true,
    refreshInterval: 30,
    language: 'en',
    timezone: 'UTC',
    compactMode: false,
    animationsEnabled: true,
    soundEnabled: false,
  });

  const updateSetting = (key: string, value: any) => {
    setSettings(prev => ({ ...prev, [key]: value }));
    // Save to localStorage
    localStorage.setItem(`setting_${key}`, JSON.stringify(value));
  };

  // Load settings from localStorage
  useEffect(() => {
    const loadedSettings: any = {};
    Object.keys(settings).forEach(key => {
      const saved = localStorage.getItem(`setting_${key}`);
      if (saved) {
        try {
          loadedSettings[key] = JSON.parse(saved);
        } catch (e) {
          // Ignore invalid JSON
        }
      }
    });
    if (Object.keys(loadedSettings).length > 0) {
      setSettings(prev => ({ ...prev, ...loadedSettings }));
    }
  }, []);

  const settingsSections: SettingsSection[] = [
    {
      title: 'Appearance',
      items: [
        {
          key: 'theme',
          label: 'Theme',
          type: 'select',
          value: theme,
          options: [
            { label: 'Light', value: 'light' },
            { label: 'Dark', value: 'dark' },
            { label: 'System', value: 'system' },
          ],
          onChange: (value) => setTheme(value),
        },
        {
          key: 'compactMode',
          label: 'Compact Mode',
          type: 'toggle',
          value: settings.compactMode,
          description: 'Use more compact spacing and smaller elements',
          onChange: (value) => updateSetting('compactMode', value),
        },
        {
          key: 'animationsEnabled',
          label: 'Enable Animations',
          type: 'toggle',
          value: settings.animationsEnabled,
          description: 'Enable smooth transitions and animations',
          onChange: (value) => updateSetting('animationsEnabled', value),
        },
      ],
    },
    {
      title: 'Notifications',
      items: [
        {
          key: 'notifications',
          label: 'Push Notifications',
          type: 'toggle',
          value: settings.notifications,
          description: 'Receive push notifications for important updates',
          onChange: (value) => updateSetting('notifications', value),
        },
        {
          key: 'soundEnabled',
          label: 'Sound Notifications',
          type: 'toggle',
          value: settings.soundEnabled,
          description: 'Play sound for notifications',
          onChange: (value) => updateSetting('soundEnabled', value),
        },
      ],
    },
    {
      title: 'Data & Sync',
      items: [
        {
          key: 'autoRefresh',
          label: 'Auto Refresh',
          type: 'toggle',
          value: settings.autoRefresh,
          description: 'Automatically refresh data in the background',
          onChange: (value) => updateSetting('autoRefresh', value),
        },
        {
          key: 'refreshInterval',
          label: 'Refresh Interval (seconds)',
          type: 'range',
          value: settings.refreshInterval,
          min: 10,
          max: 300,
          step: 10,
          onChange: (value) => updateSetting('refreshInterval', value),
        },
      ],
    },
    {
      title: 'Localization',
      items: [
        {
          key: 'language',
          label: 'Language',
          type: 'select',
          value: settings.language,
          options: [
            { label: 'English', value: 'en' },
            { label: 'Deutsch', value: 'de' },
            { label: 'Français', value: 'fr' },
            { label: 'Español', value: 'es' },
          ],
          onChange: (value) => updateSetting('language', value),
        },
        {
          key: 'timezone',
          label: 'Timezone',
          type: 'select',
          value: settings.timezone,
          options: [
            { label: 'UTC', value: 'UTC' },
            { label: 'America/New_York', value: 'America/New_York' },
            { label: 'Europe/London', value: 'Europe/London' },
            { label: 'Europe/Berlin', value: 'Europe/Berlin' },
            { label: 'Asia/Tokyo', value: 'Asia/Tokyo' },
          ],
          onChange: (value) => updateSetting('timezone', value),
        },
      ],
    },
  ];

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      <div className="absolute inset-0 bg-black bg-opacity-50" onClick={onClose} />
      
      <div className="absolute top-0 right-0 h-full w-full max-w-md bg-white dark:bg-gray-800 shadow-xl">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Settings</h2>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 rounded-lg transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Settings Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-8">
          {settingsSections.map((section) => (
            <div key={section.title}>
              <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-4">
                {section.title}
              </h3>
              
              <div className="space-y-4">
                {section.items.map((item) => (
                  <SettingItem key={item.key} item={item} />
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
            <span>InfoTerminal v0.1.0</span>
            <button
              onClick={() => {
                if (confirm('Reset all settings to default?')) {
                  Object.keys(settings).forEach(key => {
                    localStorage.removeItem(`setting_${key}`);
                  });
                  window.location.reload();
                }
              }}
              className="text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300"
            >
              Reset All
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function SettingItem({ item }: { item: SettingItem }) {
  const renderInput = () => {
    switch (item.type) {
      case 'toggle':
        return (
          <button
            onClick={() => item.onChange(!item.value)}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 ${
              item.value ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'
            }`}
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                item.value ? 'translate-x-6' : 'translate-x-1'
              }`}
            />
          </button>
        );
      
      case 'select':
        return (
          <select
            value={item.value}
            onChange={(e) => item.onChange(e.target.value)}
            className="px-3 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          >
            {item.options?.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        );
      
      case 'range':
        return (
          <div className="flex items-center gap-3">
            <input
              type="range"
              min={item.min}
              max={item.max}
              step={item.step}
              value={item.value}
              onChange={(e) => item.onChange(Number(e.target.value))}
              className="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
            />
            <span className="text-sm font-medium text-gray-900 dark:text-gray-100 min-w-[3rem] text-right">
              {item.value}
            </span>
          </div>
        );
      
      case 'input':
        return (
          <input
            type="text"
            value={item.value}
            onChange={(e) => item.onChange(e.target.value)}
            className="px-3 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 w-full"
          />
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="flex items-center justify-between">
      <div className="flex-1">
        <label className="text-sm font-medium text-gray-900 dark:text-gray-100">
          {item.label}
        </label>
        {item.description && (
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
            {item.description}
          </p>
        )}
      </div>
      <div className="ml-4">
        {renderInput()}
      </div>
    </div>
  );
}