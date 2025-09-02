export async function fetchAsset(id: string) {
  const res = await fetch(`/api/assets/${id}`);
  if (!res.ok) throw new Error('Failed to fetch asset');
  return res.json();
}

export async function fetchAssetPrices(id: string, from?: string, to?: string) {
  const params = new URLSearchParams();
  if (from) params.append('from', from);
  if (to) params.append('to', to);
  const res = await fetch(`/api/assets/${id}/prices?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch prices');
  return res.json();
}

export async function fetchGraph(id: string, depth = 1) {
  const res = await fetch(`/api/graph?node=${id}&depth=${depth}`);
  if (!res.ok) throw new Error('Failed to fetch graph');
  return res.json();
}

export async function fetchNews(entityId: string) {
  const res = await fetch(`/api/news?entity=${entityId}`);
  if (!res.ok) throw new Error('Failed to fetch news');
  return res.json();
}
