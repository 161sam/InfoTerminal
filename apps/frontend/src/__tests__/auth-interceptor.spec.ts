import { beforeEach, afterEach, describe, expect, it, vi } from "vitest";

let installAuthInterceptor: typeof import("@/lib/auth/interceptor").installAuthInterceptor;
let resetAuthInterceptorForTests: typeof import("@/lib/auth/interceptor").resetAuthInterceptorForTests;

describe("auth interceptor", () => {
  let originalWindow: any;

  beforeEach(async () => {
    originalWindow = globalThis.window;
    (globalThis as any).window = { fetch: vi.fn() };
    vi.resetModules();
    ({ installAuthInterceptor, resetAuthInterceptorForTests } = await import("@/lib/auth/interceptor"));
  });

  afterEach(() => {
    if (resetAuthInterceptorForTests) {
      resetAuthInterceptorForTests();
    }
    if (originalWindow === undefined) {
      delete (globalThis as any).window;
    } else {
      globalThis.window = originalWindow;
    }
  });

  it("does not override fetch when auth is disabled", () => {
    const initialFetch = (window as any).fetch;
    const cleanup = installAuthInterceptor({
      isAuthEnabled: false,
      refresh: async () => true,
      onUnauthorized: () => undefined,
    });
    expect(typeof cleanup).toBe("function");
    expect((window as any).fetch).toBe(initialFetch);
  });

  it("retries the request after a successful refresh", async () => {
    const fetchSpy = vi
      .fn()
      .mockResolvedValueOnce({ status: 401 })
      .mockResolvedValueOnce({ status: 200 });
    const refreshSpy = vi.fn().mockResolvedValue(true);
    const unauthorizedSpy = vi.fn();
    (window as any).fetch = fetchSpy;

    installAuthInterceptor({
      isAuthEnabled: true,
      refresh: refreshSpy,
      onUnauthorized: unauthorizedSpy,
    });

    const response = await (window as any).fetch("/api/data");
    expect(response.status).toBe(200);
    expect(fetchSpy).toHaveBeenCalledTimes(2);
    expect(refreshSpy).toHaveBeenCalledTimes(1);
    expect(unauthorizedSpy).not.toHaveBeenCalled();
  });

  it("triggers logout when refresh fails", async () => {
    const fetchSpy = vi.fn().mockResolvedValue({ status: 401 });
    const refreshSpy = vi.fn().mockResolvedValue(false);
    const unauthorizedSpy = vi.fn();
    (window as any).fetch = fetchSpy;

    installAuthInterceptor({
      isAuthEnabled: true,
      refresh: refreshSpy,
      onUnauthorized: unauthorizedSpy,
    });

    const response = await (window as any).fetch("/api/data");
    expect(response.status).toBe(401);
    expect(fetchSpy).toHaveBeenCalledTimes(1);
    expect(refreshSpy).toHaveBeenCalledTimes(1);
    expect(unauthorizedSpy).toHaveBeenCalledTimes(1);
  });

  it("skips interception when shouldSkip matches", async () => {
    const fetchSpy = vi.fn().mockResolvedValue({ status: 401 });
    const refreshSpy = vi.fn().mockResolvedValue(true);
    (window as any).fetch = fetchSpy;

    installAuthInterceptor({
      isAuthEnabled: true,
      refresh: refreshSpy,
      onUnauthorized: () => undefined,
      shouldSkip: (input) => typeof input === "string" && input.includes("/api/auth/refresh"),
    });

    const response = await (window as any).fetch("/api/auth/refresh");
    expect(response.status).toBe(401);
    expect(fetchSpy).toHaveBeenCalledTimes(1);
    expect(refreshSpy).not.toHaveBeenCalled();
  });
});
