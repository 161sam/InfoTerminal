// Collaboration task management panel
import { useState } from "react";
import {
  CheckCircle,
  Plus,
  Search,
  Filter,
  Calendar,
  User,
  Clock,
  AlertCircle,
  Circle,
  MoreVertical,
} from "lucide-react";
import {
  Workspace,
  Task,
  TASK_STATUS_COLORS,
  PRIORITY_COLORS,
} from "@/lib/collaboration/collab-config";

interface CollabTaskPanelProps {
  workspace: Workspace;
  tasks?: Task[];
  onCreateTask?: () => void;
  onTaskAction?: (task: Task, action: string) => void;
}

export function CollabTaskPanel({
  workspace,
  tasks = [],
  onCreateTask,
  onTaskAction,
}: CollabTaskPanelProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [priorityFilter, setPriorityFilter] = useState<string>("all");

  const filteredTasks = tasks.filter((task) => {
    const matchesSearch =
      task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      task.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === "all" || task.status === statusFilter;
    const matchesPriority = priorityFilter === "all" || task.priority === priorityFilter;

    return matchesSearch && matchesStatus && matchesPriority;
  });

  const tasksByStatus = {
    todo: filteredTasks.filter((t) => t.status === "todo"),
    in_progress: filteredTasks.filter((t) => t.status === "in_progress"),
    review: filteredTasks.filter((t) => t.status === "review"),
    done: filteredTasks.filter((t) => t.status === "done"),
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "todo":
        return <Circle size={16} className="text-gray-400" />;
      case "in_progress":
        return <Clock size={16} className="text-blue-500" />;
      case "review":
        return <AlertCircle size={16} className="text-yellow-500" />;
      case "done":
        return <CheckCircle size={16} className="text-green-500" />;
      default:
        return <Circle size={16} className="text-gray-400" />;
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case "todo":
        return "To Do";
      case "in_progress":
        return "In Progress";
      case "review":
        return "Review";
      case "done":
        return "Done";
      default:
        return status;
    }
  };

  const getPriorityLabel = (priority: string) => {
    switch (priority) {
      case "low":
        return "Low";
      case "medium":
        return "Medium";
      case "high":
        return "High";
      case "urgent":
        return "Urgent";
      default:
        return priority;
    }
  };

  if (tasks.length === 0) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center">
          <CheckCircle size={48} className="mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
            Task Management
          </h3>
          <p className="text-gray-500 dark:text-gray-400 mb-4">
            Create and track tasks within your workspace for better project coordination.
          </p>
          <button
            onClick={onCreateTask}
            className="inline-flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            <Plus size={16} />
            Create Task
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Tasks</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">{filteredTasks.length} tasks</p>
        </div>
        <button
          onClick={onCreateTask}
          className="inline-flex items-center gap-2 px-3 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700"
        >
          <Plus size={16} />
          New Task
        </button>
      </div>

      {/* Search and filters */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="space-y-3">
          <div className="relative">
            <Search
              className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
              size={16}
            />
            <input
              type="text"
              placeholder="Search tasks..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
            />
          </div>

          <div className="flex gap-3">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
            >
              <option value="all">All Status</option>
              <option value="todo">To Do</option>
              <option value="in_progress">In Progress</option>
              <option value="review">Review</option>
              <option value="done">Done</option>
            </select>

            <select
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
            >
              <option value="all">All Priority</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>
        </div>
      </div>

      {/* Task board */}
      <div className="flex-1 overflow-hidden">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-4 h-full">
          {Object.entries(tasksByStatus).map(([status, statusTasks]) => (
            <div key={status} className="flex flex-col">
              <div className="flex items-center gap-2 mb-3">
                {getStatusIcon(status)}
                <h4 className="font-medium text-gray-900 dark:text-white">
                  {getStatusLabel(status)}
                </h4>
                <span className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full dark:bg-gray-700 dark:text-gray-400">
                  {statusTasks.length}
                </span>
              </div>

              <div className="space-y-2 flex-1 overflow-y-auto">
                {statusTasks.map((task) => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onAction={(action) => onTaskAction?.(task, action)}
                  />
                ))}

                {statusTasks.length === 0 && (
                  <div className="text-center py-8 text-gray-400 dark:text-gray-500 text-sm">
                    No {getStatusLabel(status).toLowerCase()} tasks
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

interface TaskCardProps {
  task: Task;
  onAction: (action: string) => void;
}

function TaskCard({ task, onAction }: TaskCardProps) {
  const statusClass = TASK_STATUS_COLORS[task.status];
  const priorityClass = PRIORITY_COLORS[task.priority];

  const isOverdue = task.dueDate && new Date(task.dueDate) < new Date();

  return (
    <div className="p-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-md transition-shadow cursor-pointer">
      <div className="flex items-start justify-between mb-2">
        <h5
          className="font-medium text-gray-900 dark:text-white text-sm line-clamp-2 flex-1"
          onClick={() => onAction("view")}
        >
          {task.title}
        </h5>
        <button
          onClick={() => onAction("menu")}
          className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded"
        >
          <MoreVertical size={14} />
        </button>
      </div>

      {task.description && (
        <p className="text-xs text-gray-500 dark:text-gray-400 mb-2 line-clamp-2">
          {task.description}
        </p>
      )}

      <div className="flex items-center gap-2 mb-2">
        <span className={`px-2 py-1 text-xs rounded-full ${priorityClass}`}>
          {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
        </span>
        {task.tags.slice(0, 2).map((tag, index) => (
          <span
            key={index}
            className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full dark:bg-blue-900/30 dark:text-blue-300"
          >
            {tag}
          </span>
        ))}
      </div>

      <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
        <div className="flex items-center gap-1">
          {task.assignee ? (
            <>
              <User size={12} />
              <span>{task.assignee.name}</span>
            </>
          ) : (
            <span>Unassigned</span>
          )}
        </div>

        {task.dueDate && (
          <div
            className={`flex items-center gap-1 ${isOverdue ? "text-red-500 dark:text-red-400" : ""}`}
          >
            <Calendar size={12} />
            <span>{task.dueDate.toLocaleDateString()}</span>
          </div>
        )}
      </div>

      {task.attachments.length > 0 && (
        <div className="mt-2 text-xs text-gray-400">
          {task.attachments.length} attachment{task.attachments.length !== 1 ? "s" : ""}
        </div>
      )}
    </div>
  );
}

export default CollabTaskPanel;
