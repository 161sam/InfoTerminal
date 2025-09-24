// Dossier preview panel
import { useState } from "react";
import { X, Download, Copy, Eye, Maximize2 } from "lucide-react";
import { GeneratedDossier } from "@/lib/dossier/dossier-config";

interface DossierPreviewPanelProps {
  dossier: GeneratedDossier;
  onClose: () => void;
  onExport?: (format: string) => void;
}

export function DossierPreviewPanel({ dossier, onClose, onExport }: DossierPreviewPanelProps) {
  const [isFullscreen, setIsFullscreen] = useState(false);

  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(dossier.markdown);
    // You could add a toast notification here
  };

  const handlePrint = () => {
    const printWindow = window.open("", "_blank");
    if (printWindow) {
      printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
          <title>${dossier.metadata.title}</title>
          <style>
            body {
              font-family: Arial, sans-serif;
              margin: 40px;
              line-height: 1.6;
              color: #333;
            }
            h1, h2, h3, h4, h5, h6 {
              color: #2c3e50;
              margin-top: 30px;
              margin-bottom: 15px;
            }
            h1 { font-size: 2em; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
            h2 { font-size: 1.5em; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }
            pre {
              background: #f8f9fa;
              padding: 15px;
              border-radius: 5px;
              border-left: 4px solid #3498db;
              overflow-x: auto;
            }
            code {
              background: #f8f9fa;
              padding: 2px 4px;
              border-radius: 3px;
              font-family: 'Courier New', monospace;
            }
            blockquote {
              border-left: 4px solid #3498db;
              margin: 0;
              padding-left: 20px;
              color: #666;
            }
            table {
              border-collapse: collapse;
              width: 100%;
              margin: 20px 0;
            }
            th, td {
              border: 1px solid #ddd;
              padding: 12px;
              text-align: left;
            }
            th {
              background-color: #f8f9fa;
              font-weight: bold;
            }
            .metadata {
              background: #f8f9fa;
              padding: 15px;
              border-radius: 5px;
              margin-bottom: 30px;
              font-size: 0.9em;
              color: #666;
            }
            @media print {
              body { margin: 20px; }
              .no-print { display: none; }
            }
          </style>
        </head>
        <body>
          <div class="metadata">
            <strong>Document:</strong> ${dossier.metadata.title}<br>
            <strong>Generated:</strong> ${new Date(dossier.metadata.generatedAt).toLocaleString()}<br>
            <strong>Items:</strong> ${dossier.metadata.itemCount}<br>
            <strong>Size:</strong> ${dossier.metadata.size}
          </div>
          <pre>${dossier.markdown}</pre>
        </body>
        </html>
      `);
      printWindow.document.close();
      printWindow.print();
    }
  };

  return (
    <div className={`fixed inset-0 z-50 ${isFullscreen ? "" : "p-4"}`}>
      <div className="absolute inset-0 bg-black bg-opacity-50" onClick={onClose} />

      <div
        className={`relative bg-white dark:bg-gray-900 rounded-lg shadow-xl flex flex-col ${
          isFullscreen ? "h-full" : "h-full max-h-[90vh] mx-auto max-w-4xl"
        }`}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
          <div className="flex items-center gap-3">
            <Eye size={20} className="text-primary-600 dark:text-primary-400" />
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white">Dossier Preview</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">{dossier.metadata.title}</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsFullscreen(!isFullscreen)}
              className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              title={isFullscreen ? "Exit fullscreen" : "Enter fullscreen"}
            >
              <Maximize2 size={16} />
            </button>

            <button
              onClick={handleCopyToClipboard}
              className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              title="Copy to clipboard"
            >
              <Copy size={16} />
            </button>

            <button
              onClick={handlePrint}
              className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              title="Print"
            >
              <Download size={16} />
            </button>

            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              title="Close"
            >
              <X size={16} />
            </button>
          </div>
        </div>

        {/* Metadata */}
        <div className="p-4 bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="text-gray-500 dark:text-gray-400">Generated:</span>
              <div className="font-medium text-gray-900 dark:text-white">
                {new Date(dossier.metadata.generatedAt).toLocaleDateString()}
              </div>
            </div>
            <div>
              <span className="text-gray-500 dark:text-gray-400">Items:</span>
              <div className="font-medium text-gray-900 dark:text-white">
                {dossier.metadata.itemCount}
              </div>
            </div>
            <div>
              <span className="text-gray-500 dark:text-gray-400">Size:</span>
              <div className="font-medium text-gray-900 dark:text-white">
                {dossier.metadata.size}
              </div>
            </div>
            <div>
              <span className="text-gray-500 dark:text-gray-400">Format:</span>
              <div className="font-medium text-gray-900 dark:text-white">Markdown</div>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-hidden">
          <div className="h-full overflow-y-auto p-6">
            <div className="prose prose-sm dark:prose-invert max-w-none">
              <pre className="whitespace-pre-wrap font-mono text-sm bg-gray-50 dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700 overflow-x-auto">
                {dossier.markdown}
              </pre>
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-700 flex-shrink-0">
          <div className="flex justify-between items-center">
            <div className="text-sm text-gray-500 dark:text-gray-400">
              {dossier.markdown.length.toLocaleString()} characters
            </div>

            <div className="flex gap-3">
              {onExport && (
                <>
                  <button
                    onClick={() => onExport("markdown")}
                    className="px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600"
                  >
                    Export Markdown
                  </button>
                  <button
                    onClick={() => onExport("pdf")}
                    className="px-3 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700"
                  >
                    Export PDF
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DossierPreviewPanel;
