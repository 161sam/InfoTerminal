export async function fetchAsset(id: string): Promise<any> {
  return { id, name: id };
}

export async function fetchAssetPrices(id: string, from?: string, to?: string): Promise<any[]> {
  return [];
}

export async function fetchGraph(id: string, depth?: number): Promise<any> {
  return { nodes: [], edges: [] };
}

export async function fetchNews(id: string): Promise<any[]> {
  return [];
}

export async function getEgo(opts: { label: string; key: string; value: string; depth?: number; limit?: number }): Promise<{ data: any; counts?: any }> {
  return { data: { nodes: [], relationships: [] }, counts: {} };
}

export async function loadPeople(payload: any): Promise<{ ok: boolean }> {
  return { ok: true };
}

export async function getShortestPath(opts: { src: string; dst: string; direction?: 'ANY' | 'OUT' | 'IN' }): Promise<{ data: any; counts?: any }> {
  return { data: { nodes: [], relationships: [] }, counts: {} };
}

export async function exportDossier(opts: { label: string; key: string; value: string }): Promise<Blob | ArrayBuffer | { ok: boolean }> {
  return { ok: true };
}
