// Enhanced dossier builder modal for analytics export
import React, { useState, useEffect, useMemo } from "react";
import { FileText, Download, X, CheckCircle2, Calendar, Filter, Eye, Copy } from "lucide-react";
import {
  AnalyticsFilters,
  AnalyticsDossierSection,
  AnalyticsDossierExport,
} from "../analytics/types";
import { DossierTemplate, DOSSIER_TEMPLATES } from "@/lib/dossier/dossier-config";
import { DossierTemplateSelector } from "@/components/dossier/panels/DossierTemplateSelector";

interface DossierBuilderModalProps {
  isOpen: boolean;
  onClose: () => void;
  filters: AnalyticsFilters;
  availableSections: AnalyticsDossierSection[];
  onExport: (dossier: AnalyticsDossierExport) => void;
  className?: string;
  templates?: DossierTemplate[];
  templatesLoading?: boolean;
}

export function DossierBuilderModal({
  isOpen,
  onClose,
  filters,
  availableSections,
  onExport,
  className = "",
  templates,
  templatesLoading = false,
}: DossierBuilderModalProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [selectedSections, setSelectedSections] = useState<string[]>([]);
  const [exportFormat, setExportFormat] = useState<"markdown" | "pdf" | "html">("pdf");
  const [includeMetadata, setIncludeMetadata] = useState(true);
  const [step, setStep] = useState<"configure" | "preview" | "generating">("configure");
  const [generatedDossier, setGeneratedDossier] = useState<AnalyticsDossierExport | null>(null);
  const [selectedTemplateId, setSelectedTemplateId] = useState<string>("standard");

  const templateCatalog = useMemo(
    () => (templates && templates.length > 0 ? templates : DOSSIER_TEMPLATES),
    [templates],
  );

  useEffect(() => {
    if (isOpen) {
      const defaultTemplate = templateCatalog[0]?.id ?? "custom";
      setSelectedTemplateId(defaultTemplate);
    }
  }, [isOpen, templateCatalog]);

  useEffect(() => {
    if (isOpen) {
      // Reset form when modal opens
      setTitle(`Analytics Report - ${new Date().toLocaleDateString()}`);
      setDescription(
        "Comprehensive OSINT analytics report based on selected filters and data sources.",
      );
      setSelectedSections(availableSections.filter((s) => s.enabled).map((s) => s.id));
      setStep("configure");
      setGeneratedDossier(null);
    }
  }, [isOpen, availableSections]);

  const handleSectionToggle = (sectionId: string) => {
    setSelectedSections((prev) =>
      prev.includes(sectionId) ? prev.filter((id) => id !== sectionId) : [...prev, sectionId],
    );
  };

  const handlePreview = () => {
    if (!title.trim() || selectedSections.length === 0) {
      return;
    }

    const template = templateCatalog.find((t) => t.id === selectedTemplateId);
    const caseId = `analytics-${Date.now()}`;
    const dossier: AnalyticsDossierExport = {
      title: title.trim(),
      description: description.trim(),
      templateId: template?.id,
      format: exportFormat,
      includeMetadata,
      filters: { ...filters },
      sections: availableSections.filter((s) => selectedSections.includes(s.id)),
      metadata: {
        generatedAt: new Date().toISOString(),
        generatedBy: "Analytics Dashboard",
        version: "1.0",
        caseId,
        templateId: template?.id,
        format: exportFormat,
      },
    };

    setGeneratedDossier(dossier);
    setStep("preview");
  };

  const handleExport = () => {
    if (!generatedDossier) return;

    setStep("generating");
    onExport(generatedDossier);
  };

  const handleCopyFilters = () => {
    const filterText = JSON.stringify(filters, null, 2);
    navigator.clipboard.writeText(filterText);
  };

  const getFormatDescription = (format: string) => {
    switch (format) {
      case "pdf":
        return "Print-ready PDF with charts and tables";
      case "markdown":
        return "Structured Markdown for documentation";
      case "html":
        return "Interactive HTML with embedded visualizations";
      default:
        return "";
    }
  };

  const getSectionIcon = (sectionId: string) => {
    const icons: Record<string, React.ComponentType<any>> = {
      "entity-analytics": () => <div className="w-4 h-4 bg-blue-500 rounded" />,
      "source-coverage": () => <div className="w-4 h-4 bg-green-500 rounded" />,
      "evidence-quality": () => <div className="w-4 h-4 bg-purple-500 rounded" />,
      "workflow-runs": () => <div className="w-4 h-4 bg-orange-500 rounded" />,
      "activity-timeline": () => <div className="w-4 h-4 bg-red-500 rounded" />,
      geospatial: () => <div className="w-4 h-4 bg-yellow-500 rounded" />,
      "query-insights": () => <div className="w-4 h-4 bg-indigo-500 rounded" />,
    };
    const IconComponent = icons[sectionId];
    return IconComponent ? <IconComponent /> : <FileText size={16} />;
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div
        className={`bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden ${className}`}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <FileText size={24} className="text-blue-600" />
            <div>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                Export Analytics Dossier
              </h2>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Create a comprehensive report with selected analytics sections
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <X size={20} />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto">
          {step === "configure" && (
            <div className="p-6 space-y-6">
              {/* Basic Information */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">
                  Report Information
                </h3>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Title
                  </label>
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter report title..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Description
                  </label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter report description..."
                  />
                </div>
              </div>

              {/* Template Selection */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">Template</h3>
                <DossierTemplateSelector
                  selectedTemplate={selectedTemplateId}
                  onTemplateSelect={setSelectedTemplateId}
                  onCustomCreate={() => setSelectedTemplateId("custom")}
                  templates={templateCatalog}
                  isLoading={templatesLoading}
                />
              </div>

              {/* Filter Summary */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">
                    Applied Filters
                  </h3>
                  <button
                    onClick={handleCopyFilters}
                    className="inline-flex items-center gap-1 px-3 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded transition-colors"
                  >
                    <Copy size={12} />
                    Copy
                  </button>
                </div>

                <div className="bg-gray-50 dark:bg-gray-900/50 rounded-lg p-4">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="font-medium text-gray-700 dark:text-gray-300">
                        Time Range:
                      </span>
                      <span className="ml-2 text-gray-600 dark:text-gray-400">
                        {filters.timeRange}
                      </span>
                    </div>

                    {filters.entityTypes.length > 0 && (
                      <div>
                        <span className="font-medium text-gray-700 dark:text-gray-300">
                          Entity Types:
                        </span>
                        <span className="ml-2 text-gray-600 dark:text-gray-400">
                          {filters.entityTypes.slice(0, 2).join(", ")}
                          {filters.entityTypes.length > 2 &&
                            ` +${filters.entityTypes.length - 2} more`}
                        </span>
                      </div>
                    )}

                    {filters.sources.length > 0 && (
                      <div>
                        <span className="font-medium text-gray-700 dark:text-gray-300">
                          Sources:
                        </span>
                        <span className="ml-2 text-gray-600 dark:text-gray-400">
                          {filters.sources.slice(0, 2).join(", ")}
                          {filters.sources.length > 2 && ` +${filters.sources.length - 2} more`}
                        </span>
                      </div>
                    )}

                    {filters.tags.length > 0 && (
                      <div>
                        <span className="font-medium text-gray-700 dark:text-gray-300">Tags:</span>
                        <span className="ml-2 text-gray-600 dark:text-gray-400">
                          {filters.tags.slice(0, 2).join(", ")}
                          {filters.tags.length > 2 && ` +${filters.tags.length - 2} more`}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Section Selection */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">
                  Include Sections
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {availableSections.map((section) => (
                    <div
                      key={section.id}
                      className={`border rounded-lg p-3 cursor-pointer transition-colors ${
                        selectedSections.includes(section.id)
                          ? "border-blue-500 bg-blue-50 dark:bg-blue-900/20"
                          : "border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600"
                      }`}
                      onClick={() => handleSectionToggle(section.id)}
                    >
                      <div className="flex items-start gap-3">
                        <div className="mt-1">
                          {selectedSections.includes(section.id) ? (
                            <CheckCircle2 size={20} className="text-blue-600" />
                          ) : (
                            <div className="w-5 h-5 border border-gray-300 dark:border-gray-600 rounded" />
                          )}
                        </div>

                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            {getSectionIcon(section.id)}
                            <span className="font-medium text-gray-900 dark:text-gray-100">
                              {section.name}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            {section.description}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Export Format */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">
                  Export Format
                </h3>

                <div className="space-y-3">
                  {(["pdf", "markdown", "html"] as const).map((format) => (
                    <div
                      key={format}
                      className={`border rounded-lg p-3 cursor-pointer transition-colors ${
                        exportFormat === format
                          ? "border-blue-500 bg-blue-50 dark:bg-blue-900/20"
                          : "border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600"
                      }`}
                      onClick={() => setExportFormat(format)}
                    >
                      <div className="flex items-center gap-3">
                        <div
                          className={`w-4 h-4 rounded-full border-2 ${
                            exportFormat === format
                              ? "border-blue-500 bg-blue-500"
                              : "border-gray-300 dark:border-gray-600"
                          }`}
                        >
                          {exportFormat === format && (
                            <div className="w-full h-full rounded-full bg-white scale-50" />
                          )}
                        </div>

                        <div>
                          <div className="font-medium text-gray-900 dark:text-gray-100 uppercase">
                            {format}
                          </div>
                          <div className="text-sm text-gray-600 dark:text-gray-400">
                            {getFormatDescription(format)}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id="includeMetadata"
                    checked={includeMetadata}
                    onChange={(e) => setIncludeMetadata(e.target.checked)}
                    className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                  />
                  <label
                    htmlFor="includeMetadata"
                    className="text-sm text-gray-700 dark:text-gray-300"
                  >
                    Include metadata and generation details
                  </label>
                </div>
              </div>
            </div>
          )}

          {step === "preview" && generatedDossier && (
            <div className="p-6 space-y-6">
              <div className="flex items-center gap-2 mb-4">
                <Eye size={20} className="text-blue-600" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">
                  Preview Dossier
                </h3>
              </div>

              <div className="bg-gray-50 dark:bg-gray-900/50 rounded-lg p-6 space-y-4">
                <h4 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                  {generatedDossier.title}
                </h4>

                {generatedDossier.description && (
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    {generatedDossier.description}
                  </p>
                )}

                <div className="grid grid-cols-2 gap-4 text-sm mb-6">
                  <div>
                    <span className="font-medium text-gray-700 dark:text-gray-300">Generated:</span>
                    <span className="ml-2 text-gray-600 dark:text-gray-400">
                      {new Date(generatedDossier.metadata.generatedAt).toLocaleString()}
                    </span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700 dark:text-gray-300">Format:</span>
                    <span className="ml-2 text-gray-600 dark:text-gray-400 uppercase">
                      {generatedDossier.format}
                    </span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700 dark:text-gray-300">Sections:</span>
                    <span className="ml-2 text-gray-600 dark:text-gray-400">
                      {generatedDossier.sections.length}
                    </span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700 dark:text-gray-300">
                      Time Range:
                    </span>
                    <span className="ml-2 text-gray-600 dark:text-gray-400">
                      {generatedDossier.filters.timeRange}
                    </span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700 dark:text-gray-300">Template:</span>
                    <span className="ml-2 text-gray-600 dark:text-gray-400">
                      {templateCatalog.find((t) => t.id === generatedDossier.templateId)?.name ||
                        "Custom"}
                    </span>
                  </div>
                </div>

                <div className="space-y-3">
                  <h5 className="font-medium text-gray-900 dark:text-gray-100">
                    Included Sections:
                  </h5>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {generatedDossier.sections.map((section) => (
                      <div key={section.id} className="flex items-center gap-2 text-sm">
                        {getSectionIcon(section.id)}
                        <span className="text-gray-700 dark:text-gray-300">{section.name}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {step === "generating" && (
            <div className="p-6 flex flex-col items-center justify-center min-h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
                Generating Dossier
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 text-center">
                Compiling analytics data and creating your report...
              </p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-6 border-t border-gray-200 dark:border-gray-700">
          <div className="text-sm text-gray-600 dark:text-gray-400">
            {step === "configure" && selectedSections.length > 0 && (
              <span>{selectedSections.length} sections selected</span>
            )}
          </div>

          <div className="flex items-center gap-3">
            {step === "configure" && (
              <>
                <button
                  onClick={onClose}
                  className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handlePreview}
                  disabled={!title.trim() || selectedSections.length === 0}
                  className="inline-flex items-center gap-2 px-4 py-2 text-sm text-white bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed rounded-lg transition-colors"
                >
                  <Eye size={16} />
                  Preview
                </button>
              </>
            )}

            {step === "preview" && (
              <>
                <button
                  onClick={() => setStep("configure")}
                  className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
                >
                  Back
                </button>
                <button
                  onClick={handleExport}
                  className="inline-flex items-center gap-2 px-4 py-2 text-sm text-white bg-green-600 hover:bg-green-700 rounded-lg transition-colors"
                >
                  <Download size={16} />
                  Export Dossier
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default DossierBuilderModal;
