import { useState, useEffect } from "react";
import { useMapEvents, useMap } from "react-leaflet";
import L from "leaflet";
import { BoundingBox, MAP_STYLES } from "@/lib/map/map-config";

interface BoundingBoxDrawerProps {
  onBoundsChange: (bounds: BoundingBox | null) => void;
  enabled: boolean;
}

export default function BoundingBoxDrawer({ onBoundsChange, enabled }: BoundingBoxDrawerProps) {
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
      const rectangle = L.rectangle(bounds, MAP_STYLES.boundingBox);
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
}
