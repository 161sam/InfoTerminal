"use client";

import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  Trash2,
  AlertTriangle,
  HardDrive,
  Database,
  FileText,
  Image,
  Download,
  Clock,
} from "lucide-react";

interface DataCategory {
  id: string;
  name: string;
  description: string;
  icon: React.ReactNode;
  size: number;
  fileCount: number;
  lastAccessed: number;
  selected: boolean;
  sensitive: boolean;
}

interface WipeProgress {
  category: string;
  progress: number;
  completed: boolean;
  error?: string;
}

interface DataWipeControlsProps {
  sessionId?: string;
  className?: string;
}

export function DataWipeControls({ sessionId, className }: DataWipeControlsProps) {
  const [dataCategories, setDataCategories] = useState<DataCategory[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [wipeProgress, setWipeProgress] = useState<WipeProgress[]>([]);
  const [isWiping, setIsWiping] = useState(false);
  const [confirmationRequired, setConfirmationRequired] = useState(false);
  const [lastScan, setLastScan] = useState<number | null>(null);

  useEffect(() => {
    if (sessionId) {
      scanDataCategories();
    }
  }, [sessionId]);

  const scanDataCategories = async () => {
    setIsLoading(true);

    try {
      const response = await fetch(`/api/security/incognito/${sessionId}/data-scan`);
      if (response.ok) {
        const data = await response.json();
        setDataCategories(
          data.categories.map((cat: any) => ({
            ...cat,
            selected: true, // Default to selecting all for wiping
            icon: getCategoryIcon(cat.id),
          })),
        );
        setLastScan(Date.now());
      }
    } catch (error) {
      console.error("Failed to scan data categories:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const getCategoryIcon = (categoryId: string): React.ReactNode => {
    switch (categoryId) {
      case "documents":
        return <FileText className="h-4 w-4" />;
      case "images":
        return <Image className="h-4 w-4" />;
      case "downloads":
        return <Download className="h-4 w-4" />;
      case "database":
        return <Database className="h-4 w-4" />;
      case "cache":
        return <HardDrive className="h-4 w-4" />;
      default:
        return <FileText className="h-4 w-4" />;
    }
  };

  const handleCategoryToggle = (categoryId: string, checked: boolean) => {
    setDataCategories((prev) =>
      prev.map((cat) => (cat.id === categoryId ? { ...cat, selected: checked } : cat)),
    );
  };

  const handleSelectAll = (checked: boolean) => {
    setDataCategories((prev) => prev.map((cat) => ({ ...cat, selected: checked })));
  };

  const handleWipeSelected = async () => {
    const selectedCategories = dataCategories.filter((cat) => cat.selected);

    if (selectedCategories.length === 0) {
      return;
    }

    // Check if any sensitive data is selected
    const hasSensitive = selectedCategories.some((cat) => cat.sensitive);
    if (hasSensitive && !confirmationRequired) {
      setConfirmationRequired(true);
      return;
    }

    setIsWiping(true);
    setWipeProgress(
      selectedCategories.map((cat) => ({
        category: cat.id,
        progress: 0,
        completed: false,
      })),
    );

    try {
      for (const category of selectedCategories) {
        await wipeCategory(category);
      }

      // Refresh data after wiping
      await scanDataCategories();
    } catch (error) {
      console.error("Wipe operation failed:", error);
    } finally {
      setIsWiping(false);
      setConfirmationRequired(false);
    }
  };

  const wipeCategory = async (category: DataCategory) => {
    const response = await fetch(`/api/security/data-wipe/${category.id}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sessionId,
        secure: category.sensitive,
        overwritePasses: category.sensitive ? 3 : 1,
      }),
    });

    if (!response.ok) {
      setWipeProgress((prev) =>
        prev.map((p) =>
          p.category === category.id ? { ...p, error: "Failed to wipe category" } : p,
        ),
      );
      return;
    }

    // Simulate progress updates (in real implementation, this would come from WebSocket)
    for (let progress = 0; progress <= 100; progress += 10) {
      await new Promise((resolve) => setTimeout(resolve, 100));
      setWipeProgress((prev) =>
        prev.map((p) =>
          p.category === category.id ? { ...p, progress, completed: progress === 100 } : p,
        ),
      );
    }
  };

  const formatSize = (bytes: number): string => {
    const mb = bytes / (1024 * 1024);
    if (mb < 1) {
      return `${(bytes / 1024).toFixed(1)} KB`;
    }
    return `${mb.toFixed(1)} MB`;
  };

  const formatLastAccessed = (timestamp: number): string => {
    const now = Date.now();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return "Just now";
  };

  const selectedCategories = dataCategories.filter((cat) => cat.selected);
  const totalSelectedSize = selectedCategories.reduce((sum, cat) => sum + cat.size, 0);
  const totalSelectedFiles = selectedCategories.reduce((sum, cat) => sum + cat.fileCount, 0);
  const hasSensitiveSelected = selectedCategories.some((cat) => cat.sensitive);

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Trash2 className="h-5 w-5" />
            <CardTitle>Data Wipe Controls</CardTitle>
          </div>
          <div className="flex items-center gap-2">
            {lastScan && (
              <span className="text-sm text-muted-foreground">
                Last scan: {new Date(lastScan).toLocaleTimeString()}
              </span>
            )}
            <Button
              variant="outline"
              size="sm"
              onClick={scanDataCategories}
              disabled={isLoading || isWiping}
            >
              Rescan
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Warning Alert */}
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            Data wiping is irreversible. Sensitive data will be securely overwritten multiple times.
            Ensure you have exported any needed information before proceeding.
          </AlertDescription>
        </Alert>

        {/* Data Categories */}
        {isLoading ? (
          <div className="text-center py-8">
            <div className="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4" />
            <p className="text-muted-foreground">Scanning data categories...</p>
          </div>
        ) : dataCategories.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">No data found to wipe</div>
        ) : (
          <div className="space-y-4">
            {/* Select All */}
            <div className="flex items-center justify-between p-3 border rounded-lg">
              <div className="flex items-center gap-3">
                <Checkbox
                  checked={dataCategories.every((cat) => cat.selected)}
                  onCheckedChange={handleSelectAll}
                />
                <span className="font-medium">Select All Categories</span>
              </div>
              <div className="text-sm text-muted-foreground">
                {selectedCategories.length} of {dataCategories.length} selected
              </div>
            </div>

            {/* Category List */}
            <div className="space-y-2">
              {dataCategories.map((category) => (
                <div
                  key={category.id}
                  className={`p-4 border rounded-lg ${category.selected ? "bg-blue-50 dark:bg-blue-950/20" : ""}`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-3">
                      <Checkbox
                        checked={category.selected}
                        onCheckedChange={(checked) =>
                          handleCategoryToggle(category.id, checked as boolean)
                        }
                      />
                      <div className="flex items-center gap-2">
                        {category.icon}
                        <span className="font-medium">{category.name}</span>
                        {category.sensitive && (
                          <Badge variant="destructive" className="text-xs">
                            Sensitive
                          </Badge>
                        )}
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium">{formatSize(category.size)}</p>
                      <p className="text-xs text-muted-foreground">{category.fileCount} files</p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-sm text-muted-foreground">
                    <p>{category.description}</p>
                    <div className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      <span>{formatLastAccessed(category.lastAccessed)}</span>
                    </div>
                  </div>

                  {/* Progress for active wipes */}
                  {isWiping && category.selected && (
                    <div className="mt-3">
                      {wipeProgress.map((progress) =>
                        progress.category === category.id ? (
                          <div key={progress.category} className="space-y-2">
                            <div className="flex justify-between text-sm">
                              <span>Wiping...</span>
                              <span>{progress.progress}%</span>
                            </div>
                            <Progress value={progress.progress} />
                            {progress.error && (
                              <p className="text-sm text-red-600">{progress.error}</p>
                            )}
                          </div>
                        ) : null,
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Summary */}
        {selectedCategories.length > 0 && (
          <div className="p-4 bg-gray-50 dark:bg-gray-900/20 rounded-lg">
            <h4 className="font-medium mb-2">Wipe Summary</h4>
            <div className="grid grid-cols-3 gap-4 text-sm">
              <div>
                <p className="text-muted-foreground">Categories</p>
                <p className="font-medium">{selectedCategories.length}</p>
              </div>
              <div>
                <p className="text-muted-foreground">Total Size</p>
                <p className="font-medium">{formatSize(totalSelectedSize)}</p>
              </div>
              <div>
                <p className="text-muted-foreground">Total Files</p>
                <p className="font-medium">{totalSelectedFiles}</p>
              </div>
            </div>
          </div>
        )}

        {/* Confirmation Dialog */}
        {confirmationRequired && (
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>
              You are about to wipe sensitive data. This action cannot be undone. Are you sure you
              want to proceed?
            </AlertDescription>
            <div className="flex gap-2 mt-3">
              <Button
                variant="destructive"
                size="sm"
                onClick={handleWipeSelected}
                disabled={isWiping}
              >
                Confirm Wipe
              </Button>
              <Button variant="outline" size="sm" onClick={() => setConfirmationRequired(false)}>
                Cancel
              </Button>
            </div>
          </Alert>
        )}

        {/* Action Buttons */}
        <div className="flex gap-2">
          <Button
            variant="destructive"
            onClick={handleWipeSelected}
            disabled={selectedCategories.length === 0 || isWiping}
            className="flex items-center gap-2"
          >
            <Trash2 className="h-4 w-4" />
            {isWiping ? "Wiping..." : `Wipe Selected (${selectedCategories.length})`}
          </Button>

          {hasSensitiveSelected && (
            <Badge variant="destructive" className="self-center">
              Contains sensitive data
            </Badge>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
