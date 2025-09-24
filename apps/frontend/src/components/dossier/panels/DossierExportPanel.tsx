// Dossier export and generation panel
import { useState } from "react";
import {
  Download,
  RefreshCw,
  FileText,
  Eye,
  Save,
  Share2,
  CheckCircle,
  AlertTriangle,
  Clock,
} from "lucide-react";
import {
  DossierItem,
  DossierSettings,
  GeneratedDossier,
  DossierExportOptions,
  createDossierPayload,
  validateDossierItems,
  formatFileSize,
} from "@/lib/dossier/dossier-config";

interface DossierExportPanelProps {
  title: string;
  items: DossierItem[];
  settings: DossierSettings;
  onGenerate: (payload: any) => Promise<GeneratedDossier>;
  onPreview: (dossier: GeneratedDossier) => void;
}

export function DossierExportPanel({
  title,
  items,
  settings,
  onGenerate,
  onPreview,
}: DossierExportPanelProps) {
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedDossier, setGeneratedDossier] = useState<GeneratedDossier | null>(null);
  const [exportOptions, setExportOptions] = useState<DossierExportOptions>({
    format: "pdf",
    includeImages: true,
    includeMetadata: true,
  });
  const [error, setError] = useState<string | null>(null);

  const validation = validateDossierItems(items);
  const canGenerate = validation.isValid && title.trim().length > 0;

  const handleGenerate = async () => {
    if (!canGenerate) return;

    setIsGenerating(true);
    setError(null);

    try {
      const payload = createDossierPayload(title, items, settings);
      const result = await onGenerate(payload);
      setGeneratedDossier(result);
    } catch (err: any) {
      setError(err.message || "Failed to generate dossier");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExport = (format: string) => {
    if (!generatedDossier) return;

    // Create a blob based on format
    let blob: Blob;
    let filename: string;

    switch (format) {
      case "markdown":
        blob = new Blob([generatedDossier.markdown], { type: "text/markdown" });
        filename = `${title.replace(/[^a-zA-Z0-9]/g, "_")}.md`;
        break;
      case "html":
        // Convert markdown to basic HTML (simplified)
        const htmlContent = `
<!DOCTYPE html>
<html>
<head>
    <title>${title}</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        h1, h2, h3 { color: #333; }
        pre { background: #f4f4f4; padding: 15px; border-radius: 5px; }
        code { background: #f4f4f4; padding: 2px 4px; border-radius: 3px; }
    </style>
</head>
<body>
    <pre>${generatedDossier.markdown}</pre>
</body>
</html>`;
        blob = new Blob([htmlContent], { type: "text/html" });
        filename = `${title.replace(/[^a-zA-Z0-9]/g, "_")}.html`;
        break;
      default:
        if (generatedDossier.pdfUrl) {
          // Open PDF URL
          window.open(generatedDossier.pdfUrl, "_blank");
          return;
        }
        return;
    }

    // Download the file
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const getGenerationStatus = () => {
    if (isGenerating) {
      return {
        icon: <RefreshCw size={16} className="animate-spin text-blue-600" />,
        text: "Generating dossier...",
        color: "text-blue-600 dark:text-blue-400",
      };
    }

    if (error) {
      return {
        icon: <AlertTriangle size={16} className="text-red-600" />,
        text: error,
        color: "text-red-600 dark:text-red-400",
      };
    }

    if (generatedDossier) {
      return {
        icon: <CheckCircle size={16} className="text-green-600" />,
        text: "Dossier generated successfully",
        color: "text-green-600 dark:text-green-400",
      };
    }

    return null;
  };

  const status = getGenerationStatus();

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2">
        <Download size={20} className="text-gray-600 dark:text-gray-400" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Generate & Export</h3>
      </div>

      {/* Generation Button */}
      <div className="space-y-4">
        <div>
          <button
            onClick={handleGenerate}
            disabled={!canGenerate || isGenerating}
            className="w-full px-4 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
          >
            {isGenerating ? (
              <>
                <RefreshCw size={16} className="animate-spin" />
                Generating Dossier...
              </>
            ) : (
              <>
                <FileText size={16} />
                Generate Dossier
              </>
            )}
          </button>

          {!canGenerate && !isGenerating && (
            <div className="mt-2 text-sm text-red-600 dark:text-red-400">
              {!title.trim() && "Please enter a title"}
              {!validation.isValid &&
                validation.errors.map((error, index) => <div key={index}>• {error}</div>)}
            </div>
          )}
        </div>

        {/* Status */}
        {status && (
          <div className={`flex items-center gap-2 ${status.color}`}>
            {status.icon}
            <span className="text-sm">{status.text}</span>
          </div>
        )}
      </div>

      {/* Export Options */}
      {generatedDossier && (
        <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800">
          <h4 className="font-medium text-gray-900 dark:text-white mb-3">Export Options</h4>

          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => handleExport("markdown")}
                className="flex items-center gap-2 px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <FileText size={16} />
                Markdown
              </button>

              <button
                onClick={() => handleExport("html")}
                className="flex items-center gap-2 px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <FileText size={16} />
                HTML
              </button>

              <button
                onClick={() => handleExport("pdf")}
                className="flex items-center gap-2 px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <Download size={16} />
                PDF
              </button>

              <button
                onClick={() => onPreview(generatedDossier)}
                className="flex items-center gap-2 px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <Eye size={16} />
                Preview
              </button>
            </div>

            {/* Export Settings */}
            <div className="space-y-2 pt-3 border-t border-gray-200 dark:border-gray-600">
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={exportOptions.includeImages}
                  onChange={(e) =>
                    setExportOptions((prev) => ({
                      ...prev,
                      includeImages: e.target.checked,
                    }))
                  }
                  className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                />
                <span className="text-sm text-gray-700 dark:text-gray-300">
                  Include images and visualizations
                </span>
              </label>

              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={exportOptions.includeMetadata}
                  onChange={(e) =>
                    setExportOptions((prev) => ({
                      ...prev,
                      includeMetadata: e.target.checked,
                    }))
                  }
                  className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                />
                <span className="text-sm text-gray-700 dark:text-gray-300">
                  Include generation metadata
                </span>
              </label>
            </div>
          </div>
        </div>
      )}

      {/* Dossier Info */}
      {generatedDossier && (
        <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-900/30 rounded-lg">
          <h4 className="font-medium text-green-900 dark:text-green-100 mb-2">
            Dossier Generated Successfully
          </h4>
          <div className="space-y-1 text-sm text-green-700 dark:text-green-300">
            <div className="flex justify-between">
              <span>Title:</span>
              <span className="font-medium">{generatedDossier.metadata.title}</span>
            </div>
            <div className="flex justify-between">
              <span>Items:</span>
              <span className="font-medium">{generatedDossier.metadata.itemCount}</span>
            </div>
            <div className="flex justify-between">
              <span>Size:</span>
              <span className="font-medium">{generatedDossier.metadata.size}</span>
            </div>
            <div className="flex justify-between">
              <span>Generated:</span>
              <span className="font-medium">
                {new Date(generatedDossier.metadata.generatedAt).toLocaleString()}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="flex gap-3">
        <button
          onClick={() => setGeneratedDossier(null)}
          disabled={isGenerating}
          className="flex-1 px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
        >
          Reset
        </button>

        <button
          onClick={() => {
            if (generatedDossier) {
              navigator.clipboard.writeText(generatedDossier.markdown);
            }
          }}
          disabled={!generatedDossier}
          className="flex-1 px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
        >
          <Save size={16} />
          Copy to Clipboard
        </button>
      </div>
    </div>
  );
}

export default DossierExportPanel;
