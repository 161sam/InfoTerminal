/**
 * TEMP shim until Codex consolidates API layer.
 * Replace with real implementations or re-export from existing modules.
 */

export type Id = string;

export async function fetchAsset(id: Id) {
  // TODO: replace with real fetch to your gateway
  return { id, name: `Asset ${id}` };
}

export async function fetchAssetPrices(id: Id) {
  // TODO: backend call; structure expected by pages/asset/[id].tsx charts
  return [{ t: Date.now(), v: 100 }];
}

export async function fetchGraph(id: Id) {
  // TODO: return minimal graph structure used by pages/* consumers
  return {
    nodes: [{ id, name: `Node ${id}` }],
    edges: [],
  };
}

export async function fetchNews(id: Id) {
  // TODO: backend call or leave empty for now
  return [];
}

export async function fetchAssetPrices(id: Id, from?: string | number, to?: string | number) {
  // Akzeptiere from/to optional – Aufrufer übergeben teils 2-3 Args
  return [{ t: Date.now(), v: 100 }];
}

export async function fetchGraph(id: Id, depth?: number) {
  // depth optional – Aufrufer rufen z.B. fetchGraph(id, 1)
  return {
    nodes: [{ id, name: `Node ${id}` }],
    edges: [],
  };
}

// === Fehlende GraphX-APIs (Minimalstubs) ===

export type EgoParams = {
  label?: string;
  key?: string;
  value?: string | number;
  depth?: number;
  limit?: number;
};

export async function getEgo(params: EgoParams) {
  const center = params.value ?? 'center';
  return {
    elements: [
      { data: { id: String(center), label: 'Center' } },
      { data: { id: 'n2', label: 'Neighbor' } },
      { data: { source: String(center), target: 'n2' } },
    ],
  };
}

export async function loadPeople(query?: { q?: string; limit?: number }) {
  const n = query?.limit ?? 5;
  return Array.from({ length: n }, (_, i) => ({
    id: `p${i + 1}`,
    name: `Person ${i + 1}`,
    knows_id: i % 2 ? `p${i}` : undefined,
  }));
}

export async function getShortestPath(a: Id, b: Id) {
  // Dummy-Pfad
  return {
    path: [a, 'mid', b].map((id, i, arr) => ({
      data: i < arr.length - 1 ? { source: arr[i], target: arr[i + 1] } : { id },
    })),
  };
}

export async function exportDossier(entityId: Id) {
  // Rückgabe z. B. Blob-URL/Dateiinfo
  return { ok: true, id: entityId, url: `/api/dossier/${entityId}.pdf` };
}
