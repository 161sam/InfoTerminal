export const VIEWS_API =
  process.env.NEXT_PUBLIC_VIEWS_API || "http://localhost:8403";

async function handleEnvelopeWithHeaders(res: Response) {
  const requestId = res.headers.get("x-request-id") || undefined;
  if (!res.ok) throw new Error(`HTTP ${res.status}${requestId ? ` (req ${requestId})` : ""}`);
  const j = await res.json();
  if (!j || j.ok !== true) {
    const msg = j?.error?.message || "Request failed";
    throw new Error(requestId ? `${msg} (req ${requestId})` : msg);
  }
  return { data: j.data, counts: j.counts || {}, requestId };
}

export async function getEgo(opts: {label:string; key:string; value:string; depth?:number; limit?:number}) {
  const p = new URLSearchParams({ label: opts.label, key: opts.key, value: String(opts.value) });
  if (opts.depth != null) p.set("depth", String(opts.depth));
  if (opts.limit != null) p.set("limit", String(opts.limit));
  const res = await fetch(`${VIEWS_API}/graphs/view/ego?${p.toString()}`);
  return handleEnvelopeWithHeaders(res);
}

export async function getShortestPath(opts: {srcLabel:string;srcKey:string;srcValue:string;dstLabel:string;dstKey:string;dstValue:string;maxLen?:number}) {
  const p = new URLSearchParams({
    srcLabel: opts.srcLabel, srcKey: opts.srcKey, srcValue: String(opts.srcValue),
    dstLabel: opts.dstLabel, dstKey: opts.dstKey, dstValue: String(opts.dstValue)
  });
  if (opts.maxLen != null) p.set("maxLen", String(opts.maxLen));
  const res = await fetch(`${VIEWS_API}/graphs/view/shortest-path?${p.toString()}`);
  return handleEnvelopeWithHeaders(res);
}

export async function loadPeople(rows: Array<{id:string; name:string; knows_id?:string}>) {
  const res = await fetch(`${VIEWS_API}/graphs/load/csv?write=1`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ rows })
  });
  return handleEnvelopeWithHeaders(res);
}

export async function exportDossier(opts: {label:string; key:string; value:string; depth?:number; limit?:number}) {
  const p = new URLSearchParams({ label: opts.label, key: opts.key, value: String(opts.value) });
  if (opts.depth != null) p.set("depth", String(opts.depth));
  if (opts.limit != null) p.set("limit", String(opts.limit));
  const res = await fetch(`${VIEWS_API}/graphs/export/dossier?${p.toString()}`);
  return handleEnvelopeWithHeaders(res);
}
