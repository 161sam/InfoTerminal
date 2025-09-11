/**
 * TEMP shim until Codex consolidates API layer.
 * Replace with real implementations or re-export from existing modules.
 */

export type Id = string;

// ---------- Asset / News / Graph (Basis) ----------

export async function fetchAsset(id: Id) {
  return { id, name: `Asset ${id}` };
}

export async function fetchAssetPrices(
  id: Id,
  from?: string | number,
  to?: string | number
): Promise<Array<{ t: number; v: number }>> {
  return [{ t: Date.now(), v: 100 }];
}

export async function fetchGraph(
  id: Id,
  depth?: number
): Promise<{ nodes: any[]; edges: any[] }> {
  return {
    nodes: [{ id, name: `Node ${id}`, depth: depth ?? 0 }],
    edges: [],
  };
}

export async function fetchNews(id: Id) {
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
 * GraphX greift auf .data.nodes / .data.relationships / .counts zu,
 * verwendet aber teilweise auch ein Cytoscape-ähnliches .data.elements.
 * Wir liefern beides für maximale Kompatibilität.
 */
export async function getEgo(params: EgoParams): Promise<{
  data: {
    nodes: Array<{ data: any }>;
    relationships: Array<{ data: any }>;
    elements: Array<{ data: any }>;
  };
  counts: { nodes: number; relationships: number };
}> {
  const center = String(params.value ?? 'center');

  const nodes = [
    { data: { id: center, label: 'Center' } },
    { data: { id: 'n2', label: 'Neighbor' } },
  ];
  const relationships = [{ data: { source: center, target: 'n2' } }];
  const elements = [...nodes, ...relationships];

  return {
    data: { nodes, relationships, elements },
    counts: { nodes: nodes.length, relationships: relationships.length },
  };
}

/**
 * loadPeople liefert { data: [...] , counts: {...} }
 */
export async function loadPeople(
  query?: { q?: string; limit?: number }
): Promise<{
  data: Array<{ id: string; name: string; knows_id?: string }>;
  counts: { total: number };
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
 * getShortestPath wird teils als getShortestPath(a,b),
 * teils mit Objektargumenten { srcLabel, srcKey, srcVal, dstLabel, dstKey, dstVal } aufgerufen.
 * Wir unterstützen beides und liefern { data.{nodes,relationships,elements} }.
 */
type ShortestPathObjArgs = {
  srcLabel: string;
  srcKey: string;
  srcVal: string | number;
  dstLabel: string;
  dstKey: string;
  dstVal: string | number;
};

export async function getShortestPath(
  a: Id,
  b?: Id
): Promise<{
  data: {
    nodes: Array<{ data: any }>;
    relationships: Array<{ data: any }>;
    elements: Array<{ data: any }>;
  };
}>;

export async function getShortestPath(
  params: ShortestPathObjArgs
): Promise<{
  data: {
    nodes: Array<{ data: any }>;
    relationships: Array<{ data: any }>;
    elements: Array<{ data: any }>;
  };
}>;

export async function getShortestPath(
  aOrObj: Id | ShortestPathObjArgs,
  b?: Id
) {
  const start = typeof aOrObj === 'string' ? String(aOrObj) : String(aOrObj.srcVal);
  const end =
    typeof aOrObj === 'string' ? String(b ?? aOrObj) : String(aOrObj.dstVal);

  const ids = [start, 'mid', end];

  const nodes = ids.map((id) => ({ data: { id, label: id } }));
  const relationships = ids.slice(0, -1).map((id, i) => ({
    data: { source: id, target: ids[i + 1] },
  }));
  const elements = [...nodes, ...relationships];

  return { data: { nodes, relationships, elements } };
}

/**
 * Simple Erfolgsantwort inkl. URL
 */
export async function exportDossier(
  entityId: Id
): Promise<{ ok: boolean; id: Id; url: string }> {
  return { ok: true, id: entityId, url: `/api/dossier/${entityId}.pdf` };
}
