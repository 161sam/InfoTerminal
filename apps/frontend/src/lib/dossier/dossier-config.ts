// Dossier creation types and configuration
export interface DossierItem {
  id: string;
  type: "document" | "entity" | "node" | "edge";
  value: string;
  metadata?: {
    title?: string;
    description?: string;
    confidence?: number;
    lastSeen?: string;
  };
}

export interface DossierTemplate {
  id: string;
  name: string;
  description: string;
  items: DossierItem[];
  settings: DossierSettings;
}

export interface DossierSettings {
  includeTimeline: boolean;
  includeSummary: boolean;
  includeVisualization: boolean;
  confidenceThreshold: number;
  dateRange?: { from: string; to: string };
  language: "en" | "de";
}

export interface GeneratedDossier {
  markdown: string;
  pdfUrl?: string;
  metadata: {
    title: string;
    generatedAt: string;
    itemCount: number;
    size: string;
  };
}

export interface DossierExportOptions {
  format: "markdown" | "pdf" | "html" | "docx";
  includeImages: boolean;
  includeMetadata: boolean;
  watermark?: string;
}

export interface DossierGenerationPayload {
  title: string;
  items: {
    docs: string[];
    nodes: string[];
    edges: string[];
  };
  options: {
    summary: boolean;
    timeline: boolean;
    visualization: boolean;
    confidence: number;
    language: string;
    dateRange?: { from: string; to: string };
  };
}

// Configuration constants
export const ITEM_TYPE_COLORS = {
  document: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
  entity: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
  node: "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300",
  edge: "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300",
} as const;

export const ITEM_TYPE_LABELS = {
  document: "Document",
  entity: "Entity",
  node: "Node",
  edge: "Relationship",
} as const;

export const LANGUAGE_OPTIONS = [
  { value: "en", label: "English" },
  { value: "de", label: "Deutsch" },
] as const;

export const CONFIDENCE_LEVELS = [
  { value: 0.5, label: "Low (50%)", color: "text-red-600" },
  { value: 0.7, label: "Medium (70%)", color: "text-yellow-600" },
  { value: 0.8, label: "High (80%)", color: "text-green-600" },
  { value: 0.9, label: "Very High (90%)", color: "text-green-700" },
] as const;

// Pre-defined templates
export const DOSSIER_TEMPLATES: DossierTemplate[] = [
  {
    id: "investigation",
    name: "Investigation Report",
    description: "Comprehensive investigation with entities and connections",
    items: [],
    settings: {
      includeTimeline: true,
      includeSummary: true,
      includeVisualization: true,
      confidenceThreshold: 0.8,
      language: "en",
    },
  },
  {
    id: "entity-profile",
    name: "Entity Profile",
    description: "Detailed profile for a specific person or organization",
    items: [],
    settings: {
      includeTimeline: true,
      includeSummary: false,
      includeVisualization: false,
      confidenceThreshold: 0.9,
      language: "en",
    },
  },
  {
    id: "network-analysis",
    name: "Network Analysis",
    description: "Focus on relationships and network connections",
    items: [],
    settings: {
      includeTimeline: false,
      includeSummary: true,
      includeVisualization: true,
      confidenceThreshold: 0.7,
      language: "en",
    },
  },
  {
    id: "financial-audit",
    name: "Financial Audit",
    description: "Financial analysis and transaction tracking",
    items: [],
    settings: {
      includeTimeline: true,
      includeSummary: true,
      includeVisualization: false,
      confidenceThreshold: 0.9,
      language: "en",
    },
  },
];

// Example items for demonstration
export const EXAMPLE_ITEMS: DossierItem[] = [
  {
    id: "1",
    type: "document",
    value: "financial-report-q3-2024.pdf",
    metadata: {
      title: "Q3 Financial Report",
      description: "Quarterly earnings report",
      lastSeen: "2024-03-01",
    },
  },
  {
    id: "2",
    type: "entity",
    value: "John Smith",
    metadata: {
      title: "John Smith",
      description: "CEO of ACME Corp",
      confidence: 0.95,
      lastSeen: "2024-03-01",
    },
  },
  {
    id: "3",
    type: "entity",
    value: "ACME Corporation",
    metadata: {
      title: "ACME Corporation",
      description: "Technology company",
      confidence: 0.98,
      lastSeen: "2024-03-02",
    },
  },
  {
    id: "4",
    type: "edge",
    value: "John Smith -> CEO_OF -> ACME Corporation",
    metadata: {
      title: "CEO Relationship",
      description: "Executive leadership connection",
      confidence: 0.99,
      lastSeen: "2024-03-01",
    },
  },
];

// Utility functions
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

export function getItemTypeColor(type: DossierItem["type"]): string {
  return ITEM_TYPE_COLORS[type] || ITEM_TYPE_COLORS.document;
}

export function getItemTypeLabel(type: DossierItem["type"]): string {
  return ITEM_TYPE_LABELS[type] || type;
}

export function getConfidenceColor(confidence: number): string {
  if (confidence >= 0.9) return "text-green-700 dark:text-green-400";
  if (confidence >= 0.8) return "text-green-600 dark:text-green-400";
  if (confidence >= 0.7) return "text-yellow-600 dark:text-yellow-400";
  return "text-red-600 dark:text-red-400";
}

export function formatConfidence(confidence: number): string {
  return `${Math.round(confidence * 100)}%`;
}

export function createDossierPayload(
  title: string,
  items: DossierItem[],
  settings: DossierSettings,
): DossierGenerationPayload {
  return {
    title,
    items: {
      docs: items.filter((i) => i.type === "document").map((i) => i.value),
      nodes: items.filter((i) => i.type === "node" || i.type === "entity").map((i) => i.value),
      edges: items.filter((i) => i.type === "edge").map((i) => i.value),
    },
    options: {
      summary: settings.includeSummary,
      timeline: settings.includeTimeline,
      visualization: settings.includeVisualization,
      confidence: settings.confidenceThreshold,
      language: settings.language,
      dateRange: settings.dateRange,
    },
  };
}

export function validateDossierItems(items: DossierItem[]): { isValid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (items.length === 0) {
    errors.push("At least one item is required");
  }

  const duplicateValues = items
    .map((item) => item.value)
    .filter((value, index, array) => array.indexOf(value) !== index);

  if (duplicateValues.length > 0) {
    errors.push(`Duplicate items found: ${duplicateValues.join(", ")}`);
  }

  const invalidItems = items.filter((item) => !item.value.trim());
  if (invalidItems.length > 0) {
    errors.push("Some items have empty values");
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

export function estimateDossierSize(items: DossierItem[], settings: DossierSettings): string {
  let baseSize = items.length * 1000; // ~1KB per item

  if (settings.includeSummary) baseSize += 5000;
  if (settings.includeTimeline) baseSize += 3000;
  if (settings.includeVisualization) baseSize += 10000;

  return formatFileSize(baseSize);
}
