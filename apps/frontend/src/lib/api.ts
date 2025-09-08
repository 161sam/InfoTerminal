export const VIEWS_API =
  process.env.NEXT_PUBLIC_VIEWS_API || "http://localhost:8403";

export async function getEgo(opts: {
  label: string;
  key: string;
  value: string;
  depth?: number;
  limit?: number;
}) {
  const params = new URLSearchParams({
    label: opts.label,
    key: opts.key,
    value: String(opts.value),
  });
  if (opts.depth != null) params.set("depth", String(opts.depth));
  if (opts.limit != null) params.set("limit", String(opts.limit));
  const res = await fetch(`${VIEWS_API}/graphs/view/ego?${params.toString()}`);
  if (!res.ok) throw new Error(`ego failed: ${res.status}`);
  return res.json();
}

export async function getShortestPath(opts: {
  srcLabel: string; srcKey: string; srcValue: string;
  dstLabel: string; dstKey: string; dstValue: string;
  maxLen?: number;
}) {
  const params = new URLSearchParams({
    srcLabel: opts.srcLabel,
    srcKey: opts.srcKey,
    srcValue: String(opts.srcValue),
    dstLabel: opts.dstLabel,
    dstKey: opts.dstKey,
    dstValue: String(opts.dstValue),
  });
  if (opts.maxLen != null) params.set("max_len", String(opts.maxLen));
  const res = await fetch(`${VIEWS_API}/graphs/view/shortest-path?${params.toString()}`);
  if (!res.ok) throw new Error(`shortest-path failed: ${res.status}`);
  return res.json();
}

// Dev-only bulk load
export async function loadPeople(rows: {id: string; name?: string; knows_id?: string | null}[]) {
  const url = `${VIEWS_API}/graphs/load/csv?write=1`;
  const res = await fetch(url, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ rows }),
  });
  if (!res.ok) throw new Error(`loadPeople failed: ${res.status}`);
  return res.json();
}

export async function exportDossier(opts: {label:string; key:string; value:string; depth?:number; limit?:number}) {
  const params = new URLSearchParams({
    label: opts.label, key: opts.key, value: String(opts.value)
  });
  if (opts.depth != null) params.set("depth", String(opts.depth));
  if (opts.limit != null) params.set("limit", String(opts.limit));
  const res = await fetch(`${VIEWS_API}/graphs/export/dossier?${params.toString()}`);
  if (!res.ok) throw new Error(`export dossier failed: ${res.status}`);
  return res.json();
}
