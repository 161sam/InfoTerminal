// Dossier settings configuration panel
import { Calendar, Settings, Globe, BarChart3 } from "lucide-react";
import {
  DossierSettings,
  LANGUAGE_OPTIONS,
  CONFIDENCE_LEVELS,
  estimateDossierSize,
  DossierItem,
} from "@/lib/dossier/dossier-config";

interface DossierSettingsPanelProps {
  settings: DossierSettings;
  items: DossierItem[];
  onSettingsChange: (settings: DossierSettings) => void;
}

export function DossierSettingsPanel({
  settings,
  items,
  onSettingsChange,
}: DossierSettingsPanelProps) {
  const updateSetting = <K extends keyof DossierSettings>(key: K, value: DossierSettings[K]) => {
    onSettingsChange({
      ...settings,
      [key]: value,
    });
  };

  const estimatedSize = estimateDossierSize(items, settings);

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2">
        <Settings size={20} className="text-gray-600 dark:text-gray-400" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Dossier Settings</h3>
      </div>

      {/* Content Options */}
      <div className="space-y-4">
        <h4 className="font-medium text-gray-900 dark:text-white">Content Options</h4>

        <div className="space-y-3">
          <label className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={settings.includeSummary}
              onChange={(e) => updateSetting("includeSummary", e.target.checked)}
              className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700"
            />
            <div>
              <span className="font-medium text-gray-900 dark:text-white">
                Include Executive Summary
              </span>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Generate a comprehensive summary of findings
              </p>
            </div>
          </label>

          <label className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={settings.includeTimeline}
              onChange={(e) => updateSetting("includeTimeline", e.target.checked)}
              className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700"
            />
            <div>
              <span className="font-medium text-gray-900 dark:text-white">Include Timeline</span>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Create chronological timeline of events
              </p>
            </div>
          </label>

          <label className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={settings.includeVisualization}
              onChange={(e) => updateSetting("includeVisualization", e.target.checked)}
              className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700"
            />
            <div>
              <span className="font-medium text-gray-900 dark:text-white">
                Include Network Visualization
              </span>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Generate entity relationship diagrams
              </p>
            </div>
          </label>
        </div>
      </div>

      {/* Quality Settings */}
      <div className="space-y-4">
        <h4 className="font-medium text-gray-900 dark:text-white">Quality Settings</h4>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Minimum Confidence Threshold
          </label>
          <div className="space-y-2">
            {CONFIDENCE_LEVELS.map((level) => (
              <label key={level.value} className="flex items-center gap-2">
                <input
                  type="radio"
                  name="confidence"
                  value={level.value}
                  checked={settings.confidenceThreshold === level.value}
                  onChange={(e) => updateSetting("confidenceThreshold", parseFloat(e.target.value))}
                  className="w-4 h-4 text-primary-600 border-gray-300 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700"
                />
                <span className={`text-sm ${level.color} dark:text-gray-300`}>{level.label}</span>
              </label>
            ))}
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
            Only include entities and relationships above this confidence level
          </p>
        </div>
      </div>

      {/* Language Settings */}
      <div className="space-y-4">
        <h4 className="font-medium text-gray-900 dark:text-white flex items-center gap-2">
          <Globe size={16} />
          Language Settings
        </h4>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Report Language
          </label>
          <select
            value={settings.language}
            onChange={(e) => updateSetting("language", e.target.value as "en" | "de")}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
          >
            {LANGUAGE_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Date Range */}
      <div className="space-y-4">
        <h4 className="font-medium text-gray-900 dark:text-white flex items-center gap-2">
          <Calendar size={16} />
          Date Range (Optional)
        </h4>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              From
            </label>
            <input
              type="date"
              value={settings.dateRange?.from || ""}
              onChange={(e) =>
                updateSetting("dateRange", {
                  from: e.target.value,
                  to: settings.dateRange?.to ?? "",
                })
              }
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              To
            </label>
            <input
              type="date"
              value={settings.dateRange?.to || ""}
              onChange={(e) =>
                updateSetting("dateRange", {
                  from: settings.dateRange?.from ?? "",
                  to: e.target.value,
                })
              }
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
            />
          </div>
        </div>

        {settings.dateRange?.from || settings.dateRange?.to ? (
          <button
            onClick={() => updateSetting("dateRange", undefined)}
            className="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
          >
            Clear date range
          </button>
        ) : null}
      </div>

      {/* Generation Preview */}
      <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
        <h4 className="font-medium text-gray-900 dark:text-white mb-3 flex items-center gap-2">
          <BarChart3 size={16} />
          Generation Preview
        </h4>

        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Items to include:</span>
            <span className="font-medium text-gray-900 dark:text-white">{items.length}</span>
          </div>

          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Sections:</span>
            <span className="font-medium text-gray-900 dark:text-white">
              {
                [
                  "Content",
                  settings.includeSummary && "Summary",
                  settings.includeTimeline && "Timeline",
                  settings.includeVisualization && "Network Diagram",
                ].filter(Boolean).length
              }
            </span>
          </div>

          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Estimated size:</span>
            <span className="font-medium text-gray-900 dark:text-white">{estimatedSize}</span>
          </div>

          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Language:</span>
            <span className="font-medium text-gray-900 dark:text-white">
              {LANGUAGE_OPTIONS.find((l) => l.value === settings.language)?.label}
            </span>
          </div>

          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Min. confidence:</span>
            <span className="font-medium text-gray-900 dark:text-white">
              {Math.round(settings.confidenceThreshold * 100)}%
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DossierSettingsPanel;
