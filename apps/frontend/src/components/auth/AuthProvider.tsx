// apps/frontend/src/components/auth/AuthProvider.tsx
import React, { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import { useRouter } from "next/router";
import { useNotifications } from "@/lib/notifications";
import type { User } from "@/types/auth";
import {
  clearOidcRequest,
  generatePkcePair,
  generateState,
  storeOidcRequest,
} from "@/lib/oidc/client";
import { Loader2, ShieldCheck } from "lucide-react";

const AUTH_REQUIRED =
  process.env.NEXT_PUBLIC_AUTH_REQUIRED === "1" ||
  process.env.NEXT_PUBLIC_AUTH_REQUIRED?.toLowerCase() === "true";

const GUEST_USER: User = {
  id: "guest",
  email: "guest@local",
  name: "Guest",
  roles: ["guest"],
  permissions: [],
};

const REFRESH_MARGIN_SECONDS = 60;

interface SessionPayload {
  accessToken: string;
  expiresIn: number;
  idToken?: string | null;
  user?: User | null;
}

export interface AuthContextType {
  user: User | null;
  accessToken: string | null;
  idToken: string | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (returnTo?: string) => Promise<void>;
  completeLogin: (session: SessionPayload) => void;
  logout: () => Promise<void>;
  refreshToken: () => Promise<void>;
  hasRole: (role: string) => boolean;
  hasPermission: (permission: string) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const initialUser = AUTH_REQUIRED ? null : GUEST_USER;

const logMissingProvider = () => {
  if (process.env.NODE_ENV !== "production") {
    console.warn("useAuth called outside of AuthProvider – returning guest session");
  }
};

const defaultAuthContext: AuthContextType = {
  user: initialUser,
  accessToken: null,
  idToken: null,
  loading: false,
  isAuthenticated: Boolean(initialUser),
  login: async () => {
    logMissingProvider();
  },
  completeLogin: () => {
    logMissingProvider();
  },
  logout: async () => {
    logMissingProvider();
  },
  refreshToken: async () => {
    logMissingProvider();
  },
  hasRole: () => false,
  hasPermission: () => false,
};

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(initialUser);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [idToken, setIdToken] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(AUTH_REQUIRED);
  const router = useRouter();
  const notifications = useNotifications();

  const refreshTimer = useRef<NodeJS.Timeout | null>(null);
  const refreshSessionRef = useRef<() => Promise<void>>(async () => Promise.resolve());

  const clearSession = useCallback(() => {
    if (refreshTimer.current) {
      clearTimeout(refreshTimer.current);
      refreshTimer.current = null;
    }
    setAccessToken(null);
    setIdToken(null);
    setUser(AUTH_REQUIRED ? null : GUEST_USER);
    setLoading(false);
  }, []);

  const scheduleRefresh = useCallback((expiresIn: number) => {
    if (!AUTH_REQUIRED) return;
    if (!expiresIn || Number.isNaN(expiresIn)) return;
    if (refreshTimer.current) {
      clearTimeout(refreshTimer.current);
    }
    const delaySeconds = Math.max(expiresIn - REFRESH_MARGIN_SECONDS, 30);
    refreshTimer.current = setTimeout(() => {
      refreshSessionRef.current().catch((error) => console.warn("Token refresh failed", error));
    }, delaySeconds * 1000);
  }, []);

  const applySession = useCallback(
    (session: SessionPayload) => {
      setAccessToken(session.accessToken);
      setIdToken(session.idToken ?? null);
      setUser(session.user ?? null);
      setLoading(false);
      scheduleRefresh(session.expiresIn);
      clearOidcRequest();
    },
    [scheduleRefresh],
  );

  const refreshToken = useCallback(async () => {
    if (!AUTH_REQUIRED) return;
    try {
      const response = await fetch("/api/auth/refresh", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
      });

      if (!response.ok) {
        if (response.status === 401) {
          clearSession();
        }
        const errorBody = await response.json().catch(() => ({}));
        throw new Error(errorBody?.error || "Token refresh failed");
      }

      const data = await response.json();
      applySession(data);
    } catch (error) {
      console.error("Token refresh failed:", error);
      clearSession();
    }
  }, [applySession, clearSession]);

  refreshSessionRef.current = refreshToken;

  const checkAuth = useCallback(async () => {
    if (!AUTH_REQUIRED) {
      setUser(GUEST_USER);
      setLoading(false);
      return;
    }
    try {
      const response = await fetch("/api/auth/session", {
        method: "GET",
        credentials: "include",
      });

      if (!response.ok) {
        clearSession();
        return;
      }

      const data = await response.json();
      applySession(data);
    } catch (error) {
      console.error("Auth check failed:", error);
      clearSession();
    }
  }, [applySession, clearSession]);

  useEffect(() => {
    checkAuth();
    return () => {
      if (refreshTimer.current) {
        clearTimeout(refreshTimer.current);
      }
    };
  }, [checkAuth]);

  const login = useCallback(
    async (returnTo?: string) => {
      if (!AUTH_REQUIRED) {
        const target = returnTo || router.asPath || "/";
        router.push(target);
        return;
      }
      if (typeof window === "undefined") return;

      try {
        const response = await fetch("/api/auth/oidc/config");
        if (!response.ok) {
          throw new Error("Failed to load OIDC configuration");
        }
        const config = await response.json();
        const { codeVerifier, codeChallenge } = await generatePkcePair();
        const state = generateState();
        const redirectUri = config.redirectUri as string;

        storeOidcRequest({
          codeVerifier,
          state,
          returnTo: returnTo || router.asPath,
        });

        const params = new URLSearchParams({
          response_type: "code",
          client_id: config.clientId,
          redirect_uri: redirectUri,
          scope: config.scope || "openid profile email",
          code_challenge: codeChallenge,
          code_challenge_method: "S256",
          state,
        });

        const authorizationEndpoint =
          config.authorizationEndpoint || `${config.issuer}/protocol/openid-connect/auth`;

        window.location.href = `${authorizationEndpoint}?${params.toString()}`;
      } catch (error: any) {
        console.error("Failed to start login", error);
        notifications.error("Login failed", error?.message || "Unable to start login flow");
        clearOidcRequest();
      }
    },
    [notifications, router],
  );

  const completeLogin = useCallback(
    (session: SessionPayload) => {
      applySession(session);
    },
    [applySession],
  );

  const logout = useCallback(async () => {
    if (typeof window === "undefined") return;
    try {
      const response = await fetch("/api/auth/logout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ idToken }),
      });
      const data = response.ok ? await response.json() : null;
      clearSession();
      notifications.info("Logged out", "You have been signed out");
      if (data?.endSessionUrl) {
        window.location.href = data.endSessionUrl as string;
        return;
      }
      router.push("/login");
    } catch (error) {
      console.error("Logout error:", error);
      clearSession();
      router.push("/login");
    } finally {
      clearOidcRequest();
    }
  }, [idToken, clearSession, notifications, router]);

  const hasRole = useCallback(
    (role: string) => {
      return Boolean(user?.roles?.includes(role));
    },
    [user?.roles],
  );

  const hasPermission = useCallback(
    (permission: string) => {
      return Boolean(user?.permissions?.includes(permission));
    },
    [user?.permissions],
  );

  const value: AuthContextType = {
    user,
    accessToken,
    idToken,
    loading,
    isAuthenticated: !!user,
    login,
    completeLogin,
    logout,
    refreshToken,
    hasRole,
    hasPermission,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    return defaultAuthContext;
  }
  return context;
}

export function LoginForm() {
  const { login } = useAuth();
  const [starting, setStarting] = useState(false);

  const handleLogin = async () => {
    try {
      setStarting(true);
      await login();
    } finally {
      setStarting(false);
    }
  };

  return (
    <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">Sign in</h2>
        <p className="text-gray-600 dark:text-gray-400">
          Use your organisation single sign-on to access InfoTerminal.
        </p>
      </div>

      <button
        type="button"
        onClick={handleLogin}
        disabled={starting}
        className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {starting ? (
          <>
            <Loader2 size={18} className="animate-spin" />
            Redirecting…
          </>
        ) : (
          <>
            <ShieldCheck size={18} />
            Continue with SSO
          </>
        )}
      </button>
    </div>
  );
}

export function RegisterForm() {
  return (
    <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 text-center space-y-4">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
        Provisioned by your administrator
      </h2>
      <p className="text-gray-600 dark:text-gray-400">
        Accounts are managed centrally via the identity provider. Contact your platform
        administrator to request access or role updates.
      </p>
    </div>
  );
}

export type { SessionPayload as AuthSessionPayload };
