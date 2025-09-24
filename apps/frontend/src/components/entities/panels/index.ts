// Entity panels index - export all components
export { EntityStatsPanel } from "./EntityStatsPanel";
export { EntitySearchPanel } from "./EntitySearchPanel";
export { EntitySidebar } from "./EntitySidebar";
export { EntityTable } from "./EntityTable";
export { EntityCard } from "./EntityCard";
export { EntityDetailPanel } from "./EntityDetailPanel";

// Re-export types and utilities
export type {
  Entity,
  EntityStats,
  EntityFilter,
  SortConfig,
  RiskLevel,
} from "@/lib/entities/entity-config";

export {
  ENTITY_TYPE_ICONS,
  RISK_LEVELS,
  calculateEntityStats,
  getRiskColor,
  MOCK_ENTITIES,
} from "@/lib/entities/entity-config";
