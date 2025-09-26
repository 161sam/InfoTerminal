// Collaboration activity feed panel
import { useState } from "react";
import Image from "next/image";
import {
  Activity,
  MessageSquare,
  FileText,
  CheckCircle,
  UserPlus,
  Clock,
  Filter,
  User,
} from "lucide-react";
import { Workspace, ActivityItem, formatTimestamp } from "@/lib/collaboration/collab-config";

interface CollabActivityPanelProps {
  workspace: Workspace;
  activities?: ActivityItem[];
}

export function CollabActivityPanel({ workspace, activities = [] }: CollabActivityPanelProps) {
  const [filterType, setFilterType] = useState<string>("all");

  const filteredActivities = activities.filter(
    (activity) => filterType === "all" || activity.type === filterType,
  );

  const getActivityIcon = (type: string) => {
    switch (type) {
      case "message":
        return <MessageSquare size={16} className="text-blue-500" />;
      case "task_created":
      case "task_updated":
        return <CheckCircle size={16} className="text-green-500" />;
      case "document_uploaded":
        return <FileText size={16} className="text-purple-500" />;
      case "member_joined":
        return <UserPlus size={16} className="text-orange-500" />;
      default:
        return <Activity size={16} className="text-gray-400" />;
    }
  };

  const getActivityColor = (type: string) => {
    switch (type) {
      case "message":
        return "border-blue-200 bg-blue-50 dark:border-blue-900/30 dark:bg-blue-900/10";
      case "task_created":
      case "task_updated":
        return "border-green-200 bg-green-50 dark:border-green-900/30 dark:bg-green-900/10";
      case "document_uploaded":
        return "border-purple-200 bg-purple-50 dark:border-purple-900/30 dark:bg-purple-900/10";
      case "member_joined":
        return "border-orange-200 bg-orange-50 dark:border-orange-900/30 dark:bg-orange-900/10";
      default:
        return "border-gray-200 bg-gray-50 dark:border-gray-700 dark:bg-gray-800";
    }
  };

  const generateMockActivities = (): ActivityItem[] => {
    // Generate some mock activities for demonstration
    const mockActivities: ActivityItem[] = [
      {
        id: "1",
        workspaceId: workspace.id,
        type: "message",
        description: "sent a message in the workspace",
        actor: workspace.members[0],
        timestamp: new Date(Date.now() - 300000), // 5 minutes ago
      },
      {
        id: "2",
        workspaceId: workspace.id,
        type: "task_created",
        description: 'created a new task "Analyze threat vectors"',
        actor: workspace.members[1],
        timestamp: new Date(Date.now() - 1800000), // 30 minutes ago
      },
      {
        id: "3",
        workspaceId: workspace.id,
        type: "document_uploaded",
        description: "uploaded preliminary-analysis.pdf",
        actor: workspace.members[0],
        timestamp: new Date(Date.now() - 3600000), // 1 hour ago
      },
      {
        id: "4",
        workspaceId: workspace.id,
        type: "member_joined",
        description: "joined the workspace",
        actor: workspace.members[2],
        timestamp: new Date(Date.now() - 86400000), // 1 day ago
      },
    ];
    return mockActivities;
  };

  const displayActivities = activities.length > 0 ? filteredActivities : generateMockActivities();

  if (displayActivities.length === 0) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center">
          <Activity size={48} className="mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">Activity Feed</h3>
          <p className="text-gray-500 dark:text-gray-400">
            Track all workspace activities, updates, and team interactions in real-time.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Activity Feed</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">Recent workspace activity</p>
        </div>
        <button className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
          <Filter size={16} />
        </button>
      </div>

      {/* Activity filter */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
        >
          <option value="all">All Activity</option>
          <option value="message">Messages</option>
          <option value="task_created">Task Created</option>
          <option value="task_updated">Task Updated</option>
          <option value="document_uploaded">Documents</option>
          <option value="member_joined">Member Changes</option>
        </select>
      </div>

      {/* Activity list */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-4 space-y-3">
          {displayActivities.map((activity, index) => (
            <ActivityCard key={activity.id} activity={activity} isFirst={index === 0} />
          ))}
        </div>
      </div>
    </div>
  );
}

interface ActivityCardProps {
  activity: ActivityItem;
  isFirst: boolean;
}

function ActivityCard({ activity, isFirst }: ActivityCardProps) {
  const colorClass = getActivityColor(activity.type);
  const icon = getActivityIcon(activity.type);

  return (
    <div className={`relative p-3 border rounded-lg ${colorClass}`}>
      {/* Timeline line */}
      {!isFirst && (
        <div className="absolute top-0 left-6 w-px h-3 bg-gray-200 dark:bg-gray-600 -mt-3" />
      )}

      <div className="flex items-start gap-3">
        {/* Icon */}
        <div className="flex-shrink-0 w-8 h-8 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-full flex items-center justify-center">
          {icon}
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
                {activity.actor.avatar ? (
                  <Image
                    src={activity.actor.avatar}
                    alt={activity.actor.name}
                    width={24}
                    height={24}
                    className="w-6 h-6 rounded-full object-cover"
                    unoptimized
                  />
                ) : (
                  <User size={12} className="text-primary-600 dark:text-primary-400" />
                )}
              </div>
              <span className="font-medium text-gray-900 dark:text-white text-sm">
                {activity.actor.name}
              </span>
            </div>
            <span className="text-xs text-gray-500 dark:text-gray-400">
              {formatTimestamp(activity.timestamp)}
            </span>
          </div>

          <p className="text-sm text-gray-700 dark:text-gray-300">{activity.description}</p>

          {/* Additional metadata */}
          {activity.metadata && (
            <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
              {Object.entries(activity.metadata).map(([key, value]) => (
                <span key={key} className="mr-3">
                  {key}: {String(value)}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function getActivityColor(type: string): string {
  switch (type) {
    case "message":
      return "border-blue-200 bg-blue-50 dark:border-blue-900/30 dark:bg-blue-900/10";
    case "task_created":
    case "task_updated":
      return "border-green-200 bg-green-50 dark:border-green-900/30 dark:bg-green-900/10";
    case "document_uploaded":
      return "border-purple-200 bg-purple-50 dark:border-purple-900/30 dark:bg-purple-900/10";
    case "member_joined":
      return "border-orange-200 bg-orange-50 dark:border-orange-900/30 dark:bg-orange-900/10";
    default:
      return "border-gray-200 bg-gray-50 dark:border-gray-700 dark:bg-gray-800";
  }
}

function getActivityIcon(type: string) {
  switch (type) {
    case "message":
      return <MessageSquare size={16} className="text-blue-500" />;
    case "task_created":
    case "task_updated":
      return <CheckCircle size={16} className="text-green-500" />;
    case "document_uploaded":
      return <FileText size={16} className="text-purple-500" />;
    case "member_joined":
      return <UserPlus size={16} className="text-orange-500" />;
    default:
      return <Activity size={16} className="text-gray-400" />;
  }
}

export default CollabActivityPanel;
