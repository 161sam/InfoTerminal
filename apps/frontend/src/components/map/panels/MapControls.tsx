import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Search, Settings, RefreshCw, BarChart3 } from "lucide-react";
import { BoundingBox, GeoStatistics, NearbySearch, formatBounds } from "@/lib/map/map-config";

interface MapControlsProps {
  searchLocation: string;
  setSearchLocation: (location: string) => void;
  onGeocode: (location: string) => void;
  geocodeSuccess: boolean;
  geocodeMessage?: string;
  activeTab: string;
  setActiveTab: (tab: string) => void;
  boundingBoxMode: boolean;
  setBoundingBoxMode: (enabled: boolean) => void;
  selectedBounds: BoundingBox | null;
  entitiesCount: number;
  nearbySearch: NearbySearch;
  setNearbySearch: (search: NearbySearch) => void;
  heatmapPointsCount: number;
  geoStats: GeoStatistics | null;
  showControls: boolean;
  setShowControls: (show: boolean) => void;
  onRefresh: () => void;
  onFetchStats: () => void;
}

export default function MapControls({
  searchLocation,
  setSearchLocation,
  onGeocode,
  geocodeSuccess,
  geocodeMessage,
  activeTab,
  setActiveTab,
  boundingBoxMode,
  setBoundingBoxMode,
  selectedBounds,
  entitiesCount,
  nearbySearch,
  setNearbySearch,
  heatmapPointsCount,
  geoStats,
  showControls,
  setShowControls,
  onRefresh,
  onFetchStats,
}: MapControlsProps) {
  return (
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
              <Button size="sm" onClick={() => onGeocode(searchLocation)}>
                <Search className="h-4 w-4" />
              </Button>
            </div>
            {geocodeSuccess && geocodeMessage && (
              <div className="text-xs text-green-600">Found: {geocodeMessage}</div>
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
                  <div>Entities: {entitiesCount}</div>
                  <div>Bounds: {formatBounds(selectedBounds)}</div>
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
                    setNearbySearch({ ...nearbySearch, radius: Number(e.target.value) })
                  }
                  min="1"
                  max="100"
                  className="mt-1"
                />
              </div>
            </TabsContent>

            <TabsContent value="heatmap" className="mt-3">
              <div className="text-sm">Draw bounding box to generate entity heatmap</div>
              {heatmapPointsCount > 0 && (
                <div className="text-xs text-gray-600">Heatmap points: {heatmapPointsCount}</div>
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
            <Button variant="outline" size="sm" onClick={onRefresh}>
              <RefreshCw className="h-4 w-4 mr-1" />
              Refresh
            </Button>
            <Button variant="outline" size="sm" onClick={onFetchStats}>
              <BarChart3 className="h-4 w-4 mr-1" />
              Stats
            </Button>
          </div>
        </CardContent>
      )}
    </Card>
  );
}
