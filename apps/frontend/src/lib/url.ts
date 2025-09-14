export type ParamPrimitive = string | number | boolean | null | undefined | Date;
export type ParamValue = ParamPrimitive | ParamPrimitive[];

/**
 * Convert heterogenous values into URLSearchParams.
 * - undefined/null/"" are skipped
 * - boolean/number/Date are converted to strings
 * - arrays yield multiple entries
 */
export function toSearchParams(input: Record<string, ParamValue>): URLSearchParams {
  const params = new URLSearchParams();

  const append = (k: string, v: ParamPrimitive) => {
    if (v === undefined || v === null) return;
    if (v instanceof Date) {
      params.append(k, v.toISOString());
      return;
    }
    const s = String(v);
    if (s.length === 0) return;
    params.append(k, s);
  };

  for (const [k, v] of Object.entries(input)) {
    if (Array.isArray(v)) {
      if (v.length === 0) continue;
      for (const item of v) append(k, item);
    } else {
      append(k, v as ParamPrimitive);
    }
  }

  return params;
}

/** Helper for building router links: returns "?a=b" or "" */
export function toQueryString(input: Record<string, ParamValue>): string {
  const sp = toSearchParams(input);
  const qs = sp.toString();
  return qs ? `?${qs}` : "";
}
