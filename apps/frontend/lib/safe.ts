export const safe = <T>(v: T | undefined | null, fallback: T): T =>
  v == null ? fallback : v;

export default safe;

