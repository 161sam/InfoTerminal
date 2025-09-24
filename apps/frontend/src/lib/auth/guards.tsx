import { useEffect, useMemo, useRef } from "react";
import { useRouter } from "next/router";
import { useAuth } from "@/components/auth/AuthProvider";

const AUTH_REQUIRED =
  process.env.NEXT_PUBLIC_AUTH_REQUIRED === "1" ||
  process.env.NEXT_PUBLIC_AUTH_REQUIRED?.toLowerCase() === "true";

export type ProtectedRouteStatus = "open" | "checking" | "authenticated" | "redirecting";

function isAuthRoute(pathname: string) {
  return pathname === "/login" || pathname.startsWith("/auth/");
}

export function useProtectedRoute(): ProtectedRouteStatus {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();
  const redirecting = useRef(false);

  useEffect(() => {
    if (!AUTH_REQUIRED) return;
    if (loading || isAuthenticated) {
      redirecting.current = false;
      return;
    }
    if (redirecting.current) {
      return;
    }

    if (isAuthRoute(router.pathname)) {
      return;
    }

    redirecting.current = true;
    const returnTo = router.asPath && router.asPath !== "/" ? router.asPath : "/";
    const query = returnTo && returnTo !== "/login" ? { returnTo } : undefined;

    router.replace({ pathname: "/login", query }).catch(() => {
      redirecting.current = false;
    });
  }, [isAuthenticated, loading, router]);

  return useMemo<ProtectedRouteStatus>(() => {
    if (!AUTH_REQUIRED) {
      return "open";
    }
    if (loading) {
      return "checking";
    }
    if (isAuthenticated) {
      return "authenticated";
    }
    return "redirecting";
  }, [isAuthenticated, loading]);
}
