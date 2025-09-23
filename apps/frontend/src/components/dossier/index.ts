// Enhanced dossier components with analytics export support
export { DossierTemplateSelector } from './panels/DossierTemplateSelector';
export { DossierItemManager } from './panels/DossierItemManager';
export { DossierSettingsPanel } from './panels/DossierSettingsPanel';
export { DossierExportPanel } from './panels/DossierExportPanel';
export { DossierPreviewPanel } from './panels/DossierPreviewPanel';
export { default as DossierBuilderModal } from './DossierBuilderModal';

// Re-export types and utilities
export type {
  DossierItem,
  DossierTemplate,
  DossierSettings,
  GeneratedDossier,
  DossierExportOptions,
  DossierGenerationPayload
} from '@/lib/dossier/dossier-config';

export {
  ITEM_TYPE_COLORS,
  ITEM_TYPE_LABELS,
  LANGUAGE_OPTIONS,
  CONFIDENCE_LEVELS,
  DOSSIER_TEMPLATES,
  EXAMPLE_ITEMS,
  formatFileSize,
  getItemTypeColor,
  getItemTypeLabel,
  getConfidenceColor,
  formatConfidence,
  createDossierPayload,
  validateDossierItems,
  estimateDossierSize
} from '@/lib/dossier/dossier-config';

// Analytics export functionality
export { 
  analyticsDossierExporter,
  AnalyticsDossierExporter 
} from '@/lib/dossier/analytics-export';

export type { 
  DossierExportOptions as AnalyticsDossierExportOptions,
  ExportResult as AnalyticsExportResult 
} from '@/lib/dossier/analytics-export';
