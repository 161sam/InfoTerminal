import { useEffect, useState } from "react";
import Head from "next/head";
import { Loader2, ShieldCheck, ShieldOff } from "lucide-react";
import { useRouter } from "next/router";
import { useAuth } from "@/components/auth/AuthProvider";

export default function LogoutPage() {
  const { logout } = useAuth();
  const router = useRouter();
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");

  useEffect(() => {
    let cancelled = false;
    const run = async () => {
      try {
        await logout();
        if (!cancelled) {
          setStatus("success");
        }
      } catch (error) {
        console.error("Logout failed", error);
        if (!cancelled) {
          setStatus("error");
        }
      }
    };

    run();

    return () => {
      cancelled = true;
    };
  }, [logout]);

  return (
    <>
      <Head>
        <title>Signing out · InfoTerminal</title>
      </Head>
      <main className="flex min-h-screen items-center justify-center bg-slate-50 py-16 dark:bg-slate-950">
        {status === "loading" && (
          <div className="flex flex-col items-center gap-3 text-gray-600 dark:text-slate-200">
            <Loader2 className="h-6 w-6 animate-spin" />
            <span>Signing you out…</span>
          </div>
        )}
        {status === "success" && (
          <div className="flex flex-col items-center gap-3 text-gray-600 dark:text-slate-200">
            <ShieldCheck className="h-8 w-8 text-green-500" />
            <p className="text-sm">You have been signed out.</p>
            <button
              type="button"
              className="rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
              onClick={() => router.replace("/login")}
            >
              Return to login
            </button>
          </div>
        )}
        {status === "error" && (
          <div className="flex flex-col items-center gap-3 text-red-600 dark:text-red-200">
            <ShieldOff className="h-8 w-8" />
            <p className="text-sm">We couldn't complete the logout. Please try again.</p>
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
