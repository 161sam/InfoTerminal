import { GeoJSON } from "react-leaflet";
import { MAP_STYLES } from "@/lib/map/map-config";

interface MapLayersProps {
  layers: any[];
}

export default function MapLayers({ layers }: MapLayersProps) {
  return (
    <>
      {layers.map((layer, idx) => (
        <GeoJSON
          key={`layer-${idx}`}
          data={layer}
          style={MAP_STYLES.geojson}
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
    </>
  );
}
