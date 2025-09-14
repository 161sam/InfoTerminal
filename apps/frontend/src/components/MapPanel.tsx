import { useEffect, useMemo, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import config from '@/lib/config';

export default function MapPanel() {
  const [layers, setLayers] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [entities, setEntities] = useState<any | null>(null);
  const [showEntities, setShowEntities] = useState<boolean>(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const listUrl = `${config.VIEWS_API}/geo/list`;
        const res = await fetch(listUrl);
        // Treat 404 as "no layers available" instead of an error
        if (res.status === 404) {
          setLayers([]);
          setError(null);
          return;
        }
        if (!res.ok) throw new Error(`Failed to load geo list (${res.status})`);
        const data = await res.json();
        const items = data.items || data || [];
        const loaded: any[] = [];
        for (const f of items) {
          try {
            const r = await fetch(
              `${config.VIEWS_API}/geo/get?name=${encodeURIComponent(f.name)}`
            );
            if (r.status === 404) continue; // silently skip missing layers
            if (!r.ok) continue;
            loaded.push(await r.json());
          } catch {
            // skip individual layer errors
          }
        }
        setLayers(loaded);
        try {
          const entRes = await fetch(`${config.VIEWS_API}/geo/entities`);
          if (entRes.ok) {
            setEntities(await entRes.json());
          }
        } catch {
          // ignore entity layer errors
        }
        setError(null);
      } catch (e: any) {
        // Show a concise error but keep the UI usable
        setError(e?.message ?? 'Failed to load geospatial data');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const tiles = useMemo(() => (
    process.env.NEXT_PUBLIC_MAP_TILES || 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
  ), []);

  return (
    <div className="w-full">
      <div className="h-96 w-full rounded border border-gray-200 overflow-hidden">
        <MapContainer center={[0, 0]} zoom={2} style={{ height: '100%', width: '100%' }}>
          <TileLayer url={tiles} />
          {showEntities && entities && (
            <GeoJSON
              data={entities}
              onEachFeature={(feature, layer) => {
                const props: any = feature.properties || {};
                const id = props.id || '';
                const name = props.name || id;
                const link = `${config.GRAPH_DEEPLINK_FALLBACK}${encodeURIComponent(id)}`;
                layer.bindPopup(`<a href="${link}">${name}</a>`);
              }}
            />
          )}
          {layers.map((geo, i) => (
            <GeoJSON
              key={i}
              data={geo}
              onEachFeature={(feature, layer) => {
                if (feature.properties) {
                  layer.bindPopup(
                    `<pre style="margin:0;">${JSON.stringify(feature.properties, null, 2)}</pre>`
                  );
                }
              }}
            />
          ))}
        </MapContainer>
      </div>

      <div className="mt-2 text-xs text-gray-600 dark:text-gray-300">
        <label className="mr-2">
          <input
            type="checkbox"
            checked={showEntities}
            onChange={(e) => setShowEntities(e.target.checked)}
          />{' '}
          Entities
        </label>
        {loading && <span>Loading layers…</span>}
        {!loading && error && <span className="text-red-600">{error}</span>}
        {!loading && !error && layers.length === 0 && <span>No layers found.</span>}
      </div>
    </div>
  );
}
