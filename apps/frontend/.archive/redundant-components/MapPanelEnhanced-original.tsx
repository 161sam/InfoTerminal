// Enhanced MapPanel with Geospatial Analytics for InfoTerminal
// Integrates with the new geospatial backend features

import React, { useEffect, useMemo, useState, useCallback } from "react";
import {
  MapContainer,
  TileLayer,
  GeoJSON,
  Marker,
  Popup,
  useMapEvents,
  useMap,
} from "react-leaflet";
import L from "leaflet";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Badge } from "./ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Switch } from "./ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "./ui/dialog";
import {
  Map,
  Search,
  Layers,
  MapPin,
  Filter,
  Download,
  RefreshCw,
  Settings,
  Crosshair,
  Navigation,
  BarChart3,
} from "lucide-react";
import config, { GRAPH_DEEPLINK_FALLBACK } from "@/lib/config";

// Fix for default markers
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

interface GeoEntity {
  node_id: string;
  name: string;
  latitude: number;
  longitude: number;
  labels: string[];
  distance_km?: number;
}

interface BoundingBox {
  south: number;
  west: number;
  north: number;
  east: number;
}

interface HeatmapPoint {
  latitude: number;
  longitude: number;
  intensity: number;
}

interface GeocodeResult {
  success: boolean;
  latitude?: number;
  longitude?: number;
  display_name?: string;
  address?: any;
  confidence?: number;
  error?: string;
}

interface GeoStatistics {
  total_nodes: number;
  geocoded_nodes: number;
  geocoding_percentage: number;
  node_types_with_coordinates: Array<{
    type: string;
    count: number;
  }>;
  geographic_bounds?: {
    min_latitude: number;
    max_latitude: number;
    min_longitude: number;
    max_longitude: number;
    center_latitude: number;
    center_longitude: number;
  };
}

// Component for drawing bounding box
const BoundingBoxDrawer: React.FC<{
  onBoundsChange: (bounds: BoundingBox | null) => void;
  enabled: boolean;
}> = ({ onBoundsChange, enabled }) => {
  const [drawing, setDrawing] = useState(false);
  const [startPoint, setStartPoint] = useState<L.LatLng | null>(null);
  const [currentBox, setCurrentBox] = useState<L.Rectangle | null>(null);

  const map = useMap();

  useMapEvents({
    mousedown: (e) => {
      if (!enabled) return;
      setDrawing(true);
      setStartPoint(e.latlng);
    },
    mousemove: (e) => {
      if (!drawing || !startPoint) return;

      if (currentBox) {
        map.removeLayer(currentBox);
      }

      const bounds = L.latLngBounds([startPoint, e.latlng]);
      const rectangle = L.rectangle(bounds, {
        color: "#3b82f6",
        fillColor: "#3b82f6",
        fillOpacity: 0.1,
        weight: 2,
      });
      rectangle.addTo(map);
      setCurrentBox(rectangle);
    },
    mouseup: (e) => {
      if (!drawing || !startPoint) return;

      const bounds = {
        south: Math.min(startPoint.lat, e.latlng.lat),
        west: Math.min(startPoint.lng, e.latlng.lng),
        north: Math.max(startPoint.lat, e.latlng.lat),
        east: Math.max(startPoint.lng, e.latlng.lng),
      };

      onBoundsChange(bounds);
      setDrawing(false);
      setStartPoint(null);
    },
  });

  useEffect(() => {
    if (!enabled && currentBox) {
      map.removeLayer(currentBox);
      setCurrentBox(null);
      onBoundsChange(null);
    }
  }, [enabled, currentBox, map, onBoundsChange]);

  return null;
};

interface EnhancedMapPanelProps {
  graphApiUrl?: string;
  viewsApiUrl?: string;
  className?: string;
}

export const EnhancedMapPanel: React.FC<EnhancedMapPanelProps> = ({
  graphApiUrl = "http://localhost:8612",
  viewsApiUrl = config.VIEWS_API,
  className = "",
}) => {
  // Original map state
  const [layers, setLayers] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [originalEntities, setOriginalEntities] = useState<any | null>(null);
  const [showEntities, setShowEntities] = useState<boolean>(true);

  // Enhanced geospatial state
  const [geoEntities, setGeoEntities] = useState<GeoEntity[]>([]);
  const [searchLocation, setSearchLocation] = useState("");
  const [geocodeResult, setGeocodeResult] = useState<GeocodeResult | null>(null);
  const [boundingBoxMode, setBoundingBoxMode] = useState(false);
  const [selectedBounds, setSelectedBounds] = useState<BoundingBox | null>(null);
  const [nearbySearch, setNearbySearch] = useState({ lat: 0, lng: 0, radius: 10 });
  const [heatmapData, setHeatmapData] = useState<HeatmapPoint[]>([]);
  const [geoStats, setGeoStats] = useState<GeoStatistics | null>(null);
  const [activeTab, setActiveTab] = useState("entities");
  const [showControls, setShowControls] = useState(true);

  // Map configuration
  const [mapCenter, setMapCenter] = useState<[number, number]>([51.505, -0.09]);
  const [mapZoom, setMapZoom] = useState(13);

  const loadOriginalData = useCallback(async () => {
    setLoading(true);
    try {
      const listUrl = `${viewsApiUrl}/geo/list`;
      const res = await fetch(listUrl);
      if (res.status === 404) {
        setLayers([]);
        setError(null);
        return;
      }
      if (!res.ok) throw new Error(`Failed to load geo list (${res.status})`);

      const data = await res.json();
      const items = data.items || data || [];
      const loaded: any[] = [];

      for (const f of items) {
        try {
          const r = await fetch(`${viewsApiUrl}/geo/get?name=${encodeURIComponent(f.name)}`);
          if (r.status === 404) continue;
          if (!r.ok) continue;
          loaded.push(await r.json());
        } catch {
          continue;
        }
      }

      setLayers(loaded);

      try {
        const entRes = await fetch(`${viewsApiUrl}/geo/entities`);
        if (entRes.ok) {
          setOriginalEntities(await entRes.json());
        }
      } catch {
        // ignore entity layer errors
      }

      setError(null);
    } catch (e: any) {
      setError(e.message || "Failed to load map data");
    } finally {
      setLoading(false);
    }
  }, [viewsApiUrl]);

  const fetchGeoEntities = useCallback(
    async (bounds?: BoundingBox) => {
      if (!bounds) return;

      try {
        const params = new URLSearchParams({
          south: bounds.south.toString(),
          west: bounds.west.toString(),
          north: bounds.north.toString(),
          east: bounds.east.toString(),
          limit: "100",
        });

        const response = await fetch(`${graphApiUrl}/geo/entities?${params}`);
        if (!response.ok) throw new Error("Failed to fetch geo entities");

        const data = await response.json();
        setGeoEntities(data.entities || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch entities");
      }
    },
    [graphApiUrl],
  );

  const fetchNearbyEntities = useCallback(
    async (lat: number, lng: number, radius: number) => {
      try {
        const response = await fetch(`${graphApiUrl}/geo/entities/nearby`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            latitude: lat,
            longitude: lng,
            radius_km: radius,
            limit: 50,
          }),
        });

        if (!response.ok) throw new Error("Failed to fetch nearby entities");

        const data = await response.json();
        setGeoEntities(data.entities || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch nearby entities");
      }
    },
    [graphApiUrl],
  );

  const geocodeLocation = useCallback(
    async (location: string) => {
      if (!location.trim()) return;

      try {
        const response = await fetch(`${graphApiUrl}/geo/geocode`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ location }),
        });

        if (!response.ok) throw new Error("Geocoding failed");

        const result = await response.json();
        setGeocodeResult(result);

        if (result.success && result.latitude && result.longitude) {
          setMapCenter([result.latitude, result.longitude]);
          setMapZoom(15);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Geocoding failed");
      }
    },
    [graphApiUrl],
  );

  const fetchHeatmapData = useCallback(
    async (bounds: BoundingBox) => {
      try {
        const params = new URLSearchParams({
          south: bounds.south.toString(),
          west: bounds.west.toString(),
          north: bounds.north.toString(),
          east: bounds.east.toString(),
          grid_size: "20",
        });

        const response = await fetch(`${graphApiUrl}/geo/heatmap?${params}`);
        if (!response.ok) throw new Error("Failed to fetch heatmap data");

        const data = await response.json();
        setHeatmapData(data.heatmap_points || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch heatmap data");
      }
    },
    [graphApiUrl],
  );

  const fetchGeoStatistics = useCallback(async () => {
    try {
      const response = await fetch(`${graphApiUrl}/geo/statistics`);
      if (!response.ok) throw new Error("Failed to fetch statistics");

      const data = await response.json();
      setGeoStats(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch statistics");
    }
  }, [graphApiUrl]);

  useEffect(() => {
    loadOriginalData();
    fetchGeoStatistics();
  }, [loadOriginalData, fetchGeoStatistics]);

  useEffect(() => {
    if (selectedBounds) {
      fetchGeoEntities(selectedBounds);
      if (activeTab === "heatmap") {
        fetchHeatmapData(selectedBounds);
      }
    }
  }, [selectedBounds, fetchGeoEntities, fetchHeatmapData, activeTab]);

  const handleMapClick = useCallback(
    (e: L.LeafletMouseEvent) => {
      if (activeTab === "nearby") {
        setNearbySearch({ lat: e.latlng.lat, lng: e.latlng.lng, radius: 10 });
        fetchNearbyEntities(e.latlng.lat, e.latlng.lng, 10);
      }
    },
    [activeTab, fetchNearbyEntities],
  );

  const createEntityIcon = (labels: string[]) => {
    const primaryLabel = labels[0] || "Unknown";
    const color =
      {
        Person: "#ef4444",
        Organization: "#3b82f6",
        Location: "#10b981",
        Event: "#f59e0b",
      }[primaryLabel] || "#6b7280";

    return L.divIcon({
      className: "custom-marker",
      html: `<div style="background: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
      iconSize: [20, 20],
      iconAnchor: [10, 10],
    });
  };

  const renderControls = () => (
    <Card className="absolute top-4 right-4 z-[1000] w-80">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">Geospatial Controls</CardTitle>
          <Button variant="ghost" size="sm" onClick={() => setShowControls(!showControls)}>
            <Settings className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>

      {showControls && (
        <CardContent className="space-y-4">
          {/* Search Location */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Search Location</label>
            <div className="flex gap-2">
              <Input
                value={searchLocation}
                onChange={(e) => setSearchLocation(e.target.value)}
                placeholder="Enter location name..."
                className="flex-1"
              />
              <Button size="sm" onClick={() => geocodeLocation(searchLocation)}>
                <Search className="h-4 w-4" />
              </Button>
            </div>
            {geocodeResult && geocodeResult.success && (
              <div className="text-xs text-green-600">Found: {geocodeResult.display_name}</div>
            )}
          </div>

          {/* Mode Selection */}
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid grid-cols-3 text-xs">
              <TabsTrigger value="entities">Entities</TabsTrigger>
              <TabsTrigger value="nearby">Nearby</TabsTrigger>
              <TabsTrigger value="heatmap">Heatmap</TabsTrigger>
            </TabsList>

            <TabsContent value="entities" className="mt-3 space-y-3">
              <div className="flex items-center space-x-2">
                <Switch
                  id="bbox-mode"
                  checked={boundingBoxMode}
                  onCheckedChange={setBoundingBoxMode}
                />
                <label htmlFor="bbox-mode" className="text-sm">
                  Draw bounding box
                </label>
              </div>

              {selectedBounds && (
                <div className="text-xs text-gray-600">
                  <div>Entities: {geoEntities.length}</div>
                  <div>
                    Bounds: {selectedBounds.south.toFixed(3)}, {selectedBounds.west.toFixed(3)} to{" "}
                    {selectedBounds.north.toFixed(3)}, {selectedBounds.east.toFixed(3)}
                  </div>
                </div>
              )}
            </TabsContent>

            <TabsContent value="nearby" className="mt-3 space-y-3">
              <div className="text-sm">Click on map to find nearby entities</div>
              <div>
                <label className="text-xs">Radius (km):</label>
                <Input
                  type="number"
                  value={nearbySearch.radius}
                  onChange={(e) =>
                    setNearbySearch((prev) => ({ ...prev, radius: Number(e.target.value) }))
                  }
                  min="1"
                  max="100"
                  className="mt-1"
                />
              </div>
            </TabsContent>

            <TabsContent value="heatmap" className="mt-3">
              <div className="text-sm">Draw bounding box to generate entity heatmap</div>
              {heatmapData.length > 0 && (
                <div className="text-xs text-gray-600">Heatmap points: {heatmapData.length}</div>
              )}
            </TabsContent>
          </Tabs>

          {/* Statistics */}
          {geoStats && (
            <div className="bg-gray-50 p-3 rounded text-xs">
              <div className="font-medium mb-2">Statistics</div>
              <div>Total nodes: {geoStats.total_nodes.toLocaleString()}</div>
              <div>
                Geocoded: {geoStats.geocoded_nodes.toLocaleString()} (
                {geoStats.geocoding_percentage.toFixed(1)}%)
              </div>
              <div>Node types: {geoStats.node_types_with_coordinates.length}</div>
            </div>
          )}

          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={loadOriginalData}>
              <RefreshCw className="h-4 w-4 mr-1" />
              Refresh
            </Button>
            <Button variant="outline" size="sm" onClick={fetchGeoStatistics}>
              <BarChart3 className="h-4 w-4 mr-1" />
              Stats
            </Button>
          </div>
        </CardContent>
      )}
    </Card>
  );

  const geojsonStyle = useMemo(
    () => ({
      color: "#3388ff",
      weight: 2,
      opacity: 0.8,
      fillOpacity: 0.3,
    }),
    [],
  );

  return (
    <div className={`relative w-full h-full ${className}`}>
      <MapContainer
        center={mapCenter}
        zoom={mapZoom}
        style={{ height: "100%", width: "100%" }}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Original GeoJSON layers */}
        {layers.map((layer, idx) => (
          <GeoJSON
            key={`layer-${idx}`}
            data={layer}
            style={geojsonStyle}
            onEachFeature={(feature, layer) => {
              if (feature.properties) {
                const popupContent = Object.entries(feature.properties)
                  .map(([key, value]) => `<strong>${key}:</strong> ${value}`)
                  .join("<br>");
                layer.bindPopup(`<div style="max-width: 200px;">${popupContent}</div>`);
              }
            }}
          />
        ))}

        {/* Enhanced geo entities */}
        {geoEntities.map((entity) => (
          <Marker
            key={entity.node_id}
            position={[entity.latitude, entity.longitude]}
            icon={createEntityIcon(entity.labels)}
          >
            <Popup>
              <div className="p-2 max-w-xs">
                <div className="font-medium">{entity.name || "Unnamed Entity"}</div>
                <div className="text-sm text-gray-600 mb-2">
                  {entity.latitude.toFixed(6)}, {entity.longitude.toFixed(6)}
                </div>
                <div className="flex flex-wrap gap-1 mb-2">
                  {entity.labels.map((label) => (
                    <Badge key={label} variant="secondary" className="text-xs">
                      {label}
                    </Badge>
                  ))}
                </div>
                {entity.distance_km && (
                  <div className="text-xs text-gray-500">
                    Distance: {entity.distance_km.toFixed(2)} km
                  </div>
                )}
                <Button
                  variant="link"
                  size="sm"
                  className="p-0 h-auto text-blue-600"
                  onClick={() => {
                    const url = `${GRAPH_DEEPLINK_FALLBACK}?focus=${encodeURIComponent(entity.node_id)}`;
                    window.open(url, "_blank");
                  }}
                >
                  View in Graph
                </Button>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Heatmap visualization */}
        {activeTab === "heatmap" &&
          heatmapData.map((point, idx) => {
            const intensity = Math.min(point.intensity / 10, 1); // Normalize intensity
            const radius = Math.max(5, point.intensity * 2);

            return (
              <Marker
                key={`heatmap-${idx}`}
                position={[point.latitude, point.longitude]}
                icon={L.divIcon({
                  className: "heatmap-marker",
                  html: `<div style="
                  background: rgba(255, 0, 0, ${intensity});
                  width: ${radius}px;
                  height: ${radius}px;
                  border-radius: 50%;
                  border: 1px solid rgba(255, 0, 0, 0.8);
                "></div>`,
                  iconSize: [radius, radius],
                  iconAnchor: [radius / 2, radius / 2],
                })}
              >
                <Popup>
                  <div>
                    <strong>Entity Density</strong>
                    <br />
                    Count: {point.intensity}
                    <br />
                    Location: {point.latitude.toFixed(4)}, {point.longitude.toFixed(4)}
                  </div>
                </Popup>
              </Marker>
            );
          })}

        {/* Geocode result marker */}
        {geocodeResult &&
          geocodeResult.success &&
          geocodeResult.latitude &&
          geocodeResult.longitude && (
            <Marker position={[geocodeResult.latitude, geocodeResult.longitude]}>
              <Popup>
                <div>
                  <strong>Search Result</strong>
                  <br />
                  {geocodeResult.display_name}
                  <br />
                  Confidence: {(geocodeResult.confidence || 0 * 100).toFixed(0)}%
                </div>
              </Popup>
            </Marker>
          )}

        {/* Bounding box drawer */}
        <BoundingBoxDrawer enabled={boundingBoxMode} onBoundsChange={setSelectedBounds} />

        {/* Map click handler for nearby search */}
        <MapClickHandler onClick={handleMapClick} />
      </MapContainer>

      {renderControls()}

      {error && (
        <div className="absolute bottom-4 left-4 bg-red-50 border border-red-200 text-red-700 px-3 py-2 rounded shadow-lg z-[1000]">
          {error}
        </div>
      )}

      {loading && (
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-4 rounded shadow-lg z-[1000]">
          <RefreshCw className="h-6 w-6 animate-spin mx-auto" />
          <div className="mt-2 text-sm">Loading map data...</div>
        </div>
      )}
    </div>
  );
};

// Helper component for map click events
const MapClickHandler: React.FC<{ onClick: (e: L.LeafletMouseEvent) => void }> = ({ onClick }) => {
  useMapEvents({
    click: onClick,
  });
  return null;
};

// Export both the original and enhanced versions
export default EnhancedMapPanel;

// Also export the original for backward compatibility
export { EnhancedMapPanel as MapPanelWithGeoFeatures };
