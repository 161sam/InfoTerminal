export type SearchParamInput = Record<string, unknown> | URLSearchParams | [string, string][];

/**
 * Convert various inputs to a stable URLSearchParams instance.
 * - Filters out undefined/null
 * - Stringifies non-string values
 */
export function toSearchParams(input: SearchParamInput): URLSearchParams {
  if (input instanceof URLSearchParams) return input;
  const params = new URLSearchParams();
  if (Array.isArray(input)) {
    for (const [k, v] of input) params.append(k, String(v));
    return params;
  }
  for (const [key, value] of Object.entries(input || {})) {
    if (value === undefined || value === null) continue;
    if (Array.isArray(value)) {
      value.forEach((v) => params.append(key, String(v)));
    } else {
      params.set(key, String(value));
    }
  }
  return params;
}

