import React from "react";
import Image from "next/image";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/components/auth/AuthProvider";
import { cn } from "@/lib/utils";
import {
  User as UserIcon,
  Mail,
  Shield,
  Key,
  LogOut,
  Settings,
  Clock,
  Phone,
  Building,
  Calendar,
} from "lucide-react";

export interface UserManagementPanelProps {
  /** Visual tweaks for embedding inside a modal vs. full page */
  variant?: "modal" | "page";
  /** Optional close handler for parent controls */
  onRequestClose?: () => void;
  /** Allow hiding the panel header when wrapped by another title */
  showHeader?: boolean;
  className?: string;
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
  className,
}) => {
  const { user, logout, isAuthenticated } = useAuth();

  if (!isAuthenticated || !user) {
    return (
      <div className="text-center py-8">
        <UserIcon className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-slate-100">
          Not authenticated
        </h3>
        <p className="mt-1 text-sm text-gray-500 dark:text-slate-400">
          Please sign in to view user management.
        </p>
      </div>
    );
  }

  const displayName =
    user?.name?.trim() ||
    user?.display_name?.trim() ||
    `${user?.first_name || ""} ${user?.last_name || ""}`.trim() ||
    user?.email?.split("@")[0] ||
    "User";

  const email = user?.email || "user@example.com";
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
      console.error("Sign out failed", error);
    }
  };

  const formatDate = (date?: Date | string) => {
    if (!date) return "Never";
    const d = typeof date === "string" ? new Date(date) : date;
    return d.toLocaleDateString() + " at " + d.toLocaleTimeString();
  };

  const getRoleColor = (role: string) => {
    switch (role.toLowerCase()) {
      case "admin":
      case "administrator":
        return "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300";
      case "security":
        return "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300";
      case "analyst":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300";
      case "viewer":
        return "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300";
    }
  };

  const getStatusColor = (status?: string) => {
    switch (status?.toLowerCase()) {
      case "active":
        return "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300";
      case "inactive":
        return "bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300";
      case "pending":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300";
      case "suspended":
        return "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300";
    }
  };

  return (
    <div className={cn("space-y-6", className)}>
      {showHeader && (
        <div className="border-b border-gray-200 pb-4 dark:border-gray-800">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100">
            User Management
          </h3>
          <p className="mt-1 text-sm text-gray-500 dark:text-slate-400">
            Review profile details and platform access for the current session
          </p>
        </div>
      )}

      {/* User Profile Card */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 dark:bg-gray-900 dark:border-gray-800">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start">
          {/* Avatar */}
          <div className="relative h-16 w-16 shrink-0 overflow-hidden rounded-full bg-primary-600 text-white">
            {user?.avatar_url ? (
              <Image src={user.avatar_url} alt={displayName} width={96} height={96} className="h-full w-full object-cover" unoptimized />
            ) : (
              <div className="flex h-full w-full items-center justify-center text-lg font-semibold">
                {avatarInitials}
              </div>
            )}
          </div>

          {/* User Info */}
          <div className="flex-1 space-y-3">
            <div>
              <h4 className="text-lg font-semibold text-gray-900 dark:text-slate-100">
                {displayName}
              </h4>
              <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-slate-400">
                <Mail className="h-4 w-4" />
                {email}
              </div>
            </div>

            {/* Roles and Status */}
            <div className="flex flex-wrap gap-2">
              {roles.map((role, index) => (
                <Badge key={index} className={cn("text-xs font-medium", getRoleColor(role))}>
                  <Shield className="mr-1 h-3 w-3" />
                  {role}
                </Badge>
              ))}
              {user?.status && (
                <Badge className={cn("text-xs font-medium", getStatusColor(user.status))}>
                  {user.status}
                </Badge>
              )}
            </div>

            {/* Additional Details */}
            <div className="grid grid-cols-1 gap-2 text-sm text-gray-600 dark:text-slate-400 sm:grid-cols-2">
              {user?.phone && (
                <div className="flex items-center gap-2">
                  <Phone className="h-4 w-4" />
                  {user.phone}
                </div>
              )}
              {user?.department && (
                <div className="flex items-center gap-2">
                  <Building className="h-4 w-4" />
                  {user.department}
                </div>
              )}
              {user?.lastLogin && (
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4" />
                  Last login: {formatDate(user.lastLogin)}
                </div>
              )}
              {user?.createdAt && (
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4" />
                  Member since: {formatDate(user.createdAt)}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Permissions */}
      {permissions.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 dark:bg-gray-900 dark:border-gray-800">
          <h5 className="mb-3 font-medium text-gray-900 dark:text-slate-100">Permissions</h5>
          <div className="flex flex-wrap gap-2">
            {permissions.slice(0, 8).map((permission, index) => (
              <Badge key={index} variant="outline" className="text-xs">
                {permission.replace(/[_:]/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())}
              </Badge>
            ))}
            {permissions.length > 8 && (
              <Badge variant="outline" className="text-xs text-gray-500">
                +{permissions.length - 8} more
              </Badge>
            )}
          </div>
        </div>
      )}

      {/* Session Stats */}
      {user?.sessionsCount !== undefined && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 dark:bg-gray-900 dark:border-gray-800">
          <h5 className="mb-3 font-medium text-gray-900 dark:text-slate-100">
            Session Information
          </h5>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-500 dark:text-slate-400">Active Sessions:</span>
              <span className="ml-2 font-medium text-gray-900 dark:text-slate-100">
                {user.sessionsCount}
              </span>
            </div>
            <div>
              <span className="text-gray-500 dark:text-slate-400">Account Status:</span>
              <span className="ml-2 font-medium text-gray-900 dark:text-slate-100">
                {user.is_active ? "Active" : "Inactive"}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex flex-wrap gap-3 pt-4 border-t border-gray-200 dark:border-gray-800">
        <button
          disabled
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-500 bg-gray-100 rounded-lg cursor-not-allowed dark:bg-gray-800 dark:text-slate-400"
          title="Profile editing will be wired once the account API is available"
        >
          <Settings className="h-4 w-4" />
          Edit Profile
        </button>
        <button
          disabled
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-500 bg-gray-100 rounded-lg cursor-not-allowed dark:bg-gray-800 dark:text-slate-400"
          title="Password updates will be enabled once identity endpoints exist"
        >
          <Key className="h-4 w-4" />
          Change Password
        </button>
        <button
          onClick={handleSignOut}
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-500 dark:bg-red-900/20 dark:text-red-400 dark:hover:bg-red-900/30"
          title="Sign out of the current session"
        >
          <LogOut className="h-4 w-4" />
          Sign Out
        </button>
      </div>
    </div>
  );
};

export default UserManagementPanel;
