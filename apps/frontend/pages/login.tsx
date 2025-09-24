import { useEffect } from "react";
import Head from "next/head";
import { useRouter } from "next/router";
import { LoginForm, useAuth } from "@/components/auth/AuthProvider";
import { Loader2 } from "lucide-react";

export default function LoginPage() {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.replace(router.query.returnTo?.toString() || "/");
    }
  }, [isAuthenticated, loading, router]);

  return (
    <>
      <Head>
        <title>Sign in · InfoTerminal</title>
      </Head>
      <main className="flex min-h-screen items-center justify-center bg-slate-50 py-16 dark:bg-slate-950">
        {loading ? (
          <div className="flex flex-col items-center gap-3 text-gray-600 dark:text-slate-200">
            <Loader2 className="h-6 w-6 animate-spin" />
            <span>Checking your session…</span>
          </div>
        ) : isAuthenticated ? (
          <div className="text-gray-600 dark:text-slate-200">Redirecting…</div>
        ) : (
          <LoginForm />
        )}
      </main>
    </>
  );
}
