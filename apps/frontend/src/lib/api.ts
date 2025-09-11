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
