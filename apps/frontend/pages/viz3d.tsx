import dynamic from 'next/dynamic';
import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Panel from '@/components/layout/Panel';

// Load DeckGL component only on client
const DeckGLComp = dynamic(() => import('@deck.gl/react').then((m: any) => m.default || m.DeckGL), { ssr: false });

export default function Viz3DPage() {
  const [ScatterplotLayer, setScatterplotLayer] = useState<any>(null);

  useEffect(() => {
    // Load layers on client to avoid SSR issues
    import('@deck.gl/layers').then((m: any) => setScatterplotLayer(() => m.ScatterplotLayer));
  }, []);

  const layers = ScatterplotLayer ? [
    new ScatterplotLayer({
      id: 'scatter',
      data: [{ position: [0, 0], size: 100 }, { position: [0.1, 0.1], size: 80 }],
      getPosition: (d: any) => d.position,
      getRadius: (d: any) => d.size,
      getFillColor: [200, 0, 80]
    })
  ] : [];

  return (
    <DashboardLayout title="3D Visualization" subtitle="deck.gl demo">
      <div className="p-4 space-y-4">
        <Panel>
          <div style={{ height: 500 }}>
            {ScatterplotLayer ? (
              // @ts-ignore: dynamic ESM default
              <DeckGLComp initialViewState={{ longitude: 0, latitude: 0, zoom: 12, pitch: 45, bearing: 0 }} controller={true} layers={layers} />
            ) : (
              <div className="text-sm text-gray-500">Loading 3D components…</div>
            )}
          </div>
        </Panel>
      </div>
    </DashboardLayout>
  );
}
