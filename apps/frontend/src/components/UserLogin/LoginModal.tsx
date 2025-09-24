import React, { useEffect, useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogBody,
} from "@/components/ui/dialog";
import { useAuth } from "@/components/auth/AuthProvider";
import UserManagementPanel from "@/components/settings/UserManagementPanel";
import { Loader2, Shield, ShieldCheck, X } from "lucide-react";

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const LoginModal: React.FC<LoginModalProps> = ({ isOpen, onClose }) => {
  const { user, isAuthenticated, login, loading } = useAuth();
  const [activeView, setActiveView] = useState<"login" | "user">("login");
  const [isStartingLogin, setIsStartingLogin] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const dialogTitle = activeView === "user" ? "User Management" : "Sign in to InfoTerminal";
  const dialogDescription =
    activeView === "user"
      ? "Review your session details and manage account access."
      : "Authenticate to unlock platform features.";

  useEffect(() => {
    if (!isOpen) return;
    const nextView: "login" | "user" = isAuthenticated ? "user" : "login";
    setActiveView(nextView);
    setError(null);
  }, [isAuthenticated, isOpen]);

  const handleLogin = async () => {
    try {
      setIsStartingLogin(true);
      setError(null);
      await login();
    } catch (err: any) {
      setError(err?.message || "Login failed. Please try again.");
    } finally {
      setIsStartingLogin(false);
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
            <div className="space-y-5">
              <p className="text-sm text-gray-600 dark:text-slate-300">
                Start the single sign-on flow to authenticate with your organisation's identity
                provider.
              </p>

              {error && (
                <div className="flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700 dark:border-red-900/40 dark:bg-red-900/20 dark:text-red-300">
                  <Shield className="h-4 w-4" />
                  <span>{error}</span>
                </div>
              )}

              <button
                type="button"
                onClick={handleLogin}
                disabled={isStartingLogin || loading}
                className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-primary-600 px-4 py-3 text-sm font-medium text-white transition hover:bg-primary-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-70"
              >
                {isStartingLogin ? (
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
