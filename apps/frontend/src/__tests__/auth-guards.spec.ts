import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";

const refreshWithTokenMock = vi.fn();
const setRefreshCookieMock = vi.fn();
const clearAuthCookiesMock = vi.fn();

vi.mock("@/server/oidc", () => ({
  refreshWithToken: refreshWithTokenMock,
  setRefreshCookie: setRefreshCookieMock,
  clearAuthCookies: clearAuthCookiesMock,
  REMEMBER_COOKIE_NAME: "it_remember_me",
}));

function createContext(overrides: Partial<any> = {}) {
  const resHeaders: Record<string, string | string[]> = {};
  return {
    req: { cookies: {}, ...overrides.req },
    res: {
      setHeader: vi.fn((name: string, value: any) => {
        resHeaders[name] = value;
      }),
      getHeader: vi.fn((name: string) => resHeaders[name]),
      ...overrides.res,
    },
    resolvedUrl: "/",
    query: {},
    ...overrides,
  };
}

describe("withAuthGuard", () => {
  beforeEach(() => {
    vi.resetModules();
    refreshWithTokenMock.mockReset();
    setRefreshCookieMock.mockReset();
    clearAuthCookiesMock.mockReset();
    delete process.env.NEXT_PUBLIC_AUTH_REQUIRED;
  });

  afterEach(() => {
    delete process.env.NEXT_PUBLIC_AUTH_REQUIRED;
  });

  it("skips checks when auth is disabled", async () => {
    process.env.NEXT_PUBLIC_AUTH_REQUIRED = "0";
    const { withAuthGuard } = await import("@/server/guards/auth");
    const result = await withAuthGuard()(createContext());
    expect(result).toEqual({ props: {} });
    expect(refreshWithTokenMock).not.toHaveBeenCalled();
  });

  it("redirects to login when refresh token cookie is missing", async () => {
    process.env.NEXT_PUBLIC_AUTH_REQUIRED = "true";
    const { withAuthGuard } = await import("@/server/guards/auth");
    const context = createContext({ resolvedUrl: "/search" });
    const result = await withAuthGuard()(context as any);
    expect(result).toEqual({
      redirect: {
        destination: "/login?returnTo=%2Fsearch",
        permanent: false,
      },
    });
    expect(refreshWithTokenMock).not.toHaveBeenCalled();
  });

  it("refreshes the session and forwards handler props", async () => {
    process.env.NEXT_PUBLIC_AUTH_REQUIRED = "true";
    refreshWithTokenMock.mockResolvedValue({ refresh_token: "next", refresh_expires_in: 120 });
    const { withAuthGuard } = await import("@/server/guards/auth");
    const context = createContext({
      req: { cookies: { refresh_token: "abc" } },
      resolvedUrl: "/graphx",
    });

    const guard = withAuthGuard(async () => ({ props: { ready: true } }));
    const result = await guard(context as any);

    expect(refreshWithTokenMock).toHaveBeenCalledWith("abc");
    expect(setRefreshCookieMock).toHaveBeenCalledWith(
      context.res,
      "next",
      120,
      expect.objectContaining({ remember: false }),
    );
    expect(result).toEqual({ props: { ready: true } });
  });

  it("respects remember-me cookie when refreshing", async () => {
    process.env.NEXT_PUBLIC_AUTH_REQUIRED = "true";
    refreshWithTokenMock.mockResolvedValue({ refresh_token: "token", refresh_expires_in: 3600 });
    const { withAuthGuard } = await import("@/server/guards/auth");
    const context = createContext({
      req: { cookies: { refresh_token: "seed", it_remember_me: "1" } },
      resolvedUrl: "/dossier",
    });

    const result = await withAuthGuard()(context as any);

    expect(setRefreshCookieMock).toHaveBeenCalledWith(
      context.res,
      "token",
      3600,
      expect.objectContaining({ remember: true }),
    );
    expect(result).toEqual({ props: {} });
  });

  it("clears cookies and redirects when refresh fails", async () => {
    process.env.NEXT_PUBLIC_AUTH_REQUIRED = "true";
    refreshWithTokenMock.mockRejectedValue(new Error("boom"));
    const { withAuthGuard } = await import("@/server/guards/auth");
    const context = createContext({
      req: { cookies: { refresh_token: "bad" } },
      resolvedUrl: "/settings",
    });

    const result = await withAuthGuard()(context as any);

    expect(clearAuthCookiesMock).toHaveBeenCalledWith(context.res);
    expect(result).toEqual({
      redirect: {
        destination: "/login?returnTo=%2Fsettings",
        permanent: false,
      },
    });
  });
});
