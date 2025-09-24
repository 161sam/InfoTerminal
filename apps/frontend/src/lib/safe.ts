export const safe = <T>(v: T | undefined | null, fallback: T): T => (v == null ? fallback : v);

/** Returns true when running in a browser environment. */
export const isBrowser = (): boolean => typeof window !== "undefined";

/** Optional logger that avoids SSR crashes. */
export const safeLog = (...args: any[]) => {
  if (isBrowser()) console.warn(...args);
};

export default safe;
