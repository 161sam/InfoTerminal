import React from "react";
import Panel from "@/components/layout/Panel";
import Button from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/components/auth/AuthProvider";
import { cn } from "@/lib/utils";
import { User as UserIcon, Mail, Shield, Key, LogOut, Settings, Clock } from "lucide-react";

export interface UserManagementPanelProps {
  /** Visual tweaks for embedding inside a modal vs. full page */
  variant?: "modal" | "page";
  /** Optional close handler for parent controls */
  onRequestClose?: () => void;
  /** Allow hiding the panel header when wrapped by another title */
  showHeader?: boolean;
}

function getInitials(name: string) {
  return (
    name
      .split(" ")
      .filter(Boolean)
      .map((part) => part[0]?.toUpperCase() ?? "")
      .join("")
      .slice(0, 2) || "U"
  );
}

const FALLBACK_PERMISSIONS = ["manage:users", "view:analytics", "configure:platform"];
const FALLBACK_ROLES = ["Administrator"];

const UserManagementPanel: React.FC<UserManagementPanelProps> = ({
  variant = "page",
  onRequestClose,
  showHeader = true,
}) => {
  const { user, logout } = useAuth();

  const displayName = user?.name?.trim() || user?.email?.split("@")[0] || "Admin User";
  const email = user?.email || "admin@example.com";
  const roles = (user?.roles && user.roles.length > 0 ? user.roles : FALLBACK_ROLES).map(
    (role) => role || "User",
  );
  const permissions = user?.permissions?.length ? user.permissions : FALLBACK_PERMISSIONS;
  const avatarInitials = getInitials(displayName);

  const handleSignOut = async () => {
    if (!logout) return;
    try {
      await logout();
      onRequestClose?.();
    } catch (error) {
      // eslint-disable-next-line no-console
      console.error("Sign out failed", error);
    }
  };

  return (
    <div className={cn("space-y-4", variant === "modal" && "pr-1")}>
      <Panel
        title={showHeader ? "User Management" : undefined}
        subtitle={
          showHeader
            ? "Review profile details and platform access for the current session"
            : undefined
        }
        footer={
          <div className="flex flex-wrap gap-2">
            <Button
              variant="primary"
              disabled
              title="Profile editing will be wired once the account API is available"
            >
              <Settings size={16} className="mr-2" />
              Edit profile
            </Button>
            <Button
              variant="outline"
              disabled
              title="Password updates will be enabled once identity endpoints exist"
            >
              <Key size={16} className="mr-2" />
              Change password
            </Button>
            <Button variant="ghost" onClick={handleSignOut} title="Sign out of the current session">
              <LogOut size={16} className="mr-2" />
              Sign out
            </Button>
          </div>
        }
        className={cn(variant === "modal" && "shadow-none")}
      >
        <Panel.Body className={cn("space-y-6", !showHeader && "mt-1")}>
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
            <div className="relative h-14 w-14 shrink-0 overflow-hidden rounded-full bg-primary-600 text-white sm:h-16 sm:w-16">
              {user?.avatar ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={user.avatar} alt={displayName} className="h-full w-full object-cover" />
              ) : (
                <div className="flex h-full w-full items-center justify-center text-lg font-semibold">
                  {avatarInitials}
                </div>
              )}
            </div>
            <div className="space-y-2">
              <div>
                <p className="text-lg font-semibold text-gray-900 dark:text-slate-100">
                  {displayName}
                </p>
                <p className="flex items-center gap-2 text-sm text-gray-600 dark:text-slate-400">
                  <Mail size={14} />
                  <span>{email}</span>
                </p>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <Badge variant="secondary">Active session</Badge>
                {roles.map((role) => (
                  <Badge
                    key={role}
                    className="bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-200"
                  >
                    {role}
                  </Badge>
                ))}
              </div>
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div className="rounded-xl border border-gray-200 bg-gray-50 p-4 dark:border-gray-800 dark:bg-gray-900/50">
              <div className="flex items-start gap-3">
                <span className="rounded-lg bg-primary-100 p-2 text-primary-600 dark:bg-primary-900/30 dark:text-primary-300">
                  <Shield size={18} />
                </span>
                <div className="space-y-2">
                  <p className="text-sm font-semibold text-gray-900 dark:text-slate-100">
                    Security posture
                  </p>
                  <p className="text-sm text-gray-600 dark:text-slate-400">
                    Multi-factor authentication and device approvals are pending backend
                    integration.
                  </p>
                  <div className="flex flex-wrap gap-2">
                    <Badge
                      variant="outline"
                      className="border-amber-300 text-amber-700 dark:border-amber-600 dark:text-amber-300"
                    >
                      MFA not configured
                    </Badge>
                    <Badge
                      variant="outline"
                      className="border-gray-300 text-gray-600 dark:border-gray-700 dark:text-slate-300"
                    >
                      Session monitoring enabled
                    </Badge>
                  </div>
                </div>
              </div>
            </div>

            <div className="rounded-xl border border-gray-200 bg-gray-50 p-4 dark:border-gray-800 dark:bg-gray-900/50">
              <div className="flex items-start gap-3">
                <span className="rounded-lg bg-primary-100 p-2 text-primary-600 dark:bg-primary-900/30 dark:text-primary-300">
                  <UserIcon size={18} />
                </span>
                <div className="space-y-2">
                  <p className="text-sm font-semibold text-gray-900 dark:text-slate-100">
                    Roles & permissions
                  </p>
                  <p className="text-sm text-gray-600 dark:text-slate-400">
                    Permissions reflect current policy; additional scopes will appear once connected
                    to the identity service.
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {permissions.map((permission) => (
                      <Badge
                        key={permission}
                        variant="outline"
                        className="border-gray-300 text-gray-700 dark:border-gray-700 dark:text-slate-200"
                      >
                        {permission}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="rounded-xl border border-dashed border-gray-300 p-4 dark:border-gray-700">
            <div className="flex items-start gap-3">
              <span className="rounded-lg bg-primary-100 p-2 text-primary-600 dark:bg-primary-900/30 dark:text-primary-300">
                <Clock size={18} />
              </span>
              <div className="space-y-2">
                <p className="text-sm font-semibold text-gray-900 dark:text-slate-100">
                  Session insights
                </p>
                <p className="text-sm text-gray-600 dark:text-slate-400">
                  Track recent sign-ins, active devices, and revoke tokens when backend telemetry
                  becomes available.
                </p>
              </div>
            </div>
          </div>
        </Panel.Body>
      </Panel>
    </div>
  );
};

export default UserManagementPanel;
