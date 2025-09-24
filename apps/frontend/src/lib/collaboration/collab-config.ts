// Collaboration workspace types and configuration
export interface Workspace {
  id: string;
  name: string;
  description: string;
  members: WorkspaceMember[];
  isPrivate: boolean;
  createdAt: Date;
  updatedAt: Date;
  pinnedItems: string[];
  color: string;
  documentsCount: number;
  tasksCount: number;
  messagesCount: number;
}

export interface WorkspaceMember {
  id: string;
  name: string;
  email: string;
  role: "owner" | "admin" | "member" | "viewer";
  status: "online" | "away" | "offline";
  avatar?: string;
  lastActive: Date;
}

export interface Message {
  id: string;
  workspaceId: string;
  userId: string;
  userName: string;
  userAvatar?: string;
  content: string;
  type: "text" | "file" | "task" | "system";
  timestamp: Date;
  edited?: boolean;
  editedAt?: Date;
  attachments?: Attachment[];
  mentions?: string[];
  reactions?: Reaction[];
  threadId?: string;
  isThread?: boolean;
}

export interface Attachment {
  id: string;
  name: string;
  type: string;
  size: number;
  url: string;
  thumbnailUrl?: string;
}

export interface Reaction {
  emoji: string;
  users: string[];
  count: number;
}

export interface Task {
  id: string;
  workspaceId: string;
  title: string;
  description?: string;
  status: "todo" | "in_progress" | "review" | "done";
  priority: "low" | "medium" | "high" | "urgent";
  assignee?: WorkspaceMember;
  reporter: WorkspaceMember;
  dueDate?: Date;
  tags: string[];
  attachments: Attachment[];
  comments: Comment[];
  createdAt: Date;
  updatedAt: Date;
}

export interface Comment {
  id: string;
  userId: string;
  userName: string;
  content: string;
  timestamp: Date;
}

export interface Document {
  id: string;
  workspaceId: string;
  name: string;
  type: string;
  size: number;
  url: string;
  uploadedBy: WorkspaceMember;
  uploadedAt: Date;
  tags: string[];
  isShared: boolean;
  comments: Comment[];
}

export interface ActivityItem {
  id: string;
  workspaceId: string;
  type: "message" | "task_created" | "task_updated" | "document_uploaded" | "member_joined";
  description: string;
  actor: WorkspaceMember;
  timestamp: Date;
  metadata?: Record<string, any>;
}

// Configuration constants
export const WORKSPACE_COLORS = {
  red: "bg-red-100 text-red-800 border-red-200 dark:bg-red-900/30 dark:text-red-300 dark:border-red-900/30",
  blue: "bg-blue-100 text-blue-800 border-blue-200 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-900/30",
  green:
    "bg-green-100 text-green-800 border-green-200 dark:bg-green-900/30 dark:text-green-300 dark:border-green-900/30",
  purple:
    "bg-purple-100 text-purple-800 border-purple-200 dark:bg-purple-900/30 dark:text-purple-300 dark:border-purple-900/30",
  orange:
    "bg-orange-100 text-orange-800 border-orange-200 dark:bg-orange-900/30 dark:text-orange-300 dark:border-orange-900/30",
} as const;

export const STATUS_COLORS = {
  online: "bg-green-500",
  away: "bg-yellow-500",
  offline: "bg-gray-400",
} as const;

export const TASK_STATUS_COLORS = {
  todo: "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300",
  in_progress: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
  review: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300",
  done: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
} as const;

export const PRIORITY_COLORS = {
  low: "bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400",
  medium: "bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400",
  high: "bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400",
  urgent: "bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400",
} as const;

// Utility functions
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

export function formatTimestamp(date: Date): string {
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const diffMinutes = Math.floor(diff / (1000 * 60));
  const diffHours = Math.floor(diff / (1000 * 60 * 60));
  const diffDays = Math.floor(diff / (1000 * 60 * 60 * 24));

  if (diffMinutes < 1) return "Just now";
  if (diffMinutes < 60) return `${diffMinutes}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;

  return date.toLocaleDateString();
}

export function getLastActiveText(date: Date): string {
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const diffMinutes = Math.floor(diff / (1000 * 60));
  const diffHours = Math.floor(diff / (1000 * 60 * 60));

  if (diffMinutes < 5) return "Active now";
  if (diffMinutes < 60) return `Active ${diffMinutes}m ago`;
  if (diffHours < 24) return `Active ${diffHours}h ago`;

  return `Active ${date.toLocaleDateString()}`;
}

export function wsUrl(): string {
  const port = process.env.NEXT_PUBLIC_COLLAB_PORT || process.env.IT_PORT_COLLAB || "8625";
  return `ws://localhost:${port}/ws`;
}

// Demo data for development
export const DEMO_WORKSPACES: Workspace[] = [
  {
    id: "1",
    name: "Operation Phoenix",
    description: "High-priority intelligence investigation",
    members: [
      {
        id: "1",
        name: "Dr. Sarah Chen",
        email: "sarah.chen@infoterminal.io",
        role: "owner",
        status: "online",
        lastActive: new Date(),
      },
      {
        id: "2",
        name: "Marcus Rodriguez",
        email: "marcus.r@infoterminal.io",
        role: "admin",
        status: "online",
        lastActive: new Date(Date.now() - 300000),
      },
      {
        id: "3",
        name: "Alex Thompson",
        email: "alex.thompson@infoterminal.io",
        role: "member",
        status: "away",
        lastActive: new Date(Date.now() - 900000),
      },
    ],
    isPrivate: true,
    createdAt: new Date("2024-03-01T10:00:00Z"),
    updatedAt: new Date("2024-03-15T16:30:00Z"),
    pinnedItems: ["msg-1", "task-1"],
    color: "red",
    documentsCount: 12,
    tasksCount: 8,
    messagesCount: 245,
  },
  {
    id: "2",
    name: "Market Analysis Q1",
    description: "Quarterly financial intelligence analysis",
    members: [
      {
        id: "1",
        name: "Dr. Sarah Chen",
        email: "sarah.chen@infoterminal.io",
        role: "member",
        status: "online",
        lastActive: new Date(),
      },
      {
        id: "4",
        name: "Emma Wilson",
        email: "emma.wilson@infoterminal.io",
        role: "owner",
        status: "offline",
        lastActive: new Date(Date.now() - 3600000),
      },
    ],
    isPrivate: false,
    createdAt: new Date("2024-02-15T09:00:00Z"),
    updatedAt: new Date("2024-03-14T11:20:00Z"),
    pinnedItems: [],
    color: "blue",
    documentsCount: 6,
    tasksCount: 4,
    messagesCount: 89,
  },
];

export const DEMO_MESSAGES: Message[] = [
  {
    id: "msg-1",
    workspaceId: "1",
    userId: "1",
    userName: "Dr. Sarah Chen",
    content:
      "I've uploaded the preliminary analysis. The patterns we're seeing suggest a coordinated effort across multiple vectors.",
    type: "text",
    timestamp: new Date("2024-03-15T15:30:00Z"),
    attachments: [
      {
        id: "att-1",
        name: "preliminary-analysis.pdf",
        type: "application/pdf",
        size: 2400000,
        url: "/files/preliminary-analysis.pdf",
      },
    ],
    reactions: [
      { emoji: "👍", users: ["2", "3"], count: 2 },
      { emoji: "🔥", users: ["2"], count: 1 },
    ],
  },
  {
    id: "msg-2",
    workspaceId: "1",
    userId: "2",
    userName: "Marcus Rodriguez",
    content:
      "Agreed. I've cross-referenced this with our threat intelligence feeds. Creating a task to investigate further.",
    type: "text",
    timestamp: new Date("2024-03-15T15:45:00Z"),
    mentions: ["1"],
  },
  {
    id: "msg-3",
    workspaceId: "1",
    userId: "3",
    userName: "Alex Thompson",
    content:
      "The geospatial data from this morning supports that theory. I'll run additional correlation analysis.",
    type: "text",
    timestamp: new Date("2024-03-15T16:00:00Z"),
  },
];
