import { useCallback, useEffect, useRef, useState } from "react";

import { wsUrl } from "@/lib/collaboration/collab-config";

export type ProgressChannel = "websocket" | "polling" | "simulated" | "manual" | "none";

export interface ProgressMessage {
  type?: string;
  case_id?: string;
  caseId?: string;
  job_id?: string;
  jobId?: string;
  status?: string;
  message?: string;
  progress?: number;
  [key: string]: unknown;
}

export interface TaskHistoryEntry {
  id: string;
  timestamp: number;
  progress: number;
  message?: string;
  status: TaskProgressState["status"];
  source: ProgressChannel;
}

export interface TaskProgressState {
  progress: number;
  status: "idle" | "running" | "completed" | "failed";
  message?: string;
  channel: ProgressChannel;
  history: TaskHistoryEntry[];
  error?: string;
  lastUpdate?: number;
}

export interface UseTaskProgressOptions {
  active: boolean;
  taskId: string | null;
  eventType: string;
  matchEvent?: (event: ProgressMessage, taskId: string) => boolean;
  pollInterval?: number;
  poller?: () => Promise<ProgressMessage | null>;
  fallbackDurationMs?: number;
}

export interface UseTaskProgressResult {
  state: TaskProgressState;
  setManualProgress: (progress: number, status?: string, message?: string) => void;
  addManualEvent: (message: string, status?: string) => void;
  reset: () => void;
}

const DEFAULT_POLL_INTERVAL = 2000;
const SIMULATION_STEP_MS = 900;

function defaultMatch(event: ProgressMessage, taskId: string): boolean {
  const caseId = event.case_id ?? event.caseId;
  const jobId = event.job_id ?? event.jobId;
  if (caseId && typeof caseId === "string") {
    return caseId === taskId;
  }
  if (jobId && typeof jobId === "string") {
    return jobId === taskId;
  }
  return false;
}

function isFailureStatus(status?: string): boolean {
  if (!status) return false;
  const lowered = status.toLowerCase();
  return lowered.includes("fail") || lowered.includes("error") || lowered.includes("abort");
}

function isCompletionStatus(status?: string): boolean {
  if (!status) return false;
  const lowered = status.toLowerCase();
  return (
    lowered.includes("complete") ||
    lowered.includes("success") ||
    lowered.includes("done") ||
    lowered === "finished"
  );
}

function normaliseStatus(
  incomingStatus: string | undefined,
  progress: number,
  previous: TaskProgressState["status"],
): TaskProgressState["status"] {
  if (isFailureStatus(incomingStatus)) {
    return "failed";
  }
  if (isCompletionStatus(incomingStatus) || progress >= 100) {
    return "completed";
  }
  if (previous === "idle") {
    return "running";
  }
  return incomingStatus ? "running" : previous;
}

function eventSuggestsCompletion(event: ProgressMessage): boolean {
  if (typeof event.progress === "number" && event.progress >= 100) {
    return true;
  }
  return isCompletionStatus(event.status);
}

function eventSuggestsFailure(event: ProgressMessage): boolean {
  return isFailureStatus(event.status);
}

export function useTaskProgress(options: UseTaskProgressOptions): UseTaskProgressResult {
  const {
    active,
    taskId,
    eventType,
    matchEvent,
    pollInterval,
    poller,
    fallbackDurationMs = 8000,
  } = options;

  const [state, setState] = useState<TaskProgressState>({
    progress: 0,
    status: "idle",
    message: undefined,
    channel: "none",
    history: [],
    error: undefined,
    lastUpdate: undefined,
  });

  const wsRef = useRef<WebSocket | null>(null);
  const fallbackTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const stopConnections = useCallback(() => {
    if (wsRef.current) {
      try {
        wsRef.current.onopen = null;
        wsRef.current.onmessage = null;
        wsRef.current.onerror = null;
        wsRef.current.onclose = null;
        wsRef.current.close();
      } catch {
        // Ignore network errors during shutdown
      }
      wsRef.current = null;
    }
    if (fallbackTimerRef.current) {
      clearInterval(fallbackTimerRef.current);
      fallbackTimerRef.current = null;
    }
  }, []);

  const pushEvent = useCallback((event: ProgressMessage, source: ProgressChannel) => {
    setState((prev) => {
      const nextProgress =
        typeof event.progress === "number"
          ? Math.max(0, Math.min(100, Math.round(event.progress)))
          : prev.progress;
      const status = normaliseStatus(event.status, nextProgress, prev.status);
      const message = event.message ?? prev.message;
      const entry: TaskHistoryEntry = {
        id: `${source}-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`,
        timestamp: Date.now(),
        progress: nextProgress,
        message,
        status,
        source,
      };
      const history = [...prev.history, entry].slice(-10);
      return {
        progress: nextProgress,
        status,
        message,
        channel:
          source === "manual"
            ? prev.channel
            : source === "websocket"
              ? "websocket"
              : source === "polling"
                ? "polling"
                : source === "simulated"
                  ? "simulated"
                  : prev.channel,
        history,
        error:
          status === "failed"
            ? ((event.message as string | undefined) ?? prev.error ?? "Task failed")
            : status === "completed"
              ? undefined
              : prev.error,
        lastUpdate: Date.now(),
      };
    });
  }, []);

  const reset = useCallback(() => {
    setState({
      progress: 0,
      status: active ? "running" : "idle",
      message: active ? "Starting…" : undefined,
      channel: "none",
      history: [],
      error: undefined,
      lastUpdate: active ? Date.now() : undefined,
    });
  }, [active]);

  useEffect(() => {
    if (active && taskId) {
      reset();
    }
  }, [active, taskId, reset]);

  useEffect(() => {
    if (!active || !taskId) {
      stopConnections();
      return;
    }

    let mounted = true;

    const match = (event: ProgressMessage) =>
      matchEvent ? matchEvent(event, taskId) : defaultMatch(event, taskId);

    const startSimulated = () => {
      if (fallbackTimerRef.current) return;
      setState((prev) => ({ ...prev, channel: "simulated" }));
      const steps = Math.max(1, Math.round(fallbackDurationMs / SIMULATION_STEP_MS));
      const increment = Math.max(1, Math.floor(100 / steps));
      fallbackTimerRef.current = setInterval(() => {
        setState((prev) => {
          if (!mounted) {
            return prev;
          }
          if (prev.status === "completed" || prev.status === "failed") {
            return prev;
          }
          const next = Math.min(prev.progress + increment, 95);
          if (next === prev.progress) {
            return prev;
          }
          const entry: TaskHistoryEntry = {
            id: `sim-${Date.now()}-${Math.random().toString(16).slice(2, 6)}`,
            timestamp: Date.now(),
            progress: next,
            message: `Working… (${next}%)`,
            status: prev.status,
            source: "simulated",
          };
          return {
            ...prev,
            progress: next,
            history: [...prev.history, entry].slice(-10),
            message: prev.message ?? entry.message,
            channel: "simulated",
          };
        });
      }, SIMULATION_STEP_MS);
    };

    const startPolling = () => {
      if (!poller || fallbackTimerRef.current) return;
      setState((prev) => ({ ...prev, channel: "polling" }));
      fallbackTimerRef.current = setInterval(async () => {
        if (!mounted) return;
        try {
          const result = await poller();
          if (!result) return;
          if (!match(result)) return;
          pushEvent(result, "polling");
          if (eventSuggestsCompletion(result) || eventSuggestsFailure(result)) {
            stopConnections();
          }
        } catch (error) {
          const message = error instanceof Error ? error.message : String(error);
          setState((prev) => ({ ...prev, error: message }));
        }
      }, pollInterval ?? DEFAULT_POLL_INTERVAL);
    };

    try {
      const socket = new WebSocket(wsUrl());
      wsRef.current = socket;

      socket.onopen = () => {
        if (!mounted) return;
        setState((prev) => ({ ...prev, channel: "websocket" }));
      };

      socket.onmessage = (event) => {
        if (!mounted) return;
        try {
          const data = JSON.parse(event.data) as ProgressMessage;
          if (!data || data.type !== eventType) return;
          if (!match(data)) return;
          pushEvent(data, "websocket");
          if (eventSuggestsCompletion(data) || eventSuggestsFailure(data)) {
            stopConnections();
          }
        } catch {
          // Ignore malformed payloads
        }
      };

      socket.onerror = () => {
        socket.close();
      };

      socket.onclose = () => {
        if (!mounted) return;
        if (poller) {
          startPolling();
        } else {
          startSimulated();
        }
      };
    } catch {
      if (poller) {
        startPolling();
      } else {
        startSimulated();
      }
    }

    if (!wsRef.current) {
      if (poller) {
        startPolling();
      } else {
        startSimulated();
      }
    }

    return () => {
      mounted = false;
      stopConnections();
    };
  }, [
    active,
    taskId,
    eventType,
    matchEvent,
    poller,
    pollInterval,
    fallbackDurationMs,
    pushEvent,
    stopConnections,
  ]);

  useEffect(() => {
    if (state.status === "completed" || state.status === "failed") {
      stopConnections();
    }
  }, [state.status, stopConnections]);

  const setManualProgress = useCallback(
    (progress: number, status?: string, message?: string) => {
      pushEvent({ progress, status, message }, "manual");
      if (progress >= 100 || isCompletionStatus(status) || isFailureStatus(status)) {
        stopConnections();
      }
    },
    [pushEvent, stopConnections],
  );

  const addManualEvent = useCallback(
    (message: string, status?: string) => {
      pushEvent({ message, status }, "manual");
      if (isCompletionStatus(status) || isFailureStatus(status)) {
        stopConnections();
      }
    },
    [pushEvent, stopConnections],
  );

  return {
    state,
    setManualProgress,
    addManualEvent,
    reset,
  };
}
