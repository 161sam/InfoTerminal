import React, { useState } from "react";
import Panel from "@/components/layout/Panel";

interface NotificationSettings {
  desktop: boolean;
  email: boolean;
  searchResults: boolean;
  systemAlerts: boolean;
  graphUpdates: boolean;
}

const NOTIFICATION_SETTINGS = [
  {
    key: "desktop",
    label: "Desktop Notifications",
    description: "Show browser notifications for important events",
  },
  {
    key: "email",
    label: "Email Notifications",
    description: "Receive email alerts for critical updates",
  },
  {
    key: "searchResults",
    label: "Search Results",
    description: "Notify when new search results are available",
  },
  {
    key: "systemAlerts",
    label: "System Alerts",
    description: "Alerts for service issues and maintenance",
  },
  {
    key: "graphUpdates",
    label: "Graph Updates",
    description: "Notifications for significant graph changes",
  },
];

export const NotificationsTab: React.FC = () => {
  const [notifications, setNotifications] = useState<NotificationSettings>({
    desktop: true,
    email: false,
    searchResults: true,
    systemAlerts: true,
    graphUpdates: false,
  });

  return (
    <Panel>
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-2">
            Notification Preferences
          </h3>
          <p className="text-sm text-gray-600 dark:text-slate-400">
            Control when and how you receive notifications
          </p>
        </div>

        <div className="space-y-4">
          {NOTIFICATION_SETTINGS.map((setting) => (
            <div
              key={setting.key}
              className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg"
            >
              <div>
                <h4 className="font-medium text-gray-900 dark:text-slate-100">{setting.label}</h4>
                <p className="text-sm text-gray-600 dark:text-slate-400">{setting.description}</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={notifications[setting.key as keyof NotificationSettings]}
                  onChange={(e) =>
                    setNotifications((prev) => ({
                      ...prev,
                      [setting.key]: e.target.checked,
                    }))
                  }
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
              </label>
            </div>
          ))}
        </div>
      </div>
    </Panel>
  );
};

export default NotificationsTab;
