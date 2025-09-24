import React, { FormEvent, useEffect, useMemo, useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogBody,
} from "@/components/ui/dialog";
import { useAuth } from "@/components/auth/AuthProvider";
import UserManagementPanel from "@/components/settings/UserManagementPanel";
import { cn } from "@/lib/utils";
import { AlertCircle, Loader2, Lock, Mail, Shield, X } from "lucide-react";

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const LoginModal: React.FC<LoginModalProps> = ({ isOpen, onClose }) => {
  const { user, isAuthenticated, login, loading } = useAuth();
  const [activeView, setActiveView] = useState<"login" | "user">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const dialogTitle = activeView === "user" ? "User Management" : "Sign in to InfoTerminal";
  const dialogDescription =
    activeView === "user"
      ? "Review your session details and manage account access."
      : "Authenticate to unlock platform features.";

  const defaultEmail = useMemo(() => {
    if (user?.email) return user.email;
    return "";
  }, [user?.email]);

  useEffect(() => {
    if (!isOpen) return;
    const nextView: "login" | "user" = isAuthenticated ? "user" : "login";
    setActiveView(nextView);
    setEmail(defaultEmail);
    setPassword("");
    setError(null);
  }, [defaultEmail, isAuthenticated, isOpen]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!email || !password) {
      setError("Email and password are required.");
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);
      await login(email, password);
      setActiveView("user");
    } catch (err: any) {
      setError(err?.message || "Login failed. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleOpenChange = (next: boolean) => {
    if (!next) {
      onClose();
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleOpenChange}>
      <DialogContent size={activeView === "user" ? "lg" : "md"} className="bg-card p-0">
        <DialogHeader className="flex items-start justify-between gap-4 text-left">
          <div className="flex items-center gap-3">
            <span className="rounded-lg bg-primary-100 p-2 text-primary-600 dark:bg-primary-900/30 dark:text-primary-300">
              <Shield size={20} />
            </span>
            <div className="space-y-1">
              <DialogTitle id="user-auth-title" className="text-base font-semibold">
                {dialogTitle}
              </DialogTitle>
              <p className="text-sm text-gray-500 dark:text-slate-400" id="user-auth-description">
                {dialogDescription}
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="inline-flex h-8 w-8 items-center justify-center rounded-full text-gray-500 transition hover:bg-gray-200 hover:text-gray-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 dark:hover:bg-gray-800"
            aria-label="Close user dialog"
          >
            <X size={16} />
          </button>
        </DialogHeader>

        <DialogBody>
          {activeView === "user" && isAuthenticated ? (
            <UserManagementPanel variant="modal" showHeader={false} onRequestClose={onClose} />
          ) : (
            <form onSubmit={handleSubmit} className="space-y-5" noValidate>
              <div className="space-y-2">
                <label
                  htmlFor="auth-email"
                  className="block text-sm font-medium text-gray-700 dark:text-slate-200"
                >
                  Email address
                </label>
                <div className="relative">
                  <Mail className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
                  <input
                    id="auth-email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    className={cn(
                      "w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm transition focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500 dark:border-gray-700 dark:bg-gray-900 dark:text-slate-100",
                      "placeholder-gray-400",
                    )}
                    placeholder="you@example.com"
                    disabled={isSubmitting || loading}
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label
                  htmlFor="auth-password"
                  className="block text-sm font-medium text-gray-700 dark:text-slate-200"
                >
                  Password
                </label>
                <div className="relative">
                  <Lock className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
                  <input
                    id="auth-password"
                    name="password"
                    type="password"
                    autoComplete="current-password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    className="w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm transition focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500 dark:border-gray-700 dark:bg-gray-900 dark:text-slate-100 placeholder-gray-400"
                    placeholder="••••••••"
                    disabled={isSubmitting || loading}
                    required
                  />
                </div>
              </div>

              {error && (
                <div className="flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700 dark:border-red-900/40 dark:bg-red-900/20 dark:text-red-300">
                  <AlertCircle size={16} className="shrink-0" />
                  <span>{error}</span>
                </div>
              )}

              <button
                type="submit"
                disabled={isSubmitting || loading}
                className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-primary-600 px-4 py-3 text-sm font-medium text-white transition hover:bg-primary-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-70"
              >
                {isSubmitting ? <Loader2 size={18} className="animate-spin" /> : null}
                {isSubmitting ? "Signing in…" : "Sign in"}
              </button>
            </form>
          )}
        </DialogBody>

        {!isAuthenticated && activeView === "login" && (
          <div className="border-t border-gray-200 bg-gray-50 px-6 py-3 text-xs text-gray-500 dark:border-gray-800 dark:bg-gray-900/60 dark:text-slate-400">
            Authentication integrates with the OAuth2/OIDC gateway. Contact your administrator if
            you need access.
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default LoginModal;
