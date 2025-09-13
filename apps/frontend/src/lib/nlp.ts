export type Entity = { text: string; label: string; start: number; end: number };

export function highlightText(text: string, ents: Entity[]) {
  const parts: Array<{ t: string; label?: string }> = [];
  let idx = 0;
  const sorted = [...ents].sort((a, b) => a.start - b.start);
  for (const e of sorted) {
    if (e.start > idx) parts.push({ t: text.slice(idx, e.start) });
    parts.push({ t: text.slice(e.start, e.end), label: e.label });
    idx = e.end;
  }
  if (idx < text.length) parts.push({ t: text.slice(idx) });
  return parts;
}
