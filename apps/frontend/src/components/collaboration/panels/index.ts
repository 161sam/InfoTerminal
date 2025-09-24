// Collaboration panels index - export all components
export { CollabWorkspaceList } from "./CollabWorkspaceList";
export { CollabChatInterface } from "./CollabChatInterface";
export { CollabTeamSidebar } from "./CollabTeamSidebar";
export { CollabDocumentPanel } from "./CollabDocumentPanel";
export { CollabTaskPanel } from "./CollabTaskPanel";
export { CollabActivityPanel } from "./CollabActivityPanel";

// Re-export types and utilities
export type {
  Workspace,
  WorkspaceMember,
  Message,
  Task,
  Document,
  ActivityItem,
  Attachment,
  Reaction,
  Comment,
} from "@/lib/collaboration/collab-config";

export {
  WORKSPACE_COLORS,
  STATUS_COLORS,
  TASK_STATUS_COLORS,
  PRIORITY_COLORS,
  formatFileSize,
  formatTimestamp,
  getLastActiveText,
  wsUrl,
  DEMO_WORKSPACES,
  DEMO_MESSAGES,
} from "@/lib/collaboration/collab-config";
