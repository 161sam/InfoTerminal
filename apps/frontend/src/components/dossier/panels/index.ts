// Dossier panels index - export all components
export { DossierTemplateSelector } from "./DossierTemplateSelector";
export { DossierItemManager } from "./DossierItemManager";
export { DossierSettingsPanel } from "./DossierSettingsPanel";
export { DossierExportPanel } from "./DossierExportPanel";
export { DossierPreviewPanel } from "./DossierPreviewPanel";

// Re-export types and utilities
export type {
  DossierItem,
  DossierTemplate,
  DossierSettings,
  GeneratedDossier,
  DossierExportOptions,
  DossierGenerationPayload,
} from "@/lib/dossier/dossier-config";

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
  estimateDossierSize,
} from "@/lib/dossier/dossier-config";
