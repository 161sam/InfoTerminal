// Collaboration team sidebar panel
import { User, Settings, Crown, Shield, UserCheck, Circle } from "lucide-react";
import NextImage from "next/image";
import {
  Workspace,
  WorkspaceMember,
  STATUS_COLORS,
  getLastActiveText,
} from "@/lib/collaboration/collab-config";

interface CollabTeamSidebarProps {
  workspace: Workspace;
  onMemberAction?: (member: WorkspaceMember, action: string) => void;
}

export function CollabTeamSidebar({ workspace, onMemberAction }: CollabTeamSidebarProps) {
  const sortedMembers = [...workspace.members].sort((a, b) => {
    // Sort by status: online > away > offline
    const statusOrder = { online: 0, away: 1, offline: 2 };
    if (statusOrder[a.status] !== statusOrder[b.status]) {
      return statusOrder[a.status] - statusOrder[b.status];
    }
    // Then by role: owner > admin > member > viewer
    const roleOrder = { owner: 0, admin: 1, member: 2, viewer: 3 };
    if (roleOrder[a.role] !== roleOrder[b.role]) {
      return roleOrder[a.role] - roleOrder[b.role];
    }
    // Finally by name
    return a.name.localeCompare(b.name);
  });

  const onlineCount = workspace.members.filter((m) => m.status === "online").length;
  const totalCount = workspace.members.length;

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Team Members</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            {onlineCount} of {totalCount} online
          </p>
        </div>
        <button
          onClick={() => onMemberAction?.(workspace.members[0], "settings")}
          className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
          title="Manage team"
        >
          <Settings size={16} />
        </button>
      </div>

      {/* Member List */}
      <div className="space-y-2 max-h-[calc(100vh-16rem)] overflow-y-auto">
        {sortedMembers.map((member) => (
          <MemberCard
            key={member.id}
            member={member}
            onAction={(action) => onMemberAction?.(member, action)}
          />
        ))}
      </div>

      {/* Workspace Info */}
      <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-500 dark:text-gray-400">Privacy:</span>
            <span className="text-gray-900 dark:text-gray-100">
              {workspace.isPrivate ? "Private" : "Public"}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500 dark:text-gray-400">Created:</span>
            <span className="text-gray-900 dark:text-gray-100">
              {workspace.createdAt.toLocaleDateString()}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500 dark:text-gray-400">Documents:</span>
            <span className="text-gray-900 dark:text-gray-100">{workspace.documentsCount}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500 dark:text-gray-400">Tasks:</span>
            <span className="text-gray-900 dark:text-gray-100">{workspace.tasksCount}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

interface MemberCardProps {
  member: WorkspaceMember;
  onAction: (action: string) => void;
}

function MemberCard({ member, onAction }: MemberCardProps) {
  const getRoleIcon = (role: string) => {
    switch (role) {
      case "owner":
        return <Crown size={12} className="text-yellow-600 dark:text-yellow-400" />;
      case "admin":
        return <Shield size={12} className="text-blue-600 dark:text-blue-400" />;
      case "member":
        return <UserCheck size={12} className="text-green-600 dark:text-green-400" />;
      case "viewer":
        return <Circle size={12} className="text-gray-600 dark:text-gray-400" />;
      default:
        return null;
    }
  };

  const getRoleLabel = (role: string) => {
    switch (role) {
      case "owner":
        return "Owner";
      case "admin":
        return "Admin";
      case "member":
        return "Member";
      case "viewer":
        return "Viewer";
      default:
        return role;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "online":
        return "text-green-600 dark:text-green-400";
      case "away":
        return "text-yellow-600 dark:text-yellow-400";
      case "offline":
        return "text-gray-600 dark:text-gray-400";
      default:
        return "text-gray-600 dark:text-gray-400";
    }
  };

  return (
    <button
      onClick={() => onAction("view")}
      className="w-full text-left p-3 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
    >
      <div className="flex items-start gap-3">
        {/* Avatar */}
        <div className="relative">
          <div className="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
            {member.avatar ? (
              <NextImage
                src={member.avatar}
                alt={member.name}
                width={40}
                height={40}
                className="w-10 h-10 rounded-full object-cover"
                unoptimized
              />
            ) : (
              <User size={20} className="text-primary-600 dark:text-primary-400" />
            )}
          </div>
          {/* Status indicator */}
          <div
            className={`absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full border-2 border-white dark:border-gray-800 ${STATUS_COLORS[member.status]}`}
          />
        </div>

        <div className="flex-1 min-w-0">
          {/* Name and role */}
          <div className="flex items-center gap-2 mb-1">
            <h4 className="font-medium text-gray-900 dark:text-white truncate">{member.name}</h4>
            {getRoleIcon(member.role)}
          </div>

          {/* Email */}
          <p className="text-xs text-gray-500 dark:text-gray-400 truncate mb-1">{member.email}</p>

          {/* Role and status */}
          <div className="flex items-center gap-2 text-xs">
            <span className="text-gray-600 dark:text-gray-300">{getRoleLabel(member.role)}</span>
            <span className="text-gray-400">•</span>
            <span className={getStatusColor(member.status)}>
              {member.status.charAt(0).toUpperCase() + member.status.slice(1)}
            </span>
          </div>

          {/* Last active */}
          <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
            {getLastActiveText(member.lastActive)}
          </p>
        </div>
      </div>
    </button>
  );
}

export default CollabTeamSidebar;
