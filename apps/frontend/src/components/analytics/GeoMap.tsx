// Geospatial map component for OSINT analytics
import React, { useState, useRef, useEffect } from "react";
import { Map, MapPin, Layers, Filter, Search, ZoomIn, ZoomOut, Maximize2 } from "lucide-react";
import { useGeoEntities } from "../../hooks/analytics";
import { AnalyticsFilters, GeoEntity, GeoCluster } from "./types";

interface GeoMapProps {
  filters: AnalyticsFilters;
  onEntityClick?: (entity: GeoEntity) => void;
  className?: string;
}

export function GeoMap({ filters, onEntityClick, className = "" }: GeoMapProps) {
  const { data, loading, error } = useGeoEntities(filters);
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const [selectedLayer, setSelectedLayer] = useState<"entities" | "heatmap" | "clusters">(
    "entities",
  );
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedEntity, setSelectedEntity] = useState<GeoEntity | null>(null);
  const [mapInstance, setMapInstance] = useState<any>(null);

  // Simple map state for demonstration (in real implementation, use Leaflet/MapLibre)
  const [mapCenter, setMapCenter] = useState<[number, number]>([40.7128, -74.006]); // NYC default
  const [mapZoom, setMapZoom] = useState(10);

  const calculateBounds = React.useCallback(
    (entities: GeoEntity[]) => {
      if (entities.length === 0) return { center: mapCenter };

      const lats = entities.map((e) => e.latitude);
      const lngs = entities.map((e) => e.longitude);

      const center: [number, number] = [
        (Math.max(...lats) + Math.min(...lats)) / 2,
        (Math.max(...lngs) + Math.min(...lngs)) / 2,
      ];

      return { center };
    },
    [mapCenter],
  );

  useEffect(() => {
    // Initialize map when component mounts
    // In real implementation: initialize Leaflet or MapLibre here
    if (mapContainerRef.current && !mapInstance) {
      // Mock map initialization
      console.log("Map would be initialized here with real mapping library");
    }
  }, [mapInstance]);

  useEffect(() => {
    // Update map when data changes
    if (data?.entities && data.entities.length > 0 && mapInstance) {
      // In real implementation: update map markers/layers
      const bounds = calculateBounds(data.entities);
      setMapCenter(bounds.center);
    }
  }, [data, mapInstance, calculateBounds]);

  if (loading) {
    return (
      <div
        className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}
      >
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4"></div>
          <div className="h-96 bg-gray-200 dark:bg-gray-700 rounded"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div
        className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 ${className}`}
      >
        <div className="flex items-center gap-2 text-red-600 dark:text-red-400">
          <Map size={20} />
          <span className="text-sm">Geospatial service unavailable. Showing empty state.</span>
        </div>
      </div>
    );
  }

  

  const filteredEntities =
    data?.entities.filter((entity) => {
      return (
        !searchQuery ||
        entity.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        entity.type.toLowerCase().includes(searchQuery.toLowerCase()) ||
        entity.metadata?.country?.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }) || [];

  const getEntityColor = (type: string) => {
    const colors: Record<string, string> = {
      Person: "#3b82f6",
      Organization: "#10b981",
      Location: "#f59e0b",
      Event: "#ef4444",
      Infrastructure: "#8b5cf6",
      Vehicle: "#06b6d4",
    };
    return colors[type] || "#6b7280";
  };

  const getConfidenceRadius = (confidence: number) => {
    return Math.max(3, Math.min(12, confidence * 15));
  };

  const handleZoomIn = () => {
    setMapZoom((prev) => Math.min(prev + 1, 18));
  };

  const handleZoomOut = () => {
    setMapZoom((prev) => Math.max(prev - 1, 1));
  };

  const handleLayerChange = (layer: "entities" | "heatmap" | "clusters") => {
    setSelectedLayer(layer);
    // In real implementation: update map layers
  };

  return (
    <div
      className={`bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden ${className}`}
    >
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Map size={20} className="text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Geospatial Analysis
            </h3>
          </div>

          {data && (
            <div className="text-xs text-gray-500 dark:text-gray-400">
              {filteredEntities.length} entities • {data.coverage.countries} countries
            </div>
          )}
        </div>

        {/* Controls */}
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="flex-1">
            <div className="relative">
              <Search
                size={16}
                className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
              />
              <input
                type="text"
                placeholder="Search locations..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              />
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Layers size={16} className="text-gray-400" />
            <select
              value={selectedLayer}
              onChange={(e) => handleLayerChange(e.target.value as any)}
              className="px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            >
              <option value="entities">Entities</option>
              <option value="heatmap">Heatmap</option>
              <option value="clusters">Clusters</option>
            </select>
          </div>
        </div>
      </div>

      {!data || filteredEntities.length === 0 ? (
        <div className="p-6 text-center">
          <Map size={48} className="mx-auto mb-4 text-gray-400" />
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            No geospatial data available for the selected filters.
          </p>
        </div>
      ) : (
        <div className="relative">
          {/* Map Container */}
          <div
            ref={mapContainerRef}
            className="h-96 bg-gray-100 dark:bg-gray-900 relative overflow-hidden"
          >
            {/* Mock Map Display - In real implementation, this would be the actual map */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <Map size={64} className="mx-auto mb-4 text-gray-400" />
                <p className="text-gray-500 dark:text-gray-400 text-sm">
                  Interactive map would be displayed here
                </p>
                <p className="text-xs text-gray-400 dark:text-gray-500 mt-2">
                  Layer: {selectedLayer} • {filteredEntities.length} entities • Zoom: {mapZoom}
                </p>
              </div>
            </div>

            {/* Map Controls */}
            <div className="absolute top-4 right-4 flex flex-col gap-2">
              <button
                onClick={handleZoomIn}
                className="w-8 h-8 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded shadow-sm hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center justify-center"
              >
                <ZoomIn size={16} />
              </button>
              <button
                onClick={handleZoomOut}
                className="w-8 h-8 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded shadow-sm hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center justify-center"
              >
                <ZoomOut size={16} />
              </button>
              <button className="w-8 h-8 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded shadow-sm hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center justify-center">
                <Maximize2 size={16} />
              </button>
            </div>
          </div>

          {/* Legend */}
          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-4 text-xs">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                <span>Person</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <span>Organization</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                <span>Location</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <span>Event</span>
              </div>
              <div className="text-gray-500 dark:text-gray-400 ml-auto">
                Size = Confidence • Color = Type
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Sidebar with entity list and details */}
      <div className="border-t border-gray-200 dark:border-gray-700">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-0">
          {/* Entity List */}
          <div className="p-4 border-r border-gray-200 dark:border-gray-700">
            <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
              Locations ({filteredEntities.length})
            </h4>
            <div className="max-h-64 overflow-y-auto space-y-2">
              {filteredEntities.slice(0, 20).map((entity) => (
                <div
                  key={entity.id}
                  className={`p-2 rounded-lg cursor-pointer transition-colors ${
                    selectedEntity?.id === entity.id
                      ? "bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800"
                      : "hover:bg-gray-50 dark:hover:bg-gray-900/50"
                  }`}
                  onClick={() => {
                    setSelectedEntity(entity);
                    onEntityClick?.(entity);
                  }}
                >
                  <div className="flex items-center gap-2">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: getEntityColor(entity.type) }}
                    />
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                        {entity.name}
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">
                        {entity.metadata?.country} • {entity.mentions} mentions
                      </div>
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      {Math.round(entity.confidence * 100)}%
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Coverage Stats */}
          <div className="p-4">
            <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">
              Geographic Coverage
            </h4>

            {data && (
              <div className="space-y-4">
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <div className="text-lg font-bold text-blue-600 dark:text-blue-400">
                      {data.coverage.countries}
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">Countries</div>
                  </div>
                  <div>
                    <div className="text-lg font-bold text-green-600 dark:text-green-400">
                      {data.coverage.regions}
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">Regions</div>
                  </div>
                  <div>
                    <div className="text-lg font-bold text-purple-600 dark:text-purple-400">
                      {data.coverage.cities}
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">Cities</div>
                  </div>
                </div>

                {/* Top Countries */}
                {data.coverage.coverage.length > 0 && (
                  <div>
                    <div className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Top Countries
                    </div>
                    <div className="space-y-2">
                      {data.coverage.coverage.slice(0, 5).map((country) => (
                        <div
                          key={country.code}
                          className="flex items-center justify-between text-xs"
                        >
                          <span className="text-gray-900 dark:text-gray-100">
                            {country.country}
                          </span>
                          <div className="flex items-center gap-2">
                            <span className="text-gray-600 dark:text-gray-400">
                              {country.entities}
                            </span>
                            <div className="w-12 bg-gray-200 dark:bg-gray-700 rounded-full h-1">
                              <div
                                className="bg-blue-500 h-1 rounded-full"
                                style={{ width: `${country.confidence * 100}%` }}
                              />
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Clusters Info */}
                {data.clusters.length > 0 && (
                  <div>
                    <div className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Geographic Clusters
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">
                      {data.clusters.length} clusters identified with avg{" "}
                      {Math.round(
                        data.clusters.reduce((sum, c) => sum + c.entities.length, 0) /
                          data.clusters.length,
                      )}{" "}
                      entities each
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default GeoMap;
