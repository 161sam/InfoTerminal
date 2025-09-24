// Modularized Entity Management Page
import { useState, useEffect, useMemo } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import {
  EntityStatsPanel,
  EntitySearchPanel,
  EntitySidebar,
  EntityTable,
  EntityDetailPanel,
  Entity,
  EntityFilter,
  SortConfig,
  calculateEntityStats,
  MOCK_ENTITIES,
} from "@/components/entities/panels";

export default function EntitiesPage() {
  // State management
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

  const [sortConfig, setSortConfig] = useState<SortConfig>({
    key: "mentions",
    direction: "desc",
  });

  // Computed values
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

  // Event handlers
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
        setSelectedEntity(entity);
        setShowDetailPanel(true);
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

  const handleEntityUpdate = (updatedEntity: Entity) => {
    setEntities((prev) => prev.map((e) => (e.id === updatedEntity.id ? updatedEntity : e)));
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

  const updateFilterField = (key: keyof EntityFilter, value: string) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  return (
    <DashboardLayout title="Entity Management" subtitle="Discover and manage detected entities">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Stats Overview */}
        <EntityStatsPanel stats={entityStats} />

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Main Content */}
          <div className={`space-y-6 ${showDetailPanel ? "lg:col-span-2" : "lg:col-span-3"}`}>
            {/* Search and Controls */}
            <EntitySearchPanel
              filters={filters}
              onFiltersChange={setFilters}
              sortConfig={sortConfig}
              onSort={handleSort}
              onClearFilters={clearFilters}
              onExport={exportEntities}
              onCreateEntity={() => setShowCreateModal(true)}
              resultsCount={sortedEntities.length}
              totalCount={entities.length}
            />

            {/* Entities Grid */}
            <EntityTable
              entities={sortedEntities}
              onEntityAction={handleEntityAction}
              isLoading={loading}
            />
          </div>

          {/* Sidebar */}
          <EntitySidebar entities={entities} filters={filters} onFilterChange={updateFilterField} />

          {/* Detail Panel */}
          {showDetailPanel && selectedEntity && (
            <div className="lg:col-span-1">
              <EntityDetailPanel
                entity={selectedEntity}
                onClose={() => {
                  setShowDetailPanel(false);
                  setSelectedEntity(null);
                }}
                onUpdate={handleEntityUpdate}
              />
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
