export type EntityLabel =
  | 'Person'
  | 'Organization'
  | 'Location'
  | 'Email'
  | 'Domain'
  | 'IP'
  | 'Misc';

export const ENTITY_COLORS: Record<EntityLabel, string> = {
  Person: 'bg-blue-100 text-blue-800',
  Organization: 'bg-purple-100 text-purple-800',
  Location: 'bg-emerald-100 text-emerald-800',
  Email: 'bg-amber-100 text-amber-800',
  Domain: 'bg-indigo-100 text-indigo-800',
  IP: 'bg-rose-100 text-rose-800',
  Misc: 'bg-slate-100 text-slate-800',
};

/** Normalize various NER labels into the set of supported EntityLabel values. */
export function normalizeLabel(x: string): EntityLabel {
  const s = x.trim().toLowerCase();
  switch (s) {
    case 'per':
    case 'pers':
    case 'person':
    case 'human':
      return 'Person';
    case 'org':
    case 'organization':
    case 'organisation':
    case 'company':
    case 'corporation':
      return 'Organization';
    case 'loc':
    case 'location':
    case 'place':
    case 'geo':
      return 'Location';
    case 'email':
    case 'e-mail':
    case 'mail':
      return 'Email';
    case 'domain':
    case 'url':
    case 'hostname':
    case 'site':
      return 'Domain';
    case 'ip':
    case 'ipv4':
    case 'ipv6':
    case 'ipaddress':
      return 'IP';
    default:
      return 'Misc';
  }
}

export function displayValue(v: string): string {
  return (v || '').trim();
}

/**
 * Deduplicate a list of entities by normalised label and case-insensitive value.
 * Returns a sorted array (by label then value) including a count for each entry.
 */
export function uniqueEntities(
  ents: { label: string; value: string }[],
): { label: EntityLabel; value: string; count: number }[] {
  const map = new Map<string, { label: EntityLabel; value: string; count: number }>();
  for (const e of ents) {
    const label = normalizeLabel(e.label);
    const value = displayValue(e.value);
    if (!value) continue;
    const key = `${label}:${value.toLowerCase()}`;
    const existing = map.get(key);
    if (existing) existing.count += 1;
    else map.set(key, { label, value, count: 1 });
  }
  return Array.from(map.values()).sort((a, b) => {
    if (a.label === b.label) return a.value.localeCompare(b.value);
    return a.label.localeCompare(b.label);
  });
}

