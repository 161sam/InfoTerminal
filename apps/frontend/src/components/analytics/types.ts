// Analytics types for OSINT data analysis
export interface AnalyticsFilters {
  timeRange: string;
  entityTypes: string[];
  sources: string[];
  tags: string[];
  collections: string[];
  workflows: string[];
  dateRange?: {
    from: string;
    to: string;
  };
  bbox?: [number, number, number, number]; // [minLng, minLat, maxLng, maxLat]
  confidence?: number;
}

export interface TimeRange {
  value: string;
  label: string;
  days?: number;
}

// Entity Analytics
export interface EntityStats {
  totalEntities: number;
  newEntities: number;
  entityTypes: EntityTypeCount[];
  topEntities: TopEntity[];
  relationshipDensity: number;
  trends: EntityTrend[];
}

export interface EntityTypeCount {
  type: string;
  count: number;
  percentage: number;
  color?: string;
}

export interface TopEntity {
  id: string;
  name: string;
  type: string;
  mentions: number;
  confidence: number;
  lastSeen: string;
  sources: number;
}

export interface EntityTrend {
  date: string;
  count: number;
  type?: string;
}

// Source Coverage
export interface SourceCoverage {
  totalSources: number;
  activeSources: number;
  sourceTypes: SourceTypeCount[];
  topSources: TopSource[];
  coverage: CoverageMetric[];
  timeline: SourceTimeline[];
}

export interface SourceTypeCount {
  type: string;
  count: number;
  percentage: number;
  active: number;
}

export interface TopSource {
  id: string;
  name: string;
  domain: string;
  type: string;
  documents: number;
  lastUpdated: string;
  reliability: number;
}

export interface CoverageMetric {
  category: string;
  coverage: number;
  target: number;
  status: "good" | "warning" | "critical";
}

export interface SourceTimeline {
  date: string;
  sources: number;
  documents: number;
  newSources: number;
}

// Evidence Quality
export interface EvidenceQuality {
  overallScore: number;
  totalClaims: number;
  verifiedClaims: number;
  qualityMetrics: QualityMetric[];
  sourceReliability: SourceReliability[];
  corroborationStats: CorroborationStats;
  recommendations: QualityRecommendation[];
}

export interface QualityMetric {
  name: string;
  score: number;
  weight: number;
  description: string;
  status: "good" | "warning" | "poor";
}

export interface SourceReliability {
  source: string;
  reliability: number;
  claimsCount: number;
  verificationRate: number;
  category: string;
}

export interface CorroborationStats {
  averageSources: number;
  independentSources: number;
  crossReferences: number;
  conflictingClaims: number;
}

export interface QualityRecommendation {
  type: string;
  priority: "high" | "medium" | "low";
  message: string;
  action?: string;
}

// Workflow Runs
export interface WorkflowRun {
  id: string;
  name: string;
  type: string;
  status: "running" | "completed" | "failed" | "cancelled";
  startTime: string;
  endTime?: string;
  duration?: number;
  input: WorkflowInput;
  output?: WorkflowOutput;
  entities: string[];
  claims: string[];
  error?: string;
}

export interface WorkflowInput {
  query?: string;
  entities?: string[];
  parameters?: Record<string, any>;
}

export interface WorkflowOutput {
  entities: number;
  relationships: number;
  documents: number;
  claims: number;
  confidence: number;
  artifacts?: string[];
}

// Timeline
export interface TimelineEvent {
  id: string;
  timestamp: string;
  type: "document" | "entity" | "claim" | "relationship";
  title: string;
  description: string;
  entities: string[];
  source: string;
  confidence: number;
  metadata?: Record<string, any>;
}

export interface TimelineData {
  events: TimelineEvent[];
  summary: TimelineSummary;
  clusters: TimelineCluster[];
}

export interface TimelineSummary {
  totalEvents: number;
  timeSpan: string;
  peakPeriod: string;
  categories: Record<string, number>;
}

export interface TimelineCluster {
  id: string;
  label: string;
  events: string[];
  timeRange: { start: string; end: string };
  significance: number;
}

// Geospatial
export interface GeoEntity {
  id: string;
  name: string;
  type: string;
  latitude: number;
  longitude: number;
  confidence: number;
  mentions: number;
  sources: number;
  metadata?: {
    country?: string;
    region?: string;
    address?: string;
    accuracy?: string;
  };
}

export interface GeoAnalytics {
  entities: GeoEntity[];
  clusters: GeoCluster[];
  heatmap: HeatmapPoint[];
  coverage: GeoCoverage;
}

export interface GeoCluster {
  id: string;
  center: [number, number];
  radius: number;
  entities: string[];
  significance: number;
}

export interface HeatmapPoint {
  latitude: number;
  longitude: number;
  intensity: number;
  count: number;
}

export interface GeoCoverage {
  countries: number;
  regions: number;
  cities: number;
  coverage: CountryCoverage[];
}

export interface CountryCoverage {
  country: string;
  code: string;
  entities: number;
  confidence: number;
}

// Query Insights
export interface QueryInsights {
  totalQueries: number;
  uniqueQueries: number;
  topQueries: TopQuery[];
  searchPatterns: SearchPattern[];
  clickthrough: ClickthroughStats;
  performance: QueryPerformance;
}

export interface TopQuery {
  query: string;
  count: number;
  averageResults: number;
  clickthrough: number;
  lastUsed: string;
}

export interface SearchPattern {
  pattern: string;
  category: string;
  frequency: number;
  effectiveness: number;
}

export interface ClickthroughStats {
  averageRate: number;
  topResults: number;
  documentTypes: Record<string, number>;
}

export interface QueryPerformance {
  averageResponseTime: number;
  slowQueries: SlowQuery[];
  errorRate: number;
}

export interface SlowQuery {
  query: string;
  responseTime: number;
  timestamp: string;
}

// Dossier Export
export interface AnalyticsDossierSection {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  data?: any;
}

export interface AnalyticsDossierExport {
  title: string;
  description: string;
  templateId?: string;
  format?: "markdown" | "pdf" | "html";
  includeMetadata?: boolean;
  filters: AnalyticsFilters;
  sections: AnalyticsDossierSection[];
  metadata: {
    generatedAt: string;
    generatedBy: string;
    version: string;
    caseId?: string;
    templateId?: string;
    format?: "markdown" | "pdf" | "html";
  };
}

// UI State
export interface AnalyticsState {
  filters: AnalyticsFilters;
  loading: Record<string, boolean>;
  errors: Record<string, string | null>;
  data: {
    entities?: EntityStats;
    sources?: SourceCoverage;
    evidence?: EvidenceQuality;
    workflows?: WorkflowRun[];
    timeline?: TimelineData;
    geo?: GeoAnalytics;
    insights?: QueryInsights;
    graph?: any;
  };
}

// Constants
export const TIME_RANGES: TimeRange[] = [
  { value: "1h", label: "Last Hour" },
  { value: "24h", label: "Last 24 Hours", days: 1 },
  { value: "7d", label: "Last 7 Days", days: 7 },
  { value: "30d", label: "Last 30 Days", days: 30 },
  { value: "90d", label: "Last 90 Days", days: 90 },
  { value: "1y", label: "Last Year", days: 365 },
  { value: "custom", label: "Custom Range" },
];

export const ENTITY_TYPES = [
  "Person",
  "Organization",
  "Location",
  "Email",
  "Domain",
  "Phone",
  "URL",
  "Date",
  "Money",
  "Document",
] as const;

export const SOURCE_TYPES = [
  "Web",
  "Document",
  "Social",
  "News",
  "Academic",
  "Government",
  "Database",
  "API",
] as const;

export const WORKFLOW_TYPES = [
  "Investigation",
  "Verification",
  "Entity Resolution",
  "Relationship Analysis",
  "Source Discovery",
  "Data Enrichment",
] as const;
