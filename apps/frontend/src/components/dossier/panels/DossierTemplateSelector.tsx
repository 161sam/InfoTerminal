// Dossier template selector panel
import { useState } from "react";
import { FileText, Settings, CheckCircle } from "lucide-react";
import { DossierTemplate, DOSSIER_TEMPLATES } from "@/lib/dossier/dossier-config";

interface DossierTemplateSelectorProps {
  selectedTemplate: string;
  onTemplateSelect: (templateId: string) => void;
  onCustomCreate: () => void;
}

export function DossierTemplateSelector({
  selectedTemplate,
  onTemplateSelect,
  onCustomCreate,
}: DossierTemplateSelectorProps) {
  const [hoveredTemplate, setHoveredTemplate] = useState<string | null>(null);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Choose Template</h3>
        <button
          onClick={onCustomCreate}
          className="text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
        >
          Start from scratch
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {DOSSIER_TEMPLATES.map((template) => (
          <TemplateCard
            key={template.id}
            template={template}
            isSelected={selectedTemplate === template.id}
            isHovered={hoveredTemplate === template.id}
            onSelect={() => onTemplateSelect(template.id)}
            onHover={() => setHoveredTemplate(template.id)}
            onLeave={() => setHoveredTemplate(null)}
          />
        ))}
      </div>

      {selectedTemplate && (
        <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-900/30 rounded-lg">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle size={16} className="text-blue-600 dark:text-blue-400" />
            <span className="font-medium text-blue-900 dark:text-blue-100">Template Selected</span>
          </div>
          <p className="text-sm text-blue-700 dark:text-blue-300">
            {DOSSIER_TEMPLATES.find((t) => t.id === selectedTemplate)?.description}
          </p>
        </div>
      )}
    </div>
  );
}

interface TemplateCardProps {
  template: DossierTemplate;
  isSelected: boolean;
  isHovered: boolean;
  onSelect: () => void;
  onHover: () => void;
  onLeave: () => void;
}

function TemplateCard({
  template,
  isSelected,
  isHovered,
  onSelect,
  onHover,
  onLeave,
}: TemplateCardProps) {
  const getTemplateIcon = (templateId: string) => {
    switch (templateId) {
      case "investigation":
        return <FileText size={24} className="text-blue-600 dark:text-blue-400" />;
      case "entity-profile":
        return <Settings size={24} className="text-green-600 dark:text-green-400" />;
      case "network-analysis":
        return <Settings size={24} className="text-purple-600 dark:text-purple-400" />;
      case "financial-audit":
        return <Settings size={24} className="text-orange-600 dark:text-orange-400" />;
      default:
        return <FileText size={24} className="text-gray-600 dark:text-gray-400" />;
    }
  };

  const getSettingsSummary = (template: DossierTemplate) => {
    const features = [];
    if (template.settings.includeSummary) features.push("Summary");
    if (template.settings.includeTimeline) features.push("Timeline");
    if (template.settings.includeVisualization) features.push("Visualization");
    return features.join(", ") || "Basic report";
  };

  return (
    <button
      onClick={onSelect}
      onMouseEnter={onHover}
      onMouseLeave={onLeave}
      className={`w-full text-left p-4 border rounded-lg transition-all duration-200 ${
        isSelected
          ? "border-primary-500 bg-primary-50 dark:bg-primary-900/20 dark:border-primary-400"
          : isHovered
            ? "border-gray-300 bg-gray-50 dark:border-gray-600 dark:bg-gray-700"
            : "border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800"
      }`}
    >
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 mt-1">{getTemplateIcon(template.id)}</div>

        <div className="flex-1 min-w-0">
          <h4 className="font-medium text-gray-900 dark:text-white mb-1">{template.name}</h4>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">{template.description}</p>

          <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
            <span>Features:</span>
            <span className="font-medium">{getSettingsSummary(template)}</span>
          </div>

          <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mt-1">
            <span>Confidence:</span>
            <span className="font-medium">
              {Math.round(template.settings.confidenceThreshold * 100)}%
            </span>
            <span>•</span>
            <span>Language:</span>
            <span className="font-medium uppercase">{template.settings.language}</span>
          </div>
        </div>

        {isSelected && (
          <div className="flex-shrink-0">
            <CheckCircle size={20} className="text-primary-600 dark:text-primary-400" />
          </div>
        )}
      </div>
    </button>
  );
}

export default DossierTemplateSelector;
