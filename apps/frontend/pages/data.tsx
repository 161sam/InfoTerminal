// apps/frontend/pages/data.tsx - Data Management & Import Hub
import { useState, useEffect, useCallback, useRef } from "react";
import {
  Database,
  Upload,
  Download,
  RefreshCw,
  Trash2,
  AlertTriangle,
  CheckCircle,
  Clock,
  HardDrive,
  FileText,
  Users,
  BarChart3,
  Image,
  Video,
  Music,
  Eye,
} from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { cn } from "@/lib/utils";

// Data Sources interfaces
interface DataSource {
  id: string;
  name: string;
  type: string;
  status: "active" | "inactive" | "syncing" | "error";
  documents: number;
  lastSync: string;
  size: string;
}

interface StorageInfo {
  used: number;
  total: number;
  documents: number;
  entities: number;
  indices: number;
}

// Import interfaces
interface ImportItem {
  id: string;
  file: File;
  fileName: string;
  fileType: "document" | "image" | "audio" | "video" | "other";
  status: "pending" | "processing" | "success" | "error";
  progress: number;
  result?: any;
  message?: string;
  uploadedAt?: Date;
}

interface ImportStats {
  total: number;
  processing: number;
  completed: number;
  failed: number;
}

// Mock data
const MOCK_DATA_SOURCES: DataSource[] = [
  {
    id: "1",
    name: "Document Storage",
    type: "Elasticsearch",
    status: "active",
    documents: 12847,
    lastSync: "2024-03-01 10:30:00",
    size: "2.4 GB",
  },
  {
    id: "2",
    name: "Entity Database",
    type: "Neo4j",
    status: "active",
    documents: 45621,
    lastSync: "2024-03-01 10:25:00",
    size: "1.8 GB",
  },
  {
    id: "3",
    name: "Aleph Integration",
    type: "External API",
    status: "inactive",
    documents: 0,
    lastSync: "2024-02-28 15:20:00",
    size: "0 MB",
  },
];

const MOCK_STORAGE: StorageInfo = {
  used: 4.2,
  total: 100,
  documents: 12847,
  entities: 45621,
  indices: 8,
};

// Utility functions for imports
const getFileType = (file: File): ImportItem["fileType"] => {
  if (file.type.startsWith("image/")) return "image";
  if (file.type.startsWith("video/")) return "video";
  if (file.type.startsWith("audio/")) return "audio";
  if (file.type.includes("pdf") || file.type.includes("text") || file.type.includes("document")) {
    return "document";
  }
  return "other";
};

const getFileIcon = (fileType: ImportItem["fileType"]) => {
  switch (fileType) {
    case "document":
      return FileText;
    case "image":
      return Image;
    case "video":
      return Video;
    case "audio":
      return Music;
    default:
      return Database;
  }
};

const getStatusIcon = (status: ImportItem["status"]) => {
  switch (status) {
    case "success":
      return CheckCircle;
    case "error":
      return AlertTriangle;
    case "processing":
      return RefreshCw;
    default:
      return Clock;
  }
};

const getStatusColor = (status: ImportItem["status"]) => {
  switch (status) {
    case "success":
      return "text-green-600 bg-green-100 dark:bg-green-900/30 dark:text-green-300";
    case "error":
      return "text-red-600 bg-red-100 dark:bg-red-900/30 dark:text-red-300";
    case "processing":
      return "text-blue-600 bg-blue-100 dark:bg-blue-900/30 dark:text-blue-300";
    default:
      return "text-gray-600 bg-gray-100 dark:bg-gray-800 dark:text-gray-300";
  }
};

const getApiEndpoint = (fileType: ImportItem["fileType"]) => {
  switch (fileType) {
    case "document":
      return "/api/documents/upload";
    case "image":
    case "video":
    case "audio":
      return "/api/forensics/ingest";
    default:
      return "/api/documents/upload";
  }
};

export default function DataPage() {
  // Data Sources state
  const [dataSources, setDataSources] = useState<DataSource[]>(MOCK_DATA_SOURCES);
  const [storageInfo, setStorageInfo] = useState<StorageInfo>(MOCK_STORAGE);
  const [loading, setLoading] = useState(false);

  // Import state
  const [imports, setImports] = useState<ImportItem[]>([]);
  const [isDragActive, setIsDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Tab state
  const [activeTab, setActiveTab] = useState<"sources" | "import">("sources");

  const stats: ImportStats = {
    total: imports.length,
    processing: imports.filter((item) => item.status === "processing").length,
    completed: imports.filter((item) => item.status === "success").length,
    failed: imports.filter((item) => item.status === "error").length,
  };

  // Data Sources functions
  const getDataSourceStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "text-green-600 bg-green-100";
      case "syncing":
        return "text-blue-600 bg-blue-100";
      case "error":
        return "text-red-600 bg-red-100";
      case "inactive":
        return "text-gray-600 bg-gray-100";
      default:
        return "text-gray-600 bg-gray-100";
    }
  };

  const getDataSourceStatusIcon = (status: string) => {
    switch (status) {
      case "active":
        return <CheckCircle size={16} />;
      case "syncing":
        return <RefreshCw size={16} className="animate-spin" />;
      case "error":
        return <AlertTriangle size={16} />;
      case "inactive":
        return <Clock size={16} />;
      default:
        return <Clock size={16} />;
    }
  };

  const handleSync = async (sourceId: string) => {
    setDataSources((prev) =>
      prev.map((source) =>
        source.id === sourceId ? { ...source, status: "syncing" as const } : source,
      ),
    );

    // Simulate sync process
    setTimeout(() => {
      setDataSources((prev) =>
        prev.map((source) =>
          source.id === sourceId
            ? {
                ...source,
                status: "active" as const,
                lastSync: new Date().toISOString().slice(0, 19).replace("T", " "),
              }
            : source,
        ),
      );
    }, 3000);
  };

  const handleExportData = () => {
    // Simulate data export
    const data = {
      dataSources,
      storageInfo,
      exportedAt: new Date().toISOString(),
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "data-export.json";
    a.click();
    URL.revokeObjectURL(url);
  };

  // Import functions
  const handleFiles = useCallback((files: FileList) => {
    const newImports: ImportItem[] = [];

    Array.from(files).forEach((file) => {
      const fileType = getFileType(file);
      const importItem: ImportItem = {
        id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        file,
        fileName: file.name,
        fileType,
        status: "pending",
        progress: 0,
      };

      newImports.push(importItem);
    });

    setImports((prev) => [...prev, ...newImports]);

    // Start processing each file
    newImports.forEach((item) => processFile(item));
  }, []);

  const processFile = async (item: ImportItem) => {
    try {
      // Update status to processing
      setImports((prev) =>
        prev.map((imp) =>
          imp.id === item.id ? { ...imp, status: "processing", progress: 0 } : imp,
        ),
      );

      const formData = new FormData();
      formData.append("file", item.file);

      const apiEndpoint = getApiEndpoint(item.fileType);

      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setImports((prev) =>
          prev.map((imp) =>
            imp.id === item.id ? { ...imp, progress: Math.min(imp.progress + 15, 90) } : imp,
          ),
        );
      }, 200);

      const response = await fetch(apiEndpoint, {
        method: "POST",
        body: formData,
      });

      clearInterval(progressInterval);

      if (response.ok) {
        const result = await response.json();

        setImports((prev) =>
          prev.map((imp) =>
            imp.id === item.id
              ? {
                  ...imp,
                  status: "success",
                  progress: 100,
                  result,
                  uploadedAt: new Date(),
                  message: `Successfully processed ${item.fileType}`,
                }
              : imp,
          ),
        );
      } else {
        const errorText = await response.text();
        setImports((prev) =>
          prev.map((imp) =>
            imp.id === item.id
              ? {
                  ...imp,
                  status: "error",
                  progress: 0,
                  message: `Upload failed: ${errorText}`,
                }
              : imp,
          ),
        );
      }
    } catch (error) {
      setImports((prev) =>
        prev.map((imp) =>
          imp.id === item.id
            ? {
                ...imp,
                status: "error",
                progress: 0,
                message: `Network error: ${error instanceof Error ? error.message : "Unknown error"}`,
              }
            : imp,
        ),
      );
    }
  };

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragActive(false);

      const files = e.dataTransfer.files;
      if (files.length > 0) {
        handleFiles(files);
      }
    },
    [handleFiles],
  );

  const handleFileInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files;
      if (files && files.length > 0) {
        handleFiles(files);
      }
    },
    [handleFiles],
  );

  const removeItem = useCallback((id: string) => {
    setImports((prev) => prev.filter((item) => item.id !== id));
  }, []);

  const clearCompleted = useCallback(() => {
    setImports((prev) =>
      prev.filter((item) => item.status !== "success" && item.status !== "error"),
    );
  }, []);

  const retryItem = useCallback((item: ImportItem) => {
    setImports((prev) =>
      prev.map((imp) =>
        imp.id === item.id ? { ...imp, status: "pending", progress: 0, message: undefined } : imp,
      ),
    );
    processFile(item);
  }, []);

  // Storage overview component
  const renderStorageOverview = () => (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <Panel padded>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600 dark:text-slate-400">Storage Used</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-slate-100">
              {storageInfo.used} GB
            </p>
            <p className="text-xs text-gray-500">of {storageInfo.total} GB total</p>
          </div>
          <HardDrive size={24} className="text-blue-500" />
        </div>
        <div className="mt-3">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-500 h-2 rounded-full"
              style={{ width: `${(storageInfo.used / storageInfo.total) * 100}%` }}
            />
          </div>
        </div>
      </Panel>

      <Panel padded>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600 dark:text-slate-400">Documents</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-slate-100">
              {storageInfo.documents.toLocaleString()}
            </p>
          </div>
          <FileText size={24} className="text-green-500" />
        </div>
      </Panel>

      <Panel padded>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600 dark:text-slate-400">Entities</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-slate-100">
              {storageInfo.entities.toLocaleString()}
            </p>
          </div>
          <Users size={24} className="text-purple-500" />
        </div>
      </Panel>

      <Panel padded>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600 dark:text-slate-400">Indices</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-slate-100">
              {storageInfo.indices}
            </p>
          </div>
          <BarChart3 size={24} className="text-orange-500" />
        </div>
      </Panel>
    </div>
  );

  // Data Sources tab content
  const renderDataSourcesTab = () => (
    <div className="space-y-6">
      {renderStorageOverview()}

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Data Sources */}
        <div className="lg:col-span-2">
          <Panel>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold">Data Sources</h3>
              <button className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm">
                Add Source
              </button>
            </div>

            <div className="space-y-4">
              {dataSources.map((source) => (
                <div
                  key={source.id}
                  className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                >
                  <div className="flex items-center gap-4">
                    <Database size={20} className="text-gray-500" />
                    <div>
                      <h4 className="font-medium text-gray-900">{source.name}</h4>
                      <p className="text-sm text-gray-500">{source.type}</p>
                      <p className="text-xs text-gray-400">
                        {source.documents.toLocaleString()} documents • {source.size}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <div className="text-right">
                      <div
                        className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${getDataSourceStatusColor(source.status)}`}
                      >
                        {getDataSourceStatusIcon(source.status)}
                        {source.status}
                      </div>
                      <p className="text-xs text-gray-500 mt-1">
                        Last sync: {new Date(source.lastSync).toLocaleString()}
                      </p>
                    </div>

                    <div className="flex gap-1">
                      <button
                        onClick={() => handleSync(source.id)}
                        disabled={source.status === "syncing"}
                        className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded disabled:opacity-50"
                      >
                        <RefreshCw
                          size={16}
                          className={source.status === "syncing" ? "animate-spin" : ""}
                        />
                      </button>
                      <button className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded">
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Panel>
        </div>

        {/* Quick Actions & Data Health */}
        <div className="space-y-6">
          <Panel>
            <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <button
                onClick={() => setActiveTab("import")}
                className="w-full flex items-center gap-3 p-3 text-left bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors dark:bg-gray-800 dark:text-slate-200 dark:hover:bg-gray-700"
              >
                <Upload size={16} />
                <div>
                  <div className="font-medium">Import Data</div>
                  <div className="text-xs text-blue-600 dark:text-slate-400">
                    Upload documents or media files
                  </div>
                </div>
              </button>

              <button
                onClick={handleExportData}
                className="w-full flex items-center gap-3 p-3 text-left bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors dark:bg-gray-800 dark:text-slate-200 dark:hover:bg-gray-700"
              >
                <Download size={16} />
                <div>
                  <div className="font-medium">Export Data</div>
                  <div className="text-xs text-green-600 dark:text-slate-400">
                    Download as JSON/CSV
                  </div>
                </div>
              </button>

              <button className="w-full flex items-center gap-3 p-3 text-left bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors dark:bg-gray-800 dark:text-slate-200 dark:hover:bg-gray-700">
                <RefreshCw size={16} />
                <div>
                  <div className="font-medium">Sync All</div>
                  <div className="text-xs text-purple-600 dark:text-slate-400">
                    Refresh all data sources
                  </div>
                </div>
              </button>
            </div>
          </Panel>

          {/* Data Health */}
          <Panel>
            <h3 className="text-lg font-semibold mb-4">Data Health</h3>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Search Index</span>
                <div className="flex items-center gap-2">
                  <CheckCircle size={16} className="text-green-500" />
                  <span className="text-sm font-medium text-green-600">Healthy</span>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Entity Resolution</span>
                <div className="flex items-center gap-2">
                  <CheckCircle size={16} className="text-green-500" />
                  <span className="text-sm font-medium text-green-600">Optimal</span>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Graph Database</span>
                <div className="flex items-center gap-2">
                  <AlertTriangle size={16} className="text-yellow-500" />
                  <span className="text-sm font-medium text-yellow-600">Warning</span>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Backup Status</span>
                <div className="flex items-center gap-2">
                  <Clock size={16} className="text-blue-500" />
                  <span className="text-sm font-medium text-blue-600">2h ago</span>
                </div>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-800">
              <button className="w-full px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200">
                View Detailed Report
              </button>
            </div>
          </Panel>
        </div>
      </div>
    </div>
  );

  // Import tab content
  const renderImportTab = () => (
    <div className="space-y-6">
      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Panel padded>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-slate-400">Total Files</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-slate-100">{stats.total}</p>
            </div>
            <Upload size={24} className="text-blue-500" />
          </div>
        </Panel>

        <Panel padded>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-slate-400">Processing</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-slate-100">
                {stats.processing}
              </p>
            </div>
            <RefreshCw size={24} className="text-blue-500 animate-spin" />
          </div>
        </Panel>

        <Panel padded>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-slate-400">Completed</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-slate-100">
                {stats.completed}
              </p>
            </div>
            <CheckCircle size={24} className="text-green-500" />
          </div>
        </Panel>

        <Panel padded>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-slate-400">Failed</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-slate-100">{stats.failed}</p>
            </div>
            <AlertTriangle size={24} className="text-red-500" />
          </div>
        </Panel>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Upload Area */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="h-5 w-5" />
                File Import
              </CardTitle>
              <p className="text-sm text-gray-600 dark:text-slate-400">
                Upload documents, images, audio, video, and other files for analysis
              </p>
            </CardHeader>
            <CardContent>
              <div
                className={cn(
                  "border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors",
                  isDragActive
                    ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20"
                    : "border-gray-300 dark:border-gray-700",
                )}
                onDragEnter={handleDragEnter}
                onDragLeave={handleDragLeave}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-center w-16 h-16 mx-auto bg-gray-100 dark:bg-gray-800 rounded-full">
                    <Upload className="h-8 w-8 text-gray-400" />
                  </div>
                  <div>
                    <p className="text-lg font-medium">Drop files here or click to browse</p>
                    <p className="text-sm text-gray-500">
                      Supports all file types • Drag & drop multiple files
                    </p>
                  </div>
                </div>

                <input
                  ref={fileInputRef}
                  type="file"
                  className="hidden"
                  multiple
                  accept="*/*"
                  onChange={handleFileInputChange}
                />
              </div>
            </CardContent>
          </Card>

          {/* Import List */}
          {imports.length > 0 && (
            <Card className="mt-6">
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle>Import Queue</CardTitle>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" onClick={clearCompleted}>
                    Clear Completed
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {imports.map((item) => {
                    const FileIcon = getFileIcon(item.fileType);
                    const StatusIcon = getStatusIcon(item.status);

                    return (
                      <div key={item.id} className="flex items-center gap-4 p-3 border rounded-lg">
                        <div className="flex items-center gap-3">
                          <FileIcon className="h-5 w-5 text-gray-500" />
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium truncate">{item.fileName}</p>
                            <p className="text-xs text-gray-500">
                              {item.fileType} • {(item.file.size / 1024 / 1024).toFixed(2)} MB
                            </p>
                          </div>
                        </div>

                        <div className="flex items-center gap-3">
                          <div
                            className={cn(
                              "flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium",
                              getStatusColor(item.status),
                            )}
                          >
                            <StatusIcon
                              className={cn(
                                "h-3 w-3",
                                item.status === "processing" && "animate-spin",
                              )}
                            />
                            {item.status}
                          </div>

                          {item.status === "processing" && item.progress > 0 && (
                            <div className="w-20">
                              <Progress value={item.progress} className="h-1" />
                            </div>
                          )}

                          <div className="flex gap-1">
                            {item.status === "error" && (
                              <Button
                                size="sm"
                                variant="ghost"
                                onClick={() => retryItem(item)}
                                className="p-2"
                              >
                                <RefreshCw className="h-3 w-3" />
                              </Button>
                            )}

                            <Button
                              size="sm"
                              variant="ghost"
                              onClick={() => removeItem(item.id)}
                              className="p-2 text-red-500 hover:text-red-700"
                            >
                              <Trash2 className="h-3 w-3" />
                            </Button>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Info Panel */}
        <div>
          <Card>
            <CardHeader>
              <CardTitle>File Type Processing</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3 text-sm">
                <div className="flex items-center gap-3">
                  <FileText className="h-4 w-4 text-blue-500" />
                  <div>
                    <p className="font-medium">Documents</p>
                    <p className="text-gray-500">PDF, TXT, DOC → Entity extraction & indexing</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <Image className="h-4 w-4 text-green-500" />
                  <div>
                    <p className="font-medium">Images</p>
                    <p className="text-gray-500">JPG, PNG, BMP → EXIF & forensic analysis</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <Video className="h-4 w-4 text-purple-500" />
                  <div>
                    <p className="font-medium">Video</p>
                    <p className="text-gray-500">MP4, AVI, MOV → Metadata extraction</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <Music className="h-4 w-4 text-orange-500" />
                  <div>
                    <p className="font-medium">Audio</p>
                    <p className="text-gray-500">MP3, WAV, M4A → Audio analysis</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Recent Uploads */}
          <Card className="mt-6">
            <CardHeader>
              <CardTitle>Recent Uploads</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {imports
                  .filter((item) => item.status === "success")
                  .slice(0, 5)
                  .map((item) => {
                    const FileIcon = getFileIcon(item.fileType);
                    return (
                      <div key={item.id} className="flex items-center gap-3 text-sm">
                        <FileIcon className="h-4 w-4 text-green-500" />
                        <div className="flex-1 min-w-0">
                          <p className="truncate">{item.fileName}</p>
                          <p className="text-gray-500 text-xs">
                            {item.uploadedAt?.toLocaleTimeString()}
                          </p>
                        </div>
                        <Button size="sm" variant="ghost" className="p-2">
                          <Eye className="h-3 w-3" />
                        </Button>
                      </div>
                    );
                  })}

                {stats.completed === 0 && (
                  <p className="text-center text-gray-500 py-4">No recent uploads</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );

  return (
    <DashboardLayout title="Data Management" subtitle="Manage data sources and import files">
      <div className="p-6">
        <Tabs
          value={activeTab}
          onValueChange={(value) => setActiveTab(value as any)}
          className="space-y-6"
        >
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="sources" className="flex items-center gap-2">
              <Database className="h-4 w-4" />
              Data Sources
            </TabsTrigger>
            <TabsTrigger value="import" className="flex items-center gap-2">
              <Upload className="h-4 w-4" />
              Import Files
            </TabsTrigger>
          </TabsList>

          <TabsContent value="sources">{renderDataSourcesTab()}</TabsContent>

          <TabsContent value="import">{renderImportTab()}</TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
}
