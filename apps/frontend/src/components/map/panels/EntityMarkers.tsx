import { Marker, Popup } from 'react-leaflet';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { GeoEntity, createEntityIcon, formatCoordinates } from '@/lib/map/map-config';
import { GRAPH_DEEPLINK_FALLBACK } from '@/lib/config';

interface EntityMarkersProps {
  entities: GeoEntity[];
}

export default function EntityMarkers({ entities }: EntityMarkersProps) {
  const handleViewInGraph = (nodeId: string) => {
    const url = `${GRAPH_DEEPLINK_FALLBACK}?focus=${encodeURIComponent(nodeId)}`;
    window.open(url, '_blank');
  };

  return (
    <>
      {entities.map((entity) => (
        <Marker
          key={entity.node_id}
          position={[entity.latitude, entity.longitude]}
          icon={createEntityIcon(entity.labels)}
        >
          <Popup>
            <div className="p-2 max-w-xs">
              <div className="font-medium">{entity.name || 'Unnamed Entity'}</div>
              <div className="text-sm text-gray-600 mb-2">
                {formatCoordinates(entity.latitude, entity.longitude)}
              </div>
              <div className="flex flex-wrap gap-1 mb-2">
                {entity.labels.map(label => (
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
                onClick={() => handleViewInGraph(entity.node_id)}
              >
                View in Graph
              </Button>
            </div>
          </Popup>
        </Marker>
      ))}
    </>
  );
}
