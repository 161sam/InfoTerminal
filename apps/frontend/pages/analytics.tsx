// OSINT Analytics Dashboard - Enhanced with modular components and dossier export
import React, { useState, useCallback, useEffect } from "react";
import { Download, Filter } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import {
  FiltersBar,
  EntityAnalytics,
  SourceCoverage,
  EvidenceQuality,
  WorkflowRunsTable,
  ActivityTimeline,
  GeoMap,
  QueryInsights,
  GraphAnalytics,
  AnalyticsFilters,
  TIME_RANGES,
  AnalyticsDossierSection,
  AnalyticsDossierExport,
} from "@/components/analytics";
import { DossierBuilderModal } from "@/components/dossier/DossierBuilderModal";
import { ProgressModal } from "@/components/feedback/ProgressModal";
import { useTaskProgress } from "@/hooks/useTaskProgress";
import { useNotifications } from "@/lib/notifications";
import { DossierTemplate, DOSSIER_TEMPLATES } from "@/lib/dossier/dossier-config";
import {
  useEntityAnalytics,
  useSourceCoverage,
  useEvidenceQuality,
  useWorkflowRuns,
  useTimeline,
  useGeoEntities,
  useQueryInsights,
  useGraphMetrics,
} from "@/hooks/analytics";

export default function AnalyticsPage() {
  const [filters, setFilters] = useState<AnalyticsFilters>({
    timeRange: "30d",
    entityTypes: [],
    sources: [],
    tags: [],
    collections: [],
    workflows: [],
    confidence: 0.7,
  });

  const [showDossierModal, setShowDossierModal] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [templates, setTemplates] = useState<DossierTemplate[]>(DOSSIER_TEMPLATES);
  const [templatesLoading, setTemplatesLoading] = useState(false);
  const [templateError, setTemplateError] = useState<string | null>(null);
  const [dossierTaskId, setDossierTaskId] = useState<string | null>(null);
  const [showDossierProgress, setShowDossierProgress] = useState(false);
  const notifications = useNotifications();

  // Initialize hooks to track loading states
  const entityAnalytics = useEntityAnalytics(filters);
  const sourceCoverage = useSourceCoverage(filters);
  const evidenceQuality = useEvidenceQuality(filters);
  const workflowRuns = useWorkflowRuns(filters);
  const timeline = useTimeline(filters);
  const geoEntities = useGeoEntities(filters);
  const queryInsights = useQueryInsights(filters);
  const graphMetrics = useGraphMetrics(filters);

  const handleFiltersChange = useCallback((newFilters: Partial<AnalyticsFilters>) => {
    setFilters((prev) => ({ ...prev, ...newFilters }));
  }, []);

  const handleRefreshAll = useCallback(() => {
    setRefreshTrigger((prev) => prev + 1);

    // Trigger refresh on all hooks
    entityAnalytics.refresh?.();
    sourceCoverage.refresh?.();
    evidenceQuality.refresh?.();
    workflowRuns.refresh?.();
    timeline.refresh?.();
    geoEntities.refresh?.();
    queryInsights.refresh?.();
    graphMetrics.refresh?.();
  }, [
    entityAnalytics.refresh,
    sourceCoverage.refresh,
    evidenceQuality.refresh,
    workflowRuns.refresh,
    timeline.refresh,
    geoEntities.refresh,
    queryInsights.refresh,
    graphMetrics.refresh,
  ]);

  const handleOpenDossierExport = () => {
    setShowDossierModal(true);
  };

  const dossierProgress = useTaskProgress({
    active: showDossierProgress,
    taskId: dossierTaskId,
    eventType: "dossier_progress",
    fallbackDurationMs: 8000,
    matchEvent: (event, id) => {
      const caseId = (event.case_id ?? event.caseId) as string | undefined;
      return caseId === id;
    },
  });

  const handleDossierExport = async (dossier: AnalyticsDossierExport) => {
    const caseId = dossier.metadata.caseId ?? `analytics-${Date.now()}`;
    const payload = {
      case_id: caseId,
      title: dossier.title,
      summary: dossier.description,
      source: "graph",
      format: dossier.format === "pdf" ? "pdf" : "markdown",
      template: dossier.templateId ?? "standard",
      analysts: ["Analytics Dashboard"],
      notes: dossier.sections.map((section) => `${section.name}: ${section.description}`),
      entities: [],
      references: [],
    };

    setShowDossierModal(false);
    setDossierTaskId(caseId);
    setShowDossierProgress(true);
    dossierProgress.setManualProgress(8, "running", "Export wird vorbereitet");

    try {
      const response = await fetch("/api/collab/dossier/export", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        let errorDetail = "Export fehlgeschlagen";
        try {
          const body = await response.json();
          if (typeof body?.error === "string") {
            errorDetail = body.error;
          } else if (typeof body?.details === "string") {
            errorDetail = body.details;
          }
        } catch {
          // ignore parse errors
        }
        dossierProgress.setManualProgress(100, "failed", errorDetail);
        notifications.error("Dossier-Export fehlgeschlagen", errorDetail);
        return;
      }

      const contentType = response.headers.get("content-type") || "";

      if (contentType.includes("application/pdf")) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const disposition = response.headers.get("content-disposition") || "";
        const filenameMatch = disposition.match(/filename="?(.+?)"?$/);
        const filename = filenameMatch?.[1] || `${caseId}.pdf`;
        const link = document.createElement("a");
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      } else {
        const data = await response.json();
        const markdown = data.markdown ?? createDossierContent(dossier);
        const blob = new Blob([markdown], { type: "text/markdown" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `${caseId}.md`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      }

      dossierProgress.setManualProgress(100, "completed", "Dossier erfolgreich exportiert");
      notifications.success("Dossier erstellt", "Der Export wurde abgeschlossen.");
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unbekannter Fehler";
      dossierProgress.setManualProgress(100, "failed", message);
      notifications.error("Dossier-Export fehlgeschlagen", message);
    }
  };

  const createDossierContent = (dossier: AnalyticsDossierExport): string => {
    let content = `# ${dossier.title}\n\n`;

    if (dossier.description) {
      content += `${dossier.description}\n\n`;
    }

    content += `## Report Metadata\n\n`;
    content += `- **Generated:** ${new Date(dossier.metadata.generatedAt).toLocaleString()}\n`;
    content += `- **Generated By:** ${dossier.metadata.generatedBy}\n`;
    content += `- **Version:** ${dossier.metadata.version}\n`;
    content += `- **Time Range:** ${dossier.filters.timeRange}\n\n`;
    if (dossier.metadata.caseId) {
      content += `- **Case ID:** ${dossier.metadata.caseId}\n`;
    }
    if (dossier.templateId) {
      const templateName = templates.find((tpl) => tpl.id === dossier.templateId)?.name;
      if (templateName) {
        content += `- **Template:** ${templateName}\n`;
      }
    }
    if (dossier.format) {
      content += `- **Format:** ${dossier.format.toUpperCase()}\n`;
    }

    if (dossier.filters.entityTypes.length > 0) {
      content += `- **Entity Types:** ${dossier.filters.entityTypes.join(", ")}\n`;
    }

    if (dossier.filters.sources.length > 0) {
      content += `- **Sources:** ${dossier.filters.sources.join(", ")}\n`;
    }

    content += `\n## Analytics Sections\n\n`;

    dossier.sections.forEach((section) => {
      content += `### ${section.name}\n\n`;
      content += `${section.description}\n\n`;
      content += `*[Data would be rendered here based on current analytics results]*\n\n`;
    });

    return content;
  };

  useEffect(() => {
    let ignore = false;

    const fetchTemplates = async () => {
      setTemplatesLoading(true);
      try {
        const response = await fetch("/api/collab/dossier/templates");
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        const data = await response.json();
        if (!ignore && Array.isArray(data?.items)) {
          setTemplates(data.items as DossierTemplate[]);
          setTemplateError(null);
        }
      } catch (error) {
        if (!ignore) {
          const message =
            error instanceof Error ? error.message : "Vorlagen konnten nicht geladen werden";
          setTemplateError(message);
          notifications.warning("Vorlagen fallback aktiv", message);
        }
      } finally {
        if (!ignore) {
          setTemplatesLoading(false);
        }
      }
    };

    fetchTemplates();

    return () => {
      ignore = true;
    };
  }, [notifications]);

  const availableSections: AnalyticsDossierSection[] = [
    {
      id: "entity-analytics",
      name: "Entity Analytics",
      description: "Entity distribution, top entities, and discovery trends",
      enabled: true,
      data: entityAnalytics.data,
    },
    {
      id: "source-coverage",
      name: "Source Coverage",
      description: "Source types, reliability metrics, and coverage analysis",
      enabled: true,
      data: sourceCoverage.data,
    },
    {
      id: "evidence-quality",
      name: "Evidence Quality",
      description: "Quality scores, verification rates, and reliability assessment",
      enabled: true,
      data: evidenceQuality.data,
    },
    {
      id: "workflow-runs",
      name: "Workflow Execution",
      description: "Workflow run history, success rates, and performance metrics",
      enabled: true,
      data: workflowRuns.data,
    },
    {
      id: "activity-timeline",
      name: "Activity Timeline",
      description: "Chronological view of OSINT findings and discoveries",
      enabled: true,
      data: timeline.data,
    },
    {
      id: "geospatial",
      name: "Geospatial Analysis",
      description: "Geographic distribution and location-based insights",
      enabled: true,
      data: geoEntities.data,
    },
    {
      id: "query-insights",
      name: "Query Insights",
      description: "Search patterns, performance, and user behavior analysis",
      enabled: queryInsights.data && queryInsights.data.totalQueries > 0,
      data: queryInsights.data,
    },
  ];

  return (
    <DashboardLayout
      title="OSINT Analytics"
      subtitle="Comprehensive analysis of intelligence gathering activities and findings"
    >
      <div className="p-6 space-y-8">
        {/* Header Controls */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Filter size={20} className="text-gray-500" />
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
              Analytics Dashboard
            </h2>
          </div>

          <button
            onClick={handleOpenDossierExport}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors"
          >
            <Download size={16} />
            Als Dossier exportieren
          </button>
        </div>
        {templateError && (
          <div className="text-xs text-red-600 dark:text-red-400">{templateError}</div>
        )}

        {/* Global Filters */}
        <FiltersBar
          filters={filters}
          onFiltersChange={handleFiltersChange}
          onRefresh={handleRefreshAll}
        />

        {/* Analytics Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Entity Analytics */}
          <Panel title="Entity Analysis" className="lg:col-span-2">
            <EntityAnalytics filters={filters} />
          </Panel>

          {/* Source Coverage */}
          <Panel title="Source Coverage">
            <SourceCoverage filters={filters} />
          </Panel>

          {/* Evidence Quality */}
          <Panel title="Evidence Quality">
            <EvidenceQuality filters={filters} />
          </Panel>

          {/* Graph Analytics */}
          <Panel title="Graph Analytics" className="lg:col-span-2">
            <GraphAnalytics className="w-full" />
          </Panel>

          {/* Workflow Runs */}
          <Panel title="Workflow Execution" className="lg:col-span-2">
            <WorkflowRunsTable filters={filters} />
          </Panel>

          {/* Activity Timeline */}
          <Panel title="Activity Timeline" className="lg:col-span-2">
            <ActivityTimeline
              filters={filters}
              onEventClick={(event) => console.log("Timeline event clicked:", event)}
            />
          </Panel>

          {/* Geospatial Map */}
          <Panel title="Geospatial Analysis" className="lg:col-span-2">
            <GeoMap
              filters={filters}
              onEntityClick={(entity) => console.log("Geo entity clicked:", entity)}
            />
          </Panel>

          {/* Query Insights - Only show if data available */}
          {queryInsights.data && queryInsights.data.totalQueries > 0 && (
            <Panel title="Query Insights" className="lg:col-span-2">
              <QueryInsights filters={filters} />
            </Panel>
          )}
        </div>
      </div>

      {/* Dossier Export Modal */}
      <DossierBuilderModal
        isOpen={showDossierModal}
        onClose={() => setShowDossierModal(false)}
        filters={filters}
        availableSections={availableSections}
        onExport={handleDossierExport}
        templates={templates}
        templatesLoading={templatesLoading}
      />
      <ProgressModal
        isOpen={showDossierProgress}
        title="Dossier Export"
        description="Wir bereiten den Bericht zum Download vor."
        state={dossierProgress.state}
        onClose={() => {
          setShowDossierProgress(false);
          setDossierTaskId(null);
        }}
        successLabel="Fenster schließen"
      />
    </DashboardLayout>
  );
}
