// Collaboration document management panel
import { useState } from "react";
import {
  FolderOpen,
  Plus,
  Search,
  Filter,
  Download,
  Share2,
  FileText,
  File,
  Image as ImageIcon,
  Video,
  Upload,
} from "lucide-react";
import { Workspace, Document, formatFileSize } from "@/lib/collaboration/collab-config";

interface CollabDocumentPanelProps {
  workspace: Workspace;
  documents?: Document[];
  onUpload?: (files: File[]) => void;
  onDocumentAction?: (document: Document, action: string) => void;
}

export function CollabDocumentPanel({
  workspace,
  documents = [],
  onUpload,
  onDocumentAction,
}: CollabDocumentPanelProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isDragging, setIsDragging] = useState(false);

  const filteredDocuments = documents.filter(
    (doc) =>
      doc.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      doc.tags.some((tag) => tag.toLowerCase().includes(searchTerm.toLowerCase())),
  );

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files);
      setSelectedFiles(files);
      onUpload?.(files);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    if (e.dataTransfer.files) {
      const files = Array.from(e.dataTransfer.files);
      setSelectedFiles(files);
      onUpload?.(files);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const getFileIcon = (type: string) => {
    if (type.startsWith("image/")) return <ImageIcon size={16} />;
    if (type.startsWith("video/")) return <Video size={16} />;
    if (type.includes("pdf") || type.includes("document")) return <FileText size={16} />;
    return <File size={16} />;
  };

  if (documents.length === 0 && !selectedFiles.length) {
    return (
      <div className="h-full flex items-center justify-center">
        <div
          className={`text-center p-8 border-2 border-dashed rounded-lg transition-colors ${
            isDragging
              ? "border-primary-400 bg-primary-50 dark:bg-primary-900/20"
              : "border-gray-300 dark:border-gray-600"
          }`}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
        >
          <FolderOpen size={48} className="mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
            Document Sharing
          </h3>
          <p className="text-gray-500 dark:text-gray-400 mb-4">
            Drag and drop files here or click to upload documents to share with your team.
          </p>
          <label className="inline-flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 cursor-pointer">
            <Plus size={16} />
            Upload Documents
            <input
              type="file"
              multiple
              onChange={handleFileSelect}
              className="hidden"
              accept="*/*"
            />
          </label>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Documents</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            {filteredDocuments.length} files shared
          </p>
        </div>
        <label className="inline-flex items-center gap-2 px-3 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700 cursor-pointer">
          <Upload size={16} />
          Upload
          <input type="file" multiple onChange={handleFileSelect} className="hidden" />
        </label>
      </div>

      {/* Search and filters */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <Search
              className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
              size={16}
            />
            <input
              type="text"
              placeholder="Search documents..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
            />
          </div>
          <button className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
            <Filter size={16} />
          </button>
        </div>
      </div>

      {/* Document list */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-3">
          {filteredDocuments.map((document) => (
            <div
              key={document.id}
              className="flex items-center gap-3 p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            >
              <div className="text-gray-400">{getFileIcon(document.type)}</div>

              <div className="flex-1 min-w-0">
                <h4 className="font-medium text-gray-900 dark:text-white truncate">
                  {document.name}
                </h4>
                <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
                  <span>{formatFileSize(document.size)}</span>
                  <span>•</span>
                  <span>by {document.uploadedBy.name}</span>
                  <span>•</span>
                  <span>{document.uploadedAt.toLocaleDateString()}</span>
                </div>
                {document.tags.length > 0 && (
                  <div className="flex items-center gap-1 mt-1">
                    {document.tags.slice(0, 3).map((tag, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full dark:bg-blue-900/30 dark:text-blue-300"
                      >
                        {tag}
                      </span>
                    ))}
                    {document.tags.length > 3 && (
                      <span className="text-xs text-gray-400">+{document.tags.length - 3}</span>
                    )}
                  </div>
                )}
              </div>

              <div className="flex items-center gap-1">
                <button
                  onClick={() => onDocumentAction?.(document, "download")}
                  className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600"
                  title="Download"
                >
                  <Download size={16} />
                </button>
                <button
                  onClick={() => onDocumentAction?.(document, "share")}
                  className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600"
                  title="Share"
                >
                  <Share2 size={16} />
                </button>
              </div>
            </div>
          ))}

          {filteredDocuments.length === 0 && searchTerm && (
            <div className="text-center py-8">
              <FileText size={32} className="mx-auto text-gray-400 mb-2" />
              <p className="text-gray-500 dark:text-gray-400">No documents match your search.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default CollabDocumentPanel;
