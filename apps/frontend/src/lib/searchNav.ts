import { ParsedUrlQuery } from 'querystring';
import { EntityLabel } from './entities';

export function buildSearchUrl(
  currentQuery: ParsedUrlQuery,
  opts: {
    addEntity?: EntityLabel;
    addValue?: string;
    remove?: { entity?: EntityLabel; value?: string };
  },
): string {
  const q: Record<string, any> = { ...currentQuery };
  const arr = (key: string) => {
    const v = q[key];
    return Array.isArray(v) ? [...v] : v ? [v] : [];
  };
  if (opts.addEntity) {
    const list = arr('entity');
    if (!list.includes(opts.addEntity)) list.push(opts.addEntity);
    q.entity = list;
    delete q.page;
  }
  if (opts.addValue) {
    const list = arr('value');
    if (!list.includes(opts.addValue)) list.push(opts.addValue);
    q.value = list;
    delete q.page;
  }
  if (opts.remove?.entity) {
    const list = arr('entity').filter((e) => e !== opts.remove?.entity);
    if (list.length) q.entity = list;
    else delete q.entity;
  }
  if (opts.remove?.value) {
    const list = arr('value').filter((v) => v !== opts.remove?.value);
    if (list.length) q.value = list;
    else delete q.value;
  }
  const search = new URLSearchParams();
  Object.entries(q).forEach(([k, v]) => {
    if (v === undefined) return;
    if (Array.isArray(v)) v.forEach((val) => search.append(k, String(val)));
    else search.set(k, String(v));
  });
  return `/search?${search.toString()}`;
}

