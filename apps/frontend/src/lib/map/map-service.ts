// Map service utilities for API interactions
import { BoundingBox, GeoEntity, GeocodeResult, GeoStatistics, HeatmapPoint } from "./map-config";
import { toSearchParams } from "@/lib/url";

export class MapService {
  constructor(
    private graphApiUrl: string,
    private viewsApiUrl: string,
  ) {}

  async fetchGeoEntities(bounds: BoundingBox): Promise<GeoEntity[]> {
    const params = toSearchParams({
      south: bounds.south.toString(),
      west: bounds.west.toString(),
      north: bounds.north.toString(),
      east: bounds.east.toString(),
      limit: "100",
    });

    const response = await fetch(`${this.graphApiUrl}/geo/entities?${params}`);
    if (!response.ok) throw new Error("Failed to fetch geo entities");

    const data = await response.json();
    return data.entities || [];
  }

  async fetchNearbyEntities(lat: number, lng: number, radius: number): Promise<GeoEntity[]> {
    const response = await fetch(`${this.graphApiUrl}/geo/entities/nearby`, {
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
    return data.entities || [];
  }

  async geocodeLocation(location: string): Promise<GeocodeResult> {
    const response = await fetch(`${this.graphApiUrl}/geo/geocode`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ location }),
    });

    if (!response.ok) throw new Error("Geocoding failed");

    return await response.json();
  }

  async fetchHeatmapData(bounds: BoundingBox): Promise<HeatmapPoint[]> {
    const params = toSearchParams({
      south: bounds.south.toString(),
      west: bounds.west.toString(),
      north: bounds.north.toString(),
      east: bounds.east.toString(),
      grid_size: "20",
    });

    const response = await fetch(`${this.graphApiUrl}/geo/heatmap?${params}`);
    if (!response.ok) throw new Error("Failed to fetch heatmap data");

    const data = await response.json();
    return data.heatmap_points || [];
  }

  async fetchGeoStatistics(): Promise<GeoStatistics> {
    const response = await fetch(`${this.graphApiUrl}/geo/statistics`);
    if (!response.ok) throw new Error("Failed to fetch statistics");

    return await response.json();
  }

  async loadOriginalData(): Promise<{ layers: any[]; entities: any }> {
    const listUrl = `${this.viewsApiUrl}/geo/list`;
    const res = await fetch(listUrl);

    if (res.status === 404) {
      return { layers: [], entities: null };
    }

    if (!res.ok) throw new Error(`Failed to load geo list (${res.status})`);

    const data = await res.json();
    const items = data.items || data || [];
    const loaded: any[] = [];

    for (const f of items) {
      try {
        const r = await fetch(`${this.viewsApiUrl}/geo/get?name=${encodeURIComponent(f.name)}`);
        if (r.status === 404) continue;
        if (!r.ok) continue;
        loaded.push(await r.json());
      } catch {
        continue;
      }
    }

    let entities = null;
    try {
      const entRes = await fetch(`${this.viewsApiUrl}/geo/entities`);
      if (entRes.ok) {
        entities = await entRes.json();
      }
    } catch {
      // ignore entity layer errors
    }

    return { layers: loaded, entities };
  }
}
