import { X, Wifi, RefreshCw, PauseCircle, CheckCircle2, AlertTriangle } from "lucide-react";

import { Progress } from "@/components/ui/progress";
import type { ProgressChannel, TaskHistoryEntry, TaskProgressState } from "@/hooks/useTaskProgress";

interface ProgressModalProps {
  isOpen: boolean;
  title: string;
  description?: string;
  state: TaskProgressState;
  onClose?: () => void;
  onCancel?: () => void;
  cancelLabel?: string;
  successLabel?: string;
}

function channelLabel(channel: ProgressChannel): { label: string; icon: JSX.Element } {
  switch (channel) {
    case "websocket":
      return { label: "Live (WebSocket)", icon: <Wifi className="h-4 w-4" /> };
    case "polling":
      return { label: "Polling", icon: <RefreshCw className="h-4 w-4" /> };
    case "simulated":
      return { label: "Simulated", icon: <PauseCircle className="h-4 w-4" /> };
    case "manual":
      return { label: "Manual", icon: <PauseCircle className="h-4 w-4" /> };
    default:
      return { label: "Connecting", icon: <RefreshCw className="h-4 w-4" /> };
  }
}

function statusBadge(status: TaskProgressState["status"]): {
  label: string;
  tone: string;
  icon: JSX.Element;
} {
  switch (status) {
    case "completed":
      return {
        label: "Abgeschlossen",
        tone: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300",
        icon: <CheckCircle2 className="h-4 w-4" />,
      };
    case "failed":
      return {
        label: "Fehlgeschlagen",
        tone: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300",
        icon: <AlertTriangle className="h-4 w-4" />,
      };
    default:
      return {
        label: "Laufend",
        tone: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300",
        icon: <RefreshCw className="h-4 w-4 animate-spin" />,
      };
  }
}

function formatHistory(history: TaskHistoryEntry[]): TaskHistoryEntry[] {
  return [...history].sort((a, b) => b.timestamp - a.timestamp);
}

export function ProgressModal({
  isOpen,
  title,
  description,
  state,
  onClose,
  onCancel,
  cancelLabel = "Abbrechen",
  successLabel = "Schließen",
}: ProgressModalProps) {
  if (!isOpen) return null;

  const status = statusBadge(state.status);
  const channel = channelLabel(state.channel);
  const history = formatHistory(state.history);

  return (
    <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="w-full max-w-xl rounded-xl bg-white dark:bg-gray-900 shadow-xl border border-gray-200 dark:border-gray-700">
        <div className="flex items-start justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-800">
          <div>
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{title}</h2>
            {description && (
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{description}</p>
            )}
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
            aria-label="Close"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="px-6 py-5 space-y-6">
          <div className="flex items-center justify-between">
            <div
              className={`inline-flex items-center gap-2 text-xs font-medium px-3 py-1 rounded-full ${status.tone}`}
            >
              {status.icon}
              <span>{status.label}</span>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-semibold text-gray-900 dark:text-gray-100">
                {Math.round(state.progress)}%
              </span>
              <span className="text-sm text-gray-500 dark:text-gray-400">Fortschritt</span>
            </div>
          </div>

          <Progress value={state.progress} className="h-2" />

          <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
            <div className="flex items-center gap-2">
              {channel.icon}
              <span>{channel.label}</span>
            </div>
            {state.lastUpdate && (
              <span>Letztes Update: {new Date(state.lastUpdate).toLocaleTimeString()}</span>
            )}
          </div>

          {state.message && (
            <div className="rounded-md bg-gray-50 dark:bg-gray-800/60 border border-gray-200 dark:border-gray-700 px-4 py-3 text-sm text-gray-700 dark:text-gray-300">
              {state.message}
            </div>
          )}

          {state.error && (
            <div className="rounded-md bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 px-4 py-3 text-sm text-red-700 dark:text-red-200">
              {state.error}
            </div>
          )}

          <div>
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Verlauf</span>
              <span className="text-xs text-gray-500 dark:text-gray-400">
                {history.length} Ereignis{history.length === 1 ? "" : "se"}
              </span>
            </div>
            <div className="max-h-48 overflow-y-auto rounded-md border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
              {history.length === 0 ? (
                <div className="px-4 py-6 text-sm text-gray-500 dark:text-gray-400 text-center">
                  Noch keine Ereignisse.
                </div>
              ) : (
                <ul className="divide-y divide-gray-200 dark:divide-gray-800">
                  {history.map((entry) => (
                    <li
                      key={entry.id}
                      className="px-4 py-3 text-sm text-gray-700 dark:text-gray-300"
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-medium">
                          {new Date(entry.timestamp).toLocaleTimeString()}
                        </span>
                        <span className="text-xs text-gray-500 dark:text-gray-400">
                          {entry.progress}% · {entry.source}
                        </span>
                      </div>
                      {entry.message && <p className="text-sm">{entry.message}</p>}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>

        <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900/40">
          {onCancel && state.status === "running" && (
            <button
              onClick={onCancel}
              className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
            >
              {cancelLabel}
            </button>
          )}
          {onClose && state.status !== "running" && (
            <button
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-lg"
            >
              {successLabel}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProgressModal;
