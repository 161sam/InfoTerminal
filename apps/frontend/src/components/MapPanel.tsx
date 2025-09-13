import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import config from '@/lib/config';

export default function MapPanel() {
  const [layers, setLayers] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch(`${config.VIEWS_API}/geo/list`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const items = data.items || data;
        const loaded: any[] = [];
        for (const f of items) {
          const r = await fetch(
            `${config.VIEWS_API}/geo/get?name=${encodeURIComponent(f.name)}`
          );
          if (r.ok) {
            loaded.push(await r.json());
          }
        }
        setLayers(loaded);
      } catch (e: any) {
        setError(e.message || 'failed to load geo data');
      }
    };
    load();
  }, []);

  const tiles =
    process.env.NEXT_PUBLIC_MAP_TILES ||
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

  return (
    <div className="w-full h-96">
      {error && <div className="text-sm text-red-600">{error}</div>}
      <MapContainer center={[0, 0]} zoom={2} style={{ height: '100%', width: '100%' }}>
        <TileLayer url={tiles} />
        {layers.map((geo, i) => (
          <GeoJSON
            key={i}
            data={geo}
            onEachFeature={(feature, layer) => {
              if (feature.properties) {
                layer.bindPopup(
                  `<pre>${JSON.stringify(feature.properties, null, 2)}</pre>`
                );
              }
            }}
          />
        ))}
      </MapContainer>
    </div>
  );
}
