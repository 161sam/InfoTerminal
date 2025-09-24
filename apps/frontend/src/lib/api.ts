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
  to?: string | number,
): Promise<Array<{ t: number; v: number }>> {
  return [{ t: Date.now(), v: 100 }];
}

export async function fetchGraph(id: Id, depth?: number): Promise<{ nodes: any[]; edges: any[] }> {
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
  const center = String(params.value ?? "center");

  const nodes = [
    { data: { id: center, label: "Center" } },
    { data: { id: "n2", label: "Neighbor" } },
  ];
  const relationships = [{ data: { source: center, target: "n2" } }];
  const elements = [...nodes, ...relationships];

  return {
    data: { nodes, relationships, elements },
    counts: { nodes: nodes.length, relationships: relationships.length },
  };
}

/**
 * loadPeople: Konsistenter Rückgabetyp
 * - Seed (Array übergeben) -> { data, inserted }
 * - Query (kein Array)     -> { data }
 */
type PersonRow = { id: string; name: string; knows_id?: string | null };

// Overloads (typed)
export function loadPeople(
  people: Array<PersonRow>,
): Promise<{ data: Array<PersonRow>; inserted: number }>;
export function loadPeople(query?: {
  q?: string;
  limit?: number;
}): Promise<{ data: Array<PersonRow>; inserted?: undefined }>;

// Implementation (broad signature)
export async function loadPeople(
  arg?: Array<PersonRow> | { q?: string; limit?: number },
): Promise<{ data: Array<PersonRow>; inserted?: number }> {
  // Seed mode: array provided
  if (Array.isArray(arg)) {
    const data = arg.map((p) => ({
      id: String(p.id),
      name: String(p.name),
      knows_id: p.knows_id ?? undefined,
    }));
    const inserted = data.length;
    return { data, inserted };
  }

  // Query/default mode: generate list
  const n = (arg as { limit?: number } | undefined)?.limit ?? 5;
  const data = Array.from({ length: n }, (_, i) => ({
    id: `p${i + 1}`,
    name: `Person ${i + 1}`,
    knows_id: i > 0 ? `p${i}` : undefined,
  }));
  return { data };
}

/**
 * getShortestPath wird teils als getShortestPath(a,b),
 * teils mit Objektargumenten { srcLabel, srcKey, srcVal, dstLabel, dstKey, dstVal } aufgerufen.
 * Wir unterstützen beides und liefern { data.{nodes,relationships,elements} }.
 */
type ShortestPathObjArgs = {
  srcLabel: string;
  srcKey: string;
  srcValue?: string | number; // preferred naming
  srcVal?: string | number; // legacy alias
  dstLabel: string;
  dstKey: string;
  dstValue?: string | number; // preferred naming
  dstVal?: string | number; // legacy alias
  // optional parameters used by callers
  maxLen?: number;
};

export function getShortestPath(
  a: Id,
  b?: Id,
): Promise<{
  data: {
    nodes: Array<{ data: any }>;
    relationships: Array<{ data: any }>;
    elements: Array<{ data: any }>;
  };
}>;

export function getShortestPath(params: ShortestPathObjArgs): Promise<{
  data: {
    nodes: Array<{ data: any }>;
    relationships: Array<{ data: any }>;
    elements: Array<{ data: any }>;
  };
}>;

export async function getShortestPath(aOrObj: Id | ShortestPathObjArgs, b?: Id) {
  const start =
    typeof aOrObj === "string" ? String(aOrObj) : String(aOrObj.srcValue ?? aOrObj.srcVal ?? "");
  const end =
    typeof aOrObj === "string"
      ? String(b ?? aOrObj)
      : String(aOrObj.dstValue ?? aOrObj.dstVal ?? "");

  const ids = [start, "mid", end];

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
// Overloads: accept plain Id or a selector object
export function exportDossier(entityId: Id): Promise<{ ok: boolean; id: Id; url: string }>;

export function exportDossier(params: {
  label: string;
  key: string;
  value: string | number;
  depth?: number;
}): Promise<{
  ok: boolean;
  label: string;
  key: string;
  value: string | number;
  depth?: number;
  url: string;
}>;

export async function exportDossier(
  entityOrParams: Id | { label: string; key: string; value: string | number; depth?: number },
) {
  if (typeof entityOrParams === "string") {
    const entityId = entityOrParams;
    return { ok: true, id: entityId, url: `/api/dossier/${entityId}.pdf` };
  }
  const { label, key, value, depth } = entityOrParams;
  const safeId = `${label.toLowerCase()}_${String(value)}`.replace(/[^a-z0-9_-]+/gi, "_");
  return {
    ok: true,
    label,
    key,
    value,
    depth,
    url: `/api/dossier/${safeId}.pdf`,
  };
}
