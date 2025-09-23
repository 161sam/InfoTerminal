// Map types and configuration
import L from 'leaflet';

export interface GeoEntity {
  node_id: string;
  name: string;
  latitude: number;
  longitude: number;
  labels: string[];
  distance_km?: number;
}

export interface BoundingBox {
  south: number;
  west: number;
  north: number;
  east: number;
}

export interface HeatmapPoint {
  latitude: number;
  longitude: number;
  intensity: number;
}

export interface GeocodeResult {
  success: boolean;
  latitude?: number;
  longitude?: number;
  display_name?: string;
  address?: any;
  confidence?: number;
  error?: string;
}

export interface GeoStatistics {
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

export interface NearbySearch {
  lat: number;
  lng: number;
  radius: number;
}

export interface MapConfig {
  center: [number, number];
  zoom: number;
  graphApiUrl: string;
  viewsApiUrl: string;
}

// Default map configuration
export const DEFAULT_MAP_CONFIG: MapConfig = {
  center: [51.505, -0.09],
  zoom: 13,
  graphApiUrl: 'http://localhost:8612',
  viewsApiUrl: 'http://localhost:8611'
};

// Entity type colors
export const ENTITY_COLORS = {
  'Person': '#ef4444',
  'Organization': '#3b82f6', 
  'Location': '#10b981',
  'Event': '#f59e0b',
  'Default': '#6b7280'
};

// Map style configuration
export const MAP_STYLES = {
  geojson: {
    color: '#3388ff',
    weight: 2,
    opacity: 0.8,
    fillOpacity: 0.3
  },
  boundingBox: {
    color: '#3b82f6',
    fillColor: '#3b82f6',
    fillOpacity: 0.1,
    weight: 2
  }
};

// Leaflet marker fix
export function setupLeafletIcons() {
  delete (L.Icon.Default.prototype as any)._getIconUrl;
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  });
}

// Utility functions
export function createEntityIcon(labels: string[]): L.DivIcon {
  const primaryLabel = labels[0] || 'Unknown';
  const color = ENTITY_COLORS[primaryLabel as keyof typeof ENTITY_COLORS] || ENTITY_COLORS.Default;

  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="background: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
    iconSize: [20, 20],
    iconAnchor: [10, 10]
  });
}

export function createHeatmapIcon(intensity: number): L.DivIcon {
  const normalizedIntensity = Math.min(intensity / 10, 1);
  const radius = Math.max(5, intensity * 2);
  
  return L.divIcon({
    className: 'heatmap-marker',
    html: `<div style="
      background: rgba(255, 0, 0, ${normalizedIntensity});
      width: ${radius}px;
      height: ${radius}px;
      border-radius: 50%;
      border: 1px solid rgba(255, 0, 0, 0.8);
    "></div>`,
    iconSize: [radius, radius],
    iconAnchor: [radius / 2, radius / 2]
  });
}

export function formatBounds(bounds: BoundingBox): string {
  return `${bounds.south.toFixed(3)}, ${bounds.west.toFixed(3)} to ${bounds.north.toFixed(3)}, ${bounds.east.toFixed(3)}`;
}

export function formatCoordinates(lat: number, lng: number): string {
  return `${lat.toFixed(6)}, ${lng.toFixed(6)}`;
}
