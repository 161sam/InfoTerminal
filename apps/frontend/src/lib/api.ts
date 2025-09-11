/**
 * TEMP shim until Codex consolidates API layer.
 * Replace with real implementations or re-export from existing modules.
 */

export type Id = string;

// ---------- Asset / News / Graph (Basis) ----------

export async function fetchAsset(id: Id) {
  // TODO: replace with real fetch to your gateway
  return { id, name: `Asset ${id}` };
}

export async function fetchAssetPrices(
  id: Id,
  from?: string | number,
  to?: string | number
): Promise<Array<{ t: number; v: number }>> {
  // Akzeptiere from/to optional – Aufrufer übergeben teils 2-3 Args
  // TODO: backend call; structure expected by pages/asset/[id].tsx charts
  return [{ t: Date.now(), v: 100 }];
}

export async function fetchGraph(
  id: Id,
  depth?: number
): Promise<{ nodes: any[]; edges: any[] }> {
  // depth optional – Aufrufer rufen z.B. fetchGraph(id, 1)
  // TODO: return minimal graph structure used by pages/* consumers
  return {
    nodes: [{ id, name: `Node ${id}`, depth: depth ?? 0 }],
    edges: [],
  };
}

export async function fetchNews(id: Id) {
  // TODO: backend call or leave empty for now
  return [];
}

// ---------- GraphX-spezifische Minimal-APIs ----------

export type EgoParams = {
  label?: string;
  key?: string;
  value?: string | number;
  depth?: number;
  limit?: number;
};

/**
 * GraphX erwartet ein Objekt mit .data.elements und optional .counts
 */
export async function getEgo(
  params: EgoParams
): Promise<{ data: { elements: any[] }; counts?: Record<string, number> }> {
  const center = String(params.value ?? 'center');
  const elements = [
    { data: { id: center, label: 'Center' } },
    { data: { id: 'n2', label: 'Neighbor' } },
    { data: { source: center, target: 'n2' } },
  ];
  return {
    data: { elements },
    counts: { nodes: 2, edges: 1 },
  };
}

/**
 * GraphX greift auf .data (Array) und optional .counts zu
 */
export async function loadPeople(
  query?: { q?: string; limit?: number }
): Promise<{
  data: Array<{ id: string; name: string; knows_id?: string }>;
  counts?: Record<string, number>;
}> {
  const n = query?.limit ?? 5;
  const data = Array.from({ length: n }, (_, i) => ({
    id: `p${i + 1}`,
    name: `Person ${i + 1}`,
    knows_id: i > 0 ? `p${i}` : undefined,
  }));
  return { data, counts: { total: data.length } };
}

/**
 * Darf mit 1 oder 2 Argumenten aufgerufen werden.
 * Rückgabeform: { data: [...] } (nicht { path: ...}),
 * da graphx.tsx auf .data zugreift.
 */
export async function getShortestPath(
  a: Id,
  b?: Id
): Promise<{ data: Array<{ data: any }> }> {
  const start = String(a);
  const end = String(b ?? a);
  const ids = [start, 'mid', end];

  const nodes = ids.map((id) => ({ data: { id, label: id } }));
  const edges = ids.slice(0, -1).map((id, i) => ({
    data: { source: id, target: ids[i + 1] },
  }));

  return { data: [...nodes, ...edges] };
}

/**
 * Liefert einfache Erfolgsantwort inkl. URL (z. B. für Download)
 */
export async function exportDossier(
  entityId: Id
): Promise<{ ok: boolean; id: Id; url: string }> {
  return { ok: true, id: entityId, url: `/api/dossier/${entityId}.pdf` };
}
