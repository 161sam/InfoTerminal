// Modularized Dossier Creation Page
import { useState, useEffect } from "react";
import { FileText } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import {
  DossierTemplateSelector,
  DossierItemManager,
  DossierSettingsPanel,
  DossierExportPanel,
  DossierPreviewPanel,
  DossierItem,
  DossierSettings,
  GeneratedDossier,
  DOSSIER_TEMPLATES,
  EXAMPLE_ITEMS,
  createDossierPayload,
} from "@/components/dossier/panels";

export default function DossierPage() {
  // State management
  const [title, setTitle] = useState("Investigation Report");
  const [items, setItems] = useState<DossierItem[]>([]);
  const [settings, setSettings] = useState<DossierSettings>({
    includeTimeline: true,
    includeSummary: true,
    includeVisualization: true,
    confidenceThreshold: 0.8,
    language: "en",
  });

  const [generatedDossier, setGeneratedDossier] = useState<GeneratedDossier | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<string>("");
  const [showPreview, setShowPreview] = useState(false);

  // Initialize with example items
  useEffect(() => {
    setItems(EXAMPLE_ITEMS);
  }, []);

  // Event handlers
  const handleTemplateSelect = (templateId: string) => {
    const template = DOSSIER_TEMPLATES.find((t) => t.id === templateId);
    if (!template) return;

    setTitle(template.name);
    setSettings(template.settings);
    setSelectedTemplate(templateId);
  };

  const handleCustomCreate = () => {
    setSelectedTemplate("");
    setTitle("Custom Dossier");
    setSettings({
      includeTimeline: true,
      includeSummary: true,
      includeVisualization: false,
      confidenceThreshold: 0.8,
      language: "en",
    });
  };

  const handleAddItem = (newItem: Omit<DossierItem, "id">) => {
    const item: DossierItem = {
      ...newItem,
      id: Date.now().toString(),
    };
    setItems((prev) => [...prev, item]);
  };

  const handleRemoveItem = (id: string) => {
    setItems((prev) => prev.filter((item) => item.id !== id));
  };

  const handleUpdateItem = (id: string, updates: Partial<DossierItem>) => {
    setItems((prev) => prev.map((item) => (item.id === id ? { ...item, ...updates } : item)));
  };

  const handleGenerate = async (payload: any): Promise<GeneratedDossier> => {
    // Simulate API call to dossier generation service
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Mock generated content
    const mockMarkdown = `# ${payload.title}

**Generated on:** ${new Date().toLocaleDateString()}
**Items Analyzed:** ${payload.items.docs.length + payload.items.nodes.length + payload.items.edges.length}
**Language:** ${payload.options.language.toUpperCase()}
**Confidence Threshold:** ${Math.round(payload.options.confidence * 100)}%

## Executive Summary
${payload.options.summary ? `This dossier provides a comprehensive analysis of the collected intelligence items. The investigation reveals patterns and connections across ${payload.items.nodes.length} entities and ${payload.items.edges.length} relationships.` : ""}

## Documents Analyzed
${payload.items.docs.map((doc: string, index: number) => `${index + 1}. ${doc}`).join("\n")}

## Key Entities
${payload.items.nodes.map((node: string, index: number) => `${index + 1}. **${node}** - High-confidence entity`).join("\n")}

## Relationships
${payload.items.edges.map((edge: string, index: number) => `${index + 1}. ${edge}`).join("\n")}

${
  payload.options.timeline
    ? `## Timeline
- **2024-01-15**: Initial document discovery
- **2024-02-01**: Entity identification began
- **2024-03-01**: Relationship mapping completed
`
    : ""
}

## Conclusion
Based on the analyzed data with a confidence threshold of ${Math.round(payload.options.confidence * 100)}%, this investigation provides actionable intelligence for further analysis.

---
*This dossier was generated automatically by InfoTerminal OSINT Platform*`;

    const result: GeneratedDossier = {
      markdown: mockMarkdown,
      pdfUrl: "/api/dossier/export/pdf/" + Date.now(),
      metadata: {
        title: payload.title,
        generatedAt: new Date().toISOString(),
        itemCount:
          payload.items.docs.length + payload.items.nodes.length + payload.items.edges.length,
        size: Math.round(mockMarkdown.length / 1024) + " KB",
      },
    };

    return result;
  };

  const handlePreview = (dossier: GeneratedDossier) => {
    setGeneratedDossier(dossier);
    setShowPreview(true);
  };

  const handleExport = (format: string) => {
    console.log("Export dossier as:", format);
    // Handle export logic
  };

  return (
    <DashboardLayout
      title="Dossier Creation"
      subtitle="Generate comprehensive intelligence reports"
    >
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Title Input */}
        <Panel>
          <div className="flex items-center gap-3">
            <FileText size={20} className="text-gray-600 dark:text-gray-400" />
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Dossier Title
              </label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter dossier title..."
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              />
            </div>
          </div>
        </Panel>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Template Selection */}
            <Panel>
              <DossierTemplateSelector
                selectedTemplate={selectedTemplate}
                onTemplateSelect={handleTemplateSelect}
                onCustomCreate={handleCustomCreate}
              />
            </Panel>

            {/* Item Management */}
            <Panel>
              <DossierItemManager
                items={items}
                onAddItem={handleAddItem}
                onRemoveItem={handleRemoveItem}
                onUpdateItem={handleUpdateItem}
              />
            </Panel>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Settings */}
            <Panel>
              <DossierSettingsPanel
                settings={settings}
                items={items}
                onSettingsChange={setSettings}
              />
            </Panel>

            {/* Export */}
            <Panel>
              <DossierExportPanel
                title={title}
                items={items}
                settings={settings}
                onGenerate={handleGenerate}
                onPreview={handlePreview}
              />
            </Panel>
          </div>
        </div>
      </div>

      {/* Preview Modal */}
      {showPreview && generatedDossier && (
        <DossierPreviewPanel
          dossier={generatedDossier}
          onClose={() => setShowPreview(false)}
          onExport={handleExport}
        />
      )}
    </DashboardLayout>
  );
}
