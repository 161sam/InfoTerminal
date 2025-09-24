// Enhanced version of apps/frontend/pages/entities.tsx - Entity Management Page

import { useState, useEffect, useMemo } from "react";
import {
  User,
  Building2,
  MapPin,
  Mail,
  Globe,
  Network,
  Search,
  Filter,
  Download,
  Eye,
  Edit,
  Trash2,
  Plus,
  TrendingUp,
  Calendar,
  BarChart3,
  Target,
  Zap,
  AlertCircle,
  CheckCircle2,
  Clock,
  ArrowUpDown,
  ExternalLink,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import { DataTable, Column, TableAction } from "@/components/ui/DataTable";
import EntityBadge from "@/components/entities/EntityBadge";
import { EntityLabel, normalizeLabel } from "@/lib/entities";

interface Entity {
  id: string;
  name: string;
  type: EntityLabel;
  mentions: number;
  confidence: number;
  firstSeen: string;
  lastSeen: string;
  sources: string[];
  verified: boolean;
  description?: string;
  aliases?: string[];
  connections?: number;
  riskScore?: number;
  tags?: string[];
}

interface EntityStats {
  total: number;
  verified: number;
  pending: number;
  highRisk: number;
  newToday: number;
  totalConnections: number;
}

interface EntityFilter {
  type: string;
  verified: string;
  riskLevel: string;
  dateRange: string;
  minMentions: number;
  searchTerm: string;
}

const MOCK_ENTITIES: Entity[] = [
  {
    id: "1",
    name: "John Smith",
    type: "Person",
    mentions: 156,
    confidence: 0.95,
    firstSeen: "2024-01-15",
    lastSeen: "2024-03-01",
    sources: ["document-1", "document-5", "document-12"],
    verified: true,
    description: "Senior executive at ACME Corporation",
    aliases: ["J. Smith", "John S."],
    connections: 23,
    riskScore: 2,
    tags: ["executive", "finance"],
  },
  {
    id: "2",
    name: "ACME Corporation",
    type: "Organization",
    mentions: 243,
    confidence: 0.98,
    firstSeen: "2024-01-10",
    lastSeen: "2024-03-02",
    sources: ["document-2", "document-3", "document-8", "document-15"],
    verified: true,
    description: "Global technology company",
    connections: 45,
    riskScore: 1,
    tags: ["technology", "public-company"],
  },
  {
    id: "3",
    name: "London",
    type: "Location",
    mentions: 89,
    confidence: 0.92,
    firstSeen: "2024-01-20",
    lastSeen: "2024-02-28",
    sources: ["document-4", "document-9"],
    verified: false,
    description: "Capital city of the United Kingdom",
    connections: 12,
    riskScore: 0,
    tags: ["city", "europe"],
  },
  {
    id: "4",
    name: "john.smith@acme.com",
    type: "Email",
    mentions: 67,
    confidence: 0.99,
    firstSeen: "2024-02-01",
    lastSeen: "2024-03-01",
    sources: ["document-1", "document-6", "document-11"],
    verified: false,
    connections: 8,
    riskScore: 1,
    tags: ["contact"],
  },
  {
    id: "5",
    name: "acme.com",
    type: "Domain",
    mentions: 45,
    confidence: 0.87,
    firstSeen: "2024-01-25",
    lastSeen: "2024-02-29",
    sources: ["document-2", "document-7"],
    verified: true,
    connections: 15,
    riskScore: 0,
    tags: ["website", "corporate"],
  },
  // Add more mock data for variety
  {
    id: "6",
    name: "suspicious.example.com",
    type: "Domain",
    mentions: 12,
    confidence: 0.75,
    firstSeen: "2024-02-28",
    lastSeen: "2024-03-01",
    sources: ["document-20"],
    verified: false,
    description: "Domain flagged for suspicious activity",
    connections: 3,
    riskScore: 8,
    tags: ["suspicious", "flagged"],
  },
];

const ENTITY_TYPE_ICONS: Record<EntityLabel, LucideIcon> = {
  Person: User,
  Organization: Building2,
  Location: MapPin,
  Email: Mail,
  Domain: Globe,
  IP: Network,
  Misc: ExternalLink,
};

const RISK_LEVELS = [
  { value: "all", label: "All Levels", color: "gray" },
  { value: "low", label: "Low Risk (0-3)", color: "green" },
  { value: "medium", label: "Medium Risk (4-6)", color: "yellow" },
  { value: "high", label: "High Risk (7-10)", color: "red" },
];

function calculateEntityStats(entities: Entity[]): EntityStats {
  return {
    total: entities.length,
    verified: entities.filter((e) => e.verified).length,
    pending: entities.filter((e) => !e.verified).length,
    highRisk: entities.filter((e) => (e.riskScore || 0) >= 7).length,
    newToday: entities.filter((e) => {
      const today = new Date().toDateString();
      return new Date(e.firstSeen).toDateString() === today;
    }).length,
    totalConnections: entities.reduce((sum, e) => sum + (e.connections || 0), 0),
  };
}

function getRiskColor(score: number): string {
  if (score >= 7) return "text-red-600 bg-red-100";
  if (score >= 4) return "text-yellow-600 bg-yellow-100";
  return "text-green-600 bg-green-100";
}

export default function EntitiesPage() {
  const [entities, setEntities] = useState<Entity[]>(MOCK_ENTITIES);
  const [loading, setLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedEntity, setSelectedEntity] = useState<Entity | null>(null);
  const [showDetailPanel, setShowDetailPanel] = useState(false);

  const [filters, setFilters] = useState<EntityFilter>({
    type: "all",
    verified: "all",
    riskLevel: "all",
    dateRange: "all",
    minMentions: 0,
    searchTerm: "",
  });

  const [sortConfig, setSortConfig] = useState<{ key: string; direction: "asc" | "desc" }>({
    key: "mentions",
    direction: "desc",
  });

  const entityStats = useMemo(() => calculateEntityStats(entities), [entities]);

  const filteredEntities = useMemo(() => {
    return entities.filter((entity) => {
      // Type filter
      if (filters.type !== "all" && entity.type !== filters.type) return false;

      // Verified filter
      if (filters.verified === "verified" && !entity.verified) return false;
      if (filters.verified === "pending" && entity.verified) return false;

      // Risk level filter
      if (filters.riskLevel !== "all") {
        const risk = entity.riskScore || 0;
        switch (filters.riskLevel) {
          case "low":
            if (risk > 3) return false;
            break;
          case "medium":
            if (risk < 4 || risk > 6) return false;
            break;
          case "high":
            if (risk < 7) return false;
            break;
        }
      }

      // Mentions filter
      if (entity.mentions < filters.minMentions) return false;

      // Search term filter
      if (filters.searchTerm) {
        const searchLower = filters.searchTerm.toLowerCase();
        if (
          !entity.name.toLowerCase().includes(searchLower) &&
          !entity.description?.toLowerCase().includes(searchLower) &&
          !(entity.aliases || []).some((alias) => alias.toLowerCase().includes(searchLower)) &&
          !(entity.tags || []).some((tag) => tag.toLowerCase().includes(searchLower))
        ) {
          return false;
        }
      }

      return true;
    });
  }, [entities, filters]);

  const sortedEntities = useMemo(() => {
    return [...filteredEntities].sort((a, b) => {
      const aValue = (a as any)[sortConfig.key];
      const bValue = (b as any)[sortConfig.key];

      if (aValue < bValue) return sortConfig.direction === "asc" ? -1 : 1;
      if (aValue > bValue) return sortConfig.direction === "asc" ? 1 : -1;
      return 0;
    });
  }, [filteredEntities, sortConfig]);

  const handleSort = (key: string) => {
    setSortConfig((prev) => ({
      key,
      direction: prev.key === key && prev.direction === "asc" ? "desc" : "asc",
    }));
  };

  const handleEntityAction = (entity: Entity, action: string) => {
    switch (action) {
      case "view":
        setSelectedEntity(entity);
        setShowDetailPanel(true);
        break;
      case "edit":
        // Open edit modal
        break;
      case "verify":
        setEntities((prev) => prev.map((e) => (e.id === entity.id ? { ...e, verified: true } : e)));
        break;
      case "delete":
        if (confirm(`Are you sure you want to delete "${entity.name}"?`)) {
          setEntities((prev) => prev.filter((e) => e.id !== entity.id));
        }
        break;
      case "graph":
        window.open(`/graphx?focus=${encodeURIComponent(entity.name)}`, "_blank");
        break;
    }
  };

  const exportEntities = () => {
    const exportData = {
      entities: filteredEntities,
      stats: entityStats,
      filters,
      exportedAt: new Date().toISOString(),
    };

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `entities-export-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const clearFilters = () => {
    setFilters({
      type: "all",
      verified: "all",
      riskLevel: "all",
      dateRange: "all",
      minMentions: 0,
      searchTerm: "",
    });
  };

  return (
    <DashboardLayout title="Entity Management" subtitle="Discover and manage detected entities">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Stats Overview */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-900/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-600 dark:text-blue-400 font-medium">Total</p>
                <p className="text-2xl font-bold text-blue-800 dark:text-blue-300">
                  {entityStats.total}
                </p>
              </div>
              <Target size={20} className="text-blue-500" />
            </div>
          </div>

          <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-900/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-600 dark:text-green-400 font-medium">Verified</p>
                <p className="text-2xl font-bold text-green-800 dark:text-green-300">
                  {entityStats.verified}
                </p>
              </div>
              <CheckCircle2 size={20} className="text-green-500" />
            </div>
          </div>

          <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-900/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-yellow-600 dark:text-yellow-400 font-medium">Pending</p>
                <p className="text-2xl font-bold text-yellow-800 dark:text-yellow-300">
                  {entityStats.pending}
                </p>
              </div>
              <Clock size={20} className="text-yellow-500" />
            </div>
          </div>

          <div className="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-900/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-red-600 dark:text-red-400 font-medium">High Risk</p>
                <p className="text-2xl font-bold text-red-800 dark:text-red-300">
                  {entityStats.highRisk}
                </p>
              </div>
              <AlertCircle size={20} className="text-red-500" />
            </div>
          </div>

          <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-900/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-purple-600 dark:text-purple-400 font-medium">
                  New Today
                </p>
                <p className="text-2xl font-bold text-purple-800 dark:text-purple-300">
                  {entityStats.newToday}
                </p>
              </div>
              <TrendingUp size={20} className="text-purple-500" />
            </div>
          </div>

          <div className="p-4 bg-indigo-50 dark:bg-indigo-900/20 rounded-lg border border-indigo-200 dark:border-indigo-900/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-indigo-600 dark:text-indigo-400 font-medium">
                  Connections
                </p>
                <p className="text-2xl font-bold text-indigo-800 dark:text-indigo-300">
                  {entityStats.totalConnections}
                </p>
              </div>
              <Network size={20} className="text-indigo-500" />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Main Content */}
          <div className={`space-y-6 ${showDetailPanel ? "lg:col-span-2" : "lg:col-span-3"}`}>
            {/* Search and Controls */}
            <Panel>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100">
                    Entity Explorer
                  </h3>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => setShowCreateModal(true)}
                      className="inline-flex items-center gap-2 px-3 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700"
                    >
                      <Plus size={14} />
                      Add Entity
                    </button>
                    <button
                      onClick={exportEntities}
                      className="inline-flex items-center gap-2 px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
                    >
                      <Download size={14} />
                      Export
                    </button>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="flex-1 relative">
                    <Search
                      className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
                      size={16}
                    />
                    <input
                      type="text"
                      placeholder="Search entities, descriptions, aliases..."
                      value={filters.searchTerm}
                      onChange={(e) =>
                        setFilters((prev) => ({ ...prev, searchTerm: e.target.value }))
                      }
                      className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                    />
                  </div>

                  <button
                    onClick={clearFilters}
                    className="px-3 py-2 text-sm text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200"
                  >
                    Clear Filters
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
                  <div>
                    <select
                      value={filters.type}
                      onChange={(e) => setFilters((prev) => ({ ...prev, type: e.target.value }))}
                      className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                    >
                      <option value="all">All Types</option>
                      <option value="Person">Person</option>
                      <option value="Organization">Organization</option>
                      <option value="Location">Location</option>
                      <option value="Email">Email</option>
                      <option value="Domain">Domain</option>
                    </select>
                  </div>

                  <div>
                    <select
                      value={filters.verified}
                      onChange={(e) =>
                        setFilters((prev) => ({ ...prev, verified: e.target.value }))
                      }
                      className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                    >
                      <option value="all">All Status</option>
                      <option value="verified">Verified</option>
                      <option value="pending">Pending</option>
                    </select>
                  </div>

                  <div>
                    <select
                      value={filters.riskLevel}
                      onChange={(e) =>
                        setFilters((prev) => ({ ...prev, riskLevel: e.target.value }))
                      }
                      className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                    >
                      {RISK_LEVELS.map((level) => (
                        <option key={level.value} value={level.value}>
                          {level.label}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <input
                      type="number"
                      min="0"
                      placeholder="Min mentions"
                      value={filters.minMentions || ""}
                      onChange={(e) =>
                        setFilters((prev) => ({
                          ...prev,
                          minMentions: parseInt(e.target.value) || 0,
                        }))
                      }
                      className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                    />
                  </div>

                  <div>
                    <select
                      value={sortConfig.key}
                      onChange={(e) => handleSort(e.target.value)}
                      className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                    >
                      <option value="mentions">Sort by Mentions</option>
                      <option value="confidence">Sort by Confidence</option>
                      <option value="name">Sort by Name</option>
                      <option value="lastSeen">Sort by Last Seen</option>
                      <option value="riskScore">Sort by Risk Score</option>
                    </select>
                  </div>
                </div>

                <div className="flex items-center justify-between text-sm text-gray-600 dark:text-slate-400">
                  <span>
                    Showing {sortedEntities.length} of {entities.length} entities
                  </span>
                  {(filters.searchTerm ||
                    filters.type !== "all" ||
                    filters.verified !== "all" ||
                    filters.riskLevel !== "all" ||
                    filters.minMentions > 0) && (
                    <span className="text-blue-600 dark:text-blue-400">Filters applied</span>
                  )}
                </div>
              </div>
            </Panel>

            {/* Entities Grid */}
            <div className="grid grid-cols-1 gap-4">
              {sortedEntities.map((entity) => (
                <EntityCard key={entity.id} entity={entity} onAction={handleEntityAction} />
              ))}

              {sortedEntities.length === 0 && (
                <div className="text-center py-12">
                  <User size={48} className="mx-auto text-gray-400 dark:text-slate-500 mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 dark:text-slate-100 mb-2">
                    No entities found
                  </h3>
                  <p className="text-gray-500 dark:text-slate-400">
                    {filters.searchTerm || filters.type !== "all"
                      ? "Try adjusting your search filters"
                      : "Upload documents to start detecting entities"}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Entity Type Distribution */}
            <Panel title="Entity Types">
              <div className="space-y-3">
                {Object.entries(
                  entities.reduce(
                    (acc, entity) => {
                      acc[entity.type] = (acc[entity.type] || 0) + 1;
                      return acc;
                    },
                    {} as Record<string, number>,
                  ),
                ).map(([type, count]) => {
                  const Icon = ENTITY_TYPE_ICONS[type as keyof typeof ENTITY_TYPE_ICONS] || User;
                  return (
                    <button
                      key={type}
                      onClick={() =>
                        setFilters((prev) => ({
                          ...prev,
                          type: type === filters.type ? "all" : type,
                        }))
                      }
                      className={`w-full flex items-center justify-between p-3 rounded-lg transition-colors ${
                        filters.type === type
                          ? "bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300"
                          : "hover:bg-gray-100 dark:hover:bg-gray-800"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <Icon size={18} />
                        <span className="font-medium">{type}</span>
                      </div>
                      <span className="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded-full">
                        {count}
                      </span>
                    </button>
                  );
                })}
              </div>
            </Panel>

            {/* Risk Distribution */}
            <Panel title="Risk Levels">
              <div className="space-y-2">
                {RISK_LEVELS.filter((level) => level.value !== "all").map((level) => {
                  const count = entities.filter((e) => {
                    const risk = e.riskScore || 0;
                    switch (level.value) {
                      case "low":
                        return risk <= 3;
                      case "medium":
                        return risk >= 4 && risk <= 6;
                      case "high":
                        return risk >= 7;
                      default:
                        return false;
                    }
                  }).length;

                  return (
                    <div key={level.value} className="flex items-center justify-between text-sm">
                      <span className="text-gray-700 dark:text-slate-300">{level.label}</span>
                      <span
                        className={`px-2 py-1 rounded text-xs ${
                          level.color === "green"
                            ? "bg-green-100 text-green-800"
                            : level.color === "yellow"
                              ? "bg-yellow-100 text-yellow-800"
                              : "bg-red-100 text-red-800"
                        }`}
                      >
                        {count}
                      </span>
                    </div>
                  );
                })}
              </div>
            </Panel>

            {/* Quick Actions */}
            <Panel title="Quick Actions">
              <div className="space-y-2">
                <button className="w-full text-left p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                  <div className="flex items-center gap-3">
                    <Zap size={16} className="text-blue-500" />
                    <div>
                      <div className="font-medium text-sm">Bulk Verify</div>
                      <div className="text-xs text-gray-500">Verify high-confidence entities</div>
                    </div>
                  </div>
                </button>

                <button className="w-full text-left p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                  <div className="flex items-center gap-3">
                    <BarChart3 size={16} className="text-green-500" />
                    <div>
                      <div className="font-medium text-sm">Generate Report</div>
                      <div className="text-xs text-gray-500">Create entity analysis report</div>
                    </div>
                  </div>
                </button>

                <button className="w-full text-left p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                  <div className="flex items-center gap-3">
                    <Network size={16} className="text-purple-500" />
                    <div>
                      <div className="font-medium text-sm">Network Analysis</div>
                      <div className="text-xs text-gray-500">Analyze entity relationships</div>
                    </div>
                  </div>
                </button>
              </div>
            </Panel>
          </div>

          {/* Detail Panel */}
          {showDetailPanel && selectedEntity && (
            <div className="lg:col-span-1">
              <EntityDetailPanel
                entity={selectedEntity}
                onClose={() => setShowDetailPanel(false)}
                onUpdate={(updatedEntity) => {
                  setEntities((prev) =>
                    prev.map((e) => (e.id === updatedEntity.id ? updatedEntity : e)),
                  );
                  setSelectedEntity(updatedEntity);
                }}
              />
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}

function EntityCard({
  entity,
  onAction,
}: {
  entity: Entity;
  onAction: (entity: Entity, action: string) => void;
}) {
  const Icon = ENTITY_TYPE_ICONS[entity.type] || User;

  return (
    <Panel className="hover:shadow-md transition-shadow">
      <div className="flex items-start gap-4">
        <div className="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
          <Icon size={24} className="text-gray-600 dark:text-slate-400" />
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between mb-2">
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-slate-100 mb-1">
                {entity.name}
              </h3>
              <div className="flex items-center gap-2 mb-2">
                <EntityBadge label={entity.type} size="sm" />
                <span
                  className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${
                    entity.verified
                      ? "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300"
                      : "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-slate-300"
                  }`}
                >
                  {entity.verified ? <CheckCircle2 size={12} /> : <Clock size={12} />}
                  {entity.verified ? "Verified" : "Pending"}
                </span>
                {entity.riskScore !== undefined && entity.riskScore > 0 && (
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(entity.riskScore)}`}
                  >
                    Risk: {entity.riskScore}/10
                  </span>
                )}
              </div>
            </div>

            <div className="flex items-center gap-1">
              <button
                onClick={() => onAction(entity, "view")}
                className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-slate-200 rounded"
              >
                <Eye size={16} />
              </button>
              <button
                onClick={() => onAction(entity, "graph")}
                className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-slate-200 rounded"
              >
                <Network size={16} />
              </button>
              <button
                onClick={() => onAction(entity, "edit")}
                className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-slate-200 rounded"
              >
                <Edit size={16} />
              </button>
            </div>
          </div>

          {entity.description && (
            <p className="text-sm text-gray-600 dark:text-slate-400 mb-2">{entity.description}</p>
          )}

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="text-gray-500 dark:text-slate-400">Mentions</span>
              <div className="font-semibold text-gray-900 dark:text-slate-100">
                {entity.mentions}
              </div>
            </div>
            <div>
              <span className="text-gray-500 dark:text-slate-400">Confidence</span>
              <div className="font-semibold text-gray-900 dark:text-slate-100">
                {Math.round(entity.confidence * 100)}%
              </div>
            </div>
            <div>
              <span className="text-gray-500 dark:text-slate-400">Sources</span>
              <div className="font-semibold text-gray-900 dark:text-slate-100">
                {entity.sources.length}
              </div>
            </div>
            <div>
              <span className="text-gray-500 dark:text-slate-400">Connections</span>
              <div className="font-semibold text-gray-900 dark:text-slate-100">
                {entity.connections || 0}
              </div>
            </div>
          </div>

          {entity.tags && entity.tags.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-1">
              {entity.tags.map((tag, index) => (
                <span
                  key={index}
                  className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full dark:bg-blue-900/30 dark:text-blue-300"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </Panel>
  );
}

function EntityDetailPanel({
  entity,
  onClose,
  onUpdate,
}: {
  entity: Entity;
  onClose: () => void;
  onUpdate: (entity: Entity) => void;
}) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedEntity, setEditedEntity] = useState(entity);

  const handleSave = () => {
    onUpdate(editedEntity);
    setIsEditing(false);
  };

  return (
    <Panel>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100">
            Entity Details
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-slate-200"
          >
            ×
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
              Name
            </label>
            {isEditing ? (
              <input
                type="text"
                value={editedEntity.name}
                onChange={(e) => setEditedEntity((prev) => ({ ...prev, name: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg"
              />
            ) : (
              <p className="text-gray-900 dark:text-slate-100">{entity.name}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
              Description
            </label>
            {isEditing ? (
              <textarea
                value={editedEntity.description || ""}
                onChange={(e) =>
                  setEditedEntity((prev) => ({ ...prev, description: e.target.value }))
                }
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg"
                rows={3}
              />
            ) : (
              <p className="text-gray-900 dark:text-slate-100">
                {entity.description || "No description"}
              </p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-500 dark:text-slate-400">Type</span>
              <div className="font-semibold text-gray-900 dark:text-slate-100">{entity.type}</div>
            </div>
            <div>
              <span className="text-gray-500 dark:text-slate-400">Verified</span>
              <div className={entity.verified ? "text-green-600" : "text-yellow-600"}>
                {entity.verified ? "Yes" : "Pending"}
              </div>
            </div>
            <div>
              <span className="text-gray-500 dark:text-slate-400">First Seen</span>
              <div className="font-semibold text-gray-900 dark:text-slate-100">
                {new Date(entity.firstSeen).toLocaleDateString()}
              </div>
            </div>
            <div>
              <span className="text-gray-500 dark:text-slate-400">Last Seen</span>
              <div className="font-semibold text-gray-900 dark:text-slate-100">
                {new Date(entity.lastSeen).toLocaleDateString()}
              </div>
            </div>
          </div>

          {entity.aliases && entity.aliases.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
                Aliases
              </label>
              <div className="flex flex-wrap gap-2">
                {entity.aliases.map((alias, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded-full"
                  >
                    {alias}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="flex gap-2">
            {isEditing ? (
              <>
                <button
                  onClick={handleSave}
                  className="px-3 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700"
                >
                  Save
                </button>
                <button
                  onClick={() => {
                    setIsEditing(false);
                    setEditedEntity(entity);
                  }}
                  className="px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
                >
                  Cancel
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={() => setIsEditing(true)}
                  className="px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 dark:bg-gray-800 dark:text-slate-300 dark:hover:bg-gray-700"
                >
                  Edit
                </button>
                <button
                  onClick={() =>
                    window.open(`/graphx?focus=${encodeURIComponent(entity.name)}`, "_blank")
                  }
                  className="px-3 py-2 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200"
                >
                  <ExternalLink size={14} className="inline mr-1" />
                  View in Graph
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </Panel>
  );
}
