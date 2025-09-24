import { Marker, Popup } from "react-leaflet";
import { GeocodeResult } from "@/lib/map/map-config";

interface GeocodeMarkerProps {
  geocodeResult: GeocodeResult | null;
}

export default function GeocodeMarker({ geocodeResult }: GeocodeMarkerProps) {
  if (
    !geocodeResult ||
    !geocodeResult.success ||
    !geocodeResult.latitude ||
    !geocodeResult.longitude
  ) {
    return null;
  }

  return (
    <Marker position={[geocodeResult.latitude, geocodeResult.longitude]}>
      <Popup>
        <div>
          <strong>Search Result</strong>
          <br />
          {geocodeResult.display_name}
          <br />
          Confidence: {((geocodeResult.confidence || 0) * 100).toFixed(0)}%
        </div>
      </Popup>
    </Marker>
  );
}
