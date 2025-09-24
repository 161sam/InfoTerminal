// Dossier template selector panel
import { useMemo, useState } from "react";
import { FileText, CheckCircle, Sparkles } from "lucide-react";
import { DossierTemplate, DOSSIER_TEMPLATES } from "@/lib/dossier/dossier-config";

interface DossierTemplateSelectorProps {
  selectedTemplate: string;
  onTemplateSelect: (templateId: string) => void;
  onCustomCreate: () => void;
  templates?: DossierTemplate[];
  isLoading?: boolean;
}

export function DossierTemplateSelector({
  selectedTemplate,
  onTemplateSelect,
  onCustomCreate,
  templates,
  isLoading = false,
}: DossierTemplateSelectorProps) {
  const [hoveredTemplate, setHoveredTemplate] = useState<string | null>(null);
  const templateList = useMemo(
    () => (templates && templates.length > 0 ? templates : DOSSIER_TEMPLATES),
    [templates],
  );
  const selected = templateList.find((t) => t.id === selectedTemplate);

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

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[0, 1].map((key) => (
            <div
              key={key}
              className="h-40 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-100/70 dark:bg-gray-800/40 animate-pulse"
            ></div>
          ))}
        </div>
      ) : templateList.length === 0 ? (
        <div className="rounded-lg border border-dashed border-gray-300 dark:border-gray-700 p-6 text-sm text-gray-500 dark:text-gray-400">
          No dossier templates available.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {templateList.map((template) => (
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
      )}

      {selected && (
        <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-900/30 rounded-lg">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle size={16} className="text-blue-600 dark:text-blue-400" />
            <span className="font-medium text-blue-900 dark:text-blue-100">Template Selected</span>
          </div>
          <p className="text-sm text-blue-700 dark:text-blue-300">{selected.description}</p>
          <div className="mt-3 text-xs text-blue-700 dark:text-blue-200 space-y-1">
            {selected.recommendedFor && <div>Empfohlen für: {selected.recommendedFor}</div>}
            {selected.estimatedDuration && (
              <div>Bearbeitungszeit: {selected.estimatedDuration}</div>
            )}
            {selected.formats && selected.formats.length > 0 && (
              <div>Formate: {selected.formats.join(", ")}</div>
            )}
          </div>
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
      case "standard":
        return <FileText size={24} className="text-blue-600 dark:text-blue-400" />;
      case "brief":
        return <Sparkles size={24} className="text-indigo-500 dark:text-indigo-300" />;
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

          {template.tags && template.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-2">
              {template.tags.slice(0, 3).map((tag) => (
                <span
                  key={tag}
                  className="inline-flex items-center rounded-full bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300 px-2 py-0.5 text-xs"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}

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

          {template.sections && template.sections.length > 0 && (
            <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
              Sections: {template.sections.slice(0, 3).join(", ")}
              {template.sections.length > 3 && " …"}
            </div>
          )}
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
