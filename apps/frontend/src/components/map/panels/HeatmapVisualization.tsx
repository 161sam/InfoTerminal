import { Marker, Popup } from "react-leaflet";
import { HeatmapPoint, createHeatmapIcon, formatCoordinates } from "@/lib/map/map-config";

interface HeatmapVisualizationProps {
  heatmapData: HeatmapPoint[];
  activeTab: string;
}

export default function HeatmapVisualization({
  heatmapData,
  activeTab,
}: HeatmapVisualizationProps) {
  if (activeTab !== "heatmap") return null;

  return (
    <>
      {heatmapData.map((point, idx) => (
        <Marker
          key={`heatmap-${idx}`}
          position={[point.latitude, point.longitude]}
          icon={createHeatmapIcon(point.intensity)}
        >
          <Popup>
            <div>
              <strong>Entity Density</strong>
              <br />
              Count: {point.intensity}
              <br />
              Location: {formatCoordinates(point.latitude, point.longitude)}
            </div>
          </Popup>
        </Marker>
      ))}
    </>
  );
}
