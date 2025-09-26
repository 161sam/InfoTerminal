// Collaboration workspace list panel
import { useState } from "react";
import { Plus, Search, Users, MessageSquare, FileText, User, Eye } from "lucide-react";
import { Workspace, WORKSPACE_COLORS, STATUS_COLORS } from "@/lib/collaboration/collab-config";

interface CollabWorkspaceListProps {
  workspaces: Workspace[];
  selectedWorkspace?: Workspace;
  onWorkspaceSelect: (workspace: Workspace) => void;
  onCreateWorkspace: () => void;
  isCreating?: boolean;
}

export function CollabWorkspaceList({
  workspaces,
  selectedWorkspace,
  onWorkspaceSelect,
  onCreateWorkspace,
  isCreating = false,
}: CollabWorkspaceListProps) {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredWorkspaces = workspaces.filter(
    (ws) =>
      ws.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      ws.description.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Workspaces</h3>
        <button
          onClick={onCreateWorkspace}
          disabled={isCreating}
          className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Plus size={16} />
          {isCreating ? "Creating..." : "New"}
        </button>
      </div>

      {/* Search */}
      <div className="relative">
        <Search
          className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
          size={16}
        />
        <input
          type="text"
          placeholder="Search workspaces..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
        />
      </div>

      {/* Workspace List */}
      <div className="space-y-2 max-h-[calc(100vh-16rem)] overflow-y-auto">
        {filteredWorkspaces.length === 0 ? (
          <div className="text-center py-8">
            <Users size={32} className="mx-auto text-gray-400 mb-2" />
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {searchTerm ? "No workspaces match your search" : "No workspaces available"}
            </p>
          </div>
        ) : (
          filteredWorkspaces.map((workspace) => (
            <WorkspaceCard
              key={workspace.id}
              workspace={workspace}
              isSelected={selectedWorkspace?.id === workspace.id}
              onSelect={() => onWorkspaceSelect(workspace)}
            />
          ))
        )}
      </div>
    </div>
  );
}

interface WorkspaceCardProps {
  workspace: Workspace;
  isSelected: boolean;
  onSelect: () => void;
}

function WorkspaceCard({ workspace, isSelected, onSelect }: WorkspaceCardProps) {
  const colorClass = WORKSPACE_COLORS[workspace.color as keyof typeof WORKSPACE_COLORS];
  const colorIndicator = colorClass.split(" ")[0]; // Extract just the background color

  return (
    <button
      onClick={onSelect}
      className={`w-full text-left p-3 rounded-lg border transition-colors ${
        isSelected
          ? "bg-primary-50 border-primary-200 dark:bg-primary-900/30 dark:border-primary-900/30"
          : "bg-white border-gray-200 hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
      }`}
    >
      <div className="flex items-start gap-3">
        {/* Color indicator */}
        <div className={`w-3 h-3 rounded-full mt-2 ${colorIndicator}`} />

        <div className="flex-1 min-w-0">
          {/* Workspace name and privacy */}
          <div className="flex items-center gap-2 mb-1">
            <h4 className="font-medium text-gray-900 dark:text-white truncate">{workspace.name}</h4>
            {workspace.isPrivate && (
              <div className="w-4 h-4 text-gray-400">
                <Eye size={12} />
              </div>
            )}
          </div>

          {/* Description */}
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-2 line-clamp-2">
            {workspace.description}
          </p>

          {/* Stats */}
          <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400 mb-2">
            <div className="flex items-center gap-1">
              <Users size={12} />
              {workspace.members.length}
            </div>
            <div className="flex items-center gap-1">
              <MessageSquare size={12} />
              {workspace.messagesCount}
            </div>
            <div className="flex items-center gap-1">
              <FileText size={12} />
              {workspace.documentsCount}
            </div>
          </div>

          {/* Active members preview */}
          <div className="flex items-center gap-1">
            {workspace.members
              .filter((m) => m.status === "online")
              .slice(0, 3)
              .map((member) => (
                <div key={member.id} className="relative">
                  <div className="w-6 h-6 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
                    {member.avatar ? (
                      <NextImage
                        src={member.avatar}
                        alt={member.name}
                        width={24}
                        height={24}
                        className="w-6 h-6 rounded-full object-cover"
                        unoptimized
                      />
                    ) : (
                      <User size={12} className="text-primary-600 dark:text-primary-400" />
                    )}
                  </div>
                  <div
                    className={`absolute -bottom-0.5 -right-0.5 w-2 h-2 rounded-full border border-white dark:border-gray-800 ${STATUS_COLORS[member.status]}`}
                  />
                </div>
              ))}
            {workspace.members.filter((m) => m.status === "online").length > 3 && (
              <div className="text-xs text-gray-400 ml-1">
                +{workspace.members.filter((m) => m.status === "online").length - 3}
              </div>
            )}
          </div>
        </div>
      </div>
    </button>
  );
}

export default CollabWorkspaceList;
import NextImage from "next/image";
