import React, { useEffect, useMemo, useState, useCallback } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import { RefreshCw } from 'lucide-react';

// Import modularized components
import MapControls from '@/components/map/panels/MapControls';
import BoundingBoxDrawer from '@/components/map/panels/BoundingBoxDrawer';
import EntityMarkers from '@/components/map/panels/EntityMarkers';
import HeatmapVisualization from '@/components/map/panels/HeatmapVisualization';
import MapLayers from '@/components/map/panels/MapLayers';
import GeocodeMarker from '@/components/map/panels/GeocodeMarker';
import MapClickHandler from '@/components/map/panels/MapClickHandler';

// Import types and utilities
import { 
  GeoEntity, 
  BoundingBox, 
  HeatmapPoint, 
  GeocodeResult, 
  GeoStatistics,
  NearbySearch,
  DEFAULT_MAP_CONFIG,
  setupLeafletIcons 
} from '@/lib/map/map-config';
import { MapService } from '@/lib/map/map-service';
import config from '@/lib/config';

interface MapPanelProps {
  graphApiUrl?: string;
  viewsApiUrl?: string;
  className?: string;
}

export default function MapPanel({
  graphApiUrl = 'http://localhost:8612',
  viewsApiUrl = config.VIEWS_API,
  className = ''
}: MapPanelProps) {
  // Setup leaflet icons
  useMemo(() => {
    setupLeafletIcons();
  }, []);

  // Create map service
  const mapService = useMemo(() => 
    new MapService(graphApiUrl, viewsApiUrl), 
    [graphApiUrl, viewsApiUrl]
  );

  // Original map state
  const [layers, setLayers] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [originalEntities, setOriginalEntities] = useState<any | null>(null);

  // Geospatial state
  const [geoEntities, setGeoEntities] = useState<GeoEntity[]>([]);
  const [searchLocation, setSearchLocation] = useState('');
  const [geocodeResult, setGeocodeResult] = useState<GeocodeResult | null>(null);
  const [boundingBoxMode, setBoundingBoxMode] = useState(false);
  const [selectedBounds, setSelectedBounds] = useState<BoundingBox | null>(null);
  const [nearbySearch, setNearbySearch] = useState<NearbySearch>({ lat: 0, lng: 0, radius: 10 });
  const [heatmapData, setHeatmapData] = useState<HeatmapPoint[]>([]);
  const [geoStats, setGeoStats] = useState<GeoStatistics | null>(null);
  const [activeTab, setActiveTab] = useState('entities');
  const [showControls, setShowControls] = useState(true);

  // Map configuration
  const [mapCenter, setMapCenter] = useState<[number, number]>(DEFAULT_MAP_CONFIG.center);
  const [mapZoom, setMapZoom] = useState(DEFAULT_MAP_CONFIG.zoom);

  const loadOriginalData = useCallback(async () => {
    setLoading(true);
    try {
      const { layers: loadedLayers, entities } = await mapService.loadOriginalData();
      setLayers(loadedLayers);
      setOriginalEntities(entities);
      setError(null);
    } catch (e: any) {
      setError(e.message || 'Failed to load map data');
    } finally {
      setLoading(false);
    }
  }, [mapService]);

  const fetchGeoEntities = useCallback(async (bounds?: BoundingBox) => {
    if (!bounds) return;
    
    try {
      const entities = await mapService.fetchGeoEntities(bounds);
      setGeoEntities(entities);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch entities');
    }
  }, [mapService]);

  const fetchNearbyEntities = useCallback(async (lat: number, lng: number, radius: number) => {
    try {
      const entities = await mapService.fetchNearbyEntities(lat, lng, radius);
      setGeoEntities(entities);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch nearby entities');
    }
  }, [mapService]);

  const geocodeLocation = useCallback(async (location: string) => {
    if (!location.trim()) return;
    
    try {
      const result = await mapService.geocodeLocation(location);
      setGeocodeResult(result);
      
      if (result.success && result.latitude && result.longitude) {
        setMapCenter([result.latitude, result.longitude]);
        setMapZoom(15);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Geocoding failed');
    }
  }, [mapService]);

  const fetchHeatmapData = useCallback(async (bounds: BoundingBox) => {
    try {
      const heatmap = await mapService.fetchHeatmapData(bounds);
      setHeatmapData(heatmap);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch heatmap data');
    }
  }, [mapService]);

  const fetchGeoStatistics = useCallback(async () => {
    try {
      const stats = await mapService.fetchGeoStatistics();
      setGeoStats(stats);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch statistics');
    }
  }, [mapService]);

  useEffect(() => {
    loadOriginalData();
    fetchGeoStatistics();
  }, [loadOriginalData, fetchGeoStatistics]);

  useEffect(() => {
    if (selectedBounds) {
      fetchGeoEntities(selectedBounds);
      if (activeTab === 'heatmap') {
        fetchHeatmapData(selectedBounds);
      }
    }
  }, [selectedBounds, fetchGeoEntities, fetchHeatmapData, activeTab]);

  const handleMapClick = useCallback((e: L.LeafletMouseEvent) => {
    if (activeTab === 'nearby') {
      setNearbySearch({ lat: e.latlng.lat, lng: e.latlng.lng, radius: nearbySearch.radius });
      fetchNearbyEntities(e.latlng.lat, e.latlng.lng, nearbySearch.radius);
    }
  }, [activeTab, fetchNearbyEntities, nearbySearch.radius]);

  return (
    <div className={`relative w-full h-full ${className}`}>
      <MapContainer
        center={mapCenter}
        zoom={mapZoom}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Original GeoJSON layers */}
        <MapLayers layers={layers} />

        {/* Enhanced geo entities */}
        <EntityMarkers entities={geoEntities} />

        {/* Heatmap visualization */}
        <HeatmapVisualization heatmapData={heatmapData} activeTab={activeTab} />

        {/* Geocode result marker */}
        <GeocodeMarker geocodeResult={geocodeResult} />

        {/* Bounding box drawer */}
        <BoundingBoxDrawer
          enabled={boundingBoxMode}
          onBoundsChange={setSelectedBounds}
        />

        {/* Map click handler for nearby search */}
        <MapClickHandler onClick={handleMapClick} />
      </MapContainer>

      {/* Map controls */}
      <MapControls
        searchLocation={searchLocation}
        setSearchLocation={setSearchLocation}
        onGeocode={geocodeLocation}
        geocodeSuccess={geocodeResult?.success || false}
        geocodeMessage={geocodeResult?.display_name}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        boundingBoxMode={boundingBoxMode}
        setBoundingBoxMode={setBoundingBoxMode}
        selectedBounds={selectedBounds}
        entitiesCount={geoEntities.length}
        nearbySearch={nearbySearch}
        setNearbySearch={setNearbySearch}
        heatmapPointsCount={heatmapData.length}
        geoStats={geoStats}
        showControls={showControls}
        setShowControls={setShowControls}
        onRefresh={loadOriginalData}
        onFetchStats={fetchGeoStatistics}
      />

      {/* Error display */}
      {error && (
        <div className="absolute bottom-4 left-4 bg-red-50 border border-red-200 text-red-700 px-3 py-2 rounded shadow-lg z-[1000]">
          {error}
        </div>
      )}

      {/* Loading display */}
      {loading && (
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-4 rounded shadow-lg z-[1000]">
          <RefreshCw className="h-6 w-6 animate-spin mx-auto" />
          <div className="mt-2 text-sm">Loading map data...</div>
        </div>
      )}
    </div>
  );
}

// Export for backward compatibility
export { MapPanel as EnhancedMapPanel };
export { MapPanel as MapPanelWithGeoFeatures };
