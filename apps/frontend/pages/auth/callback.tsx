import { useEffect, useMemo, useState } from "react";
import Head from "next/head";
import { useRouter } from "next/router";
import { Loader2, ShieldOff } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import { clearOidcRequest, loadOidcRequest } from "@/lib/oidc/client";

interface CallbackState {
  status: "loading" | "success" | "error";
  message: string;
}

export default function OidcCallbackPage() {
  const router = useRouter();
  const { completeLogin } = useAuth();
  const [state, setState] = useState<CallbackState>({
    status: "loading",
    message: "Processing login…",
  });

  const redirectUri = useMemo(() => {
    if (typeof window === "undefined") return null;
    return process.env.NEXT_PUBLIC_OIDC_REDIRECT_URI || `${window.location.origin}/auth/callback`;
  }, []);

  useEffect(() => {
    if (!router.isReady) return;

    const { code, state: returnedState, error, error_description: errorDescription } = router.query;

    if (error) {
      setState({ status: "error", message: String(errorDescription || error) });
      clearOidcRequest();
      return;
    }

    if (typeof code !== "string" || typeof returnedState !== "string") {
      setState({ status: "error", message: "Missing authorization response." });
      clearOidcRequest();
      return;
    }

    const stored = loadOidcRequest();
    if (!stored || stored.state !== returnedState) {
      setState({ status: "error", message: "Login session expired or invalid." });
      clearOidcRequest();
      return;
    }

    if (stored.issuedAt && Date.now() - stored.issuedAt > 10 * 60 * 1000) {
      setState({ status: "error", message: "Login session expired. Please start again." });
      clearOidcRequest();
      return;
    }

    const exchange = async () => {
      try {
        const response = await fetch("/api/auth/oidc/token", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({
            code,
            codeVerifier: stored.codeVerifier,
            redirectUri,
            remember: stored.remember,
          }),
        });

        if (!response.ok) {
          const payload = await response.json().catch(() => ({}));
          throw new Error(payload?.error || "Token exchange failed");
        }

        const data = await response.json();
        completeLogin({
          accessToken: data.accessToken,
          expiresIn: data.expiresIn,
          idToken: data.idToken,
          user: data.user,
        });

        const destination = stored.returnTo || "/";
        setState({ status: "success", message: "Login successful." });
        router.replace(destination);
      } catch (err: any) {
        console.error("OIDC callback failed", err);
        setState({ status: "error", message: err?.message || "Unable to complete login." });
      }
    };

    exchange();
  }, [completeLogin, redirectUri, router]);

  return (
    <>
      <Head>
        <title>Completing sign-in · InfoTerminal</title>
      </Head>
      <main className="flex min-h-screen items-center justify-center bg-slate-50 py-16 dark:bg-slate-950">
        {state.status === "loading" && (
          <div className="flex flex-col items-center gap-3 text-gray-600 dark:text-slate-200">
            <Loader2 className="h-6 w-6 animate-spin" />
            <span>{state.message}</span>
          </div>
        )}
        {state.status === "error" && (
          <div className="flex max-w-md flex-col items-center gap-3 rounded-lg border border-red-200 bg-red-50 p-6 text-center text-red-700 dark:border-red-900/50 dark:bg-red-900/20 dark:text-red-200">
            <ShieldOff className="h-8 w-8" />
            <h1 className="text-lg font-semibold">Login failed</h1>
            <p className="text-sm">{state.message}</p>
            <button
              type="button"
              className="rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
              onClick={() => router.replace("/login")}
            >
              Back to login
            </button>
          </div>
        )}
      </main>
    </>
  );
}
