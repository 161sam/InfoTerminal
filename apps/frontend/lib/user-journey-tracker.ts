/**
 * User Journey Tracking Service
 *
 * Tracks user interactions, click paths, dwell time, and feature usage for UX optimization.
 */

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/router";

interface UserAction {
  timestamp: number;
  sessionId: string;
  userId?: string;
  actionType: "click" | "hover" | "scroll" | "form_submit" | "page_view" | "search" | "download";
  element: string;
  elementText?: string;
  page: string;
  coordinates?: { x: number; y: number };
  dwellTime?: number;
  metadata?: Record<string, any>;
}

interface UserSession {
  sessionId: string;
  userId?: string;
  startTime: number;
  endTime?: number;
  actions: UserAction[];
  pageViews: string[];
  totalDwellTime: number;
  featureUsage: Record<string, number>;
  completedWorkflows: string[];
  abandonedAt?: string;
}

class UserJourneyTracker {
  private static instance: UserJourneyTracker;
  private sessionId: string;
  private userId?: string;
  private session: UserSession;
  private pageStartTime: number;
  private isTracking: boolean = true;
  private batchBuffer: UserAction[] = [];
  private batchTimeout: NodeJS.Timeout | null = null;

  constructor() {
    this.sessionId = this.generateSessionId();
    this.pageStartTime = Date.now();
    this.session = {
      sessionId: this.sessionId,
      startTime: Date.now(),
      actions: [],
      pageViews: [],
      totalDwellTime: 0,
      featureUsage: {},
      completedWorkflows: [],
    };

    this.setupEventListeners();
    this.startHeartbeat();
  }

  static getInstance(): UserJourneyTracker {
    if (!UserJourneyTracker.instance) {
      UserJourneyTracker.instance = new UserJourneyTracker();
    }
    return UserJourneyTracker.instance;
  }

  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  setUserId(userId: string) {
    this.userId = userId;
    this.session.userId = userId;
  }

  enableTracking() {
    this.isTracking = true;
  }

  disableTracking() {
    this.isTracking = false;
  }

  private setupEventListeners() {
    if (typeof window === "undefined") return;

    // Track clicks
    document.addEventListener("click", (event) => {
      if (!this.isTracking) return;

      const target = event.target as HTMLElement;
      const elementInfo = this.getElementInfo(target);

      this.trackAction({
        actionType: "click",
        element: elementInfo.selector,
        elementText: elementInfo.text,
        coordinates: { x: event.clientX, y: event.clientY },
        metadata: {
          tagName: target.tagName,
          className: target.className,
          id: target.id,
        },
      });

      // Track feature usage
      this.trackFeatureUsage(elementInfo.selector);
    });

    // Track form submissions
    document.addEventListener("submit", (event) => {
      if (!this.isTracking) return;

      const form = event.target as HTMLFormElement;
      const formData = new FormData(form);
      const formFields = Array.from(formData.keys());

      this.trackAction({
        actionType: "form_submit",
        element: this.getElementSelector(form),
        metadata: {
          formId: form.id,
          formClass: form.className,
          fieldCount: formFields.length,
          fields: formFields,
        },
      });
    });

    // Track scrolling behavior
    let scrollTimeout: NodeJS.Timeout;
    document.addEventListener("scroll", () => {
      if (!this.isTracking) return;

      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        const scrollPercentage = Math.round(
          (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100,
        );

        this.trackAction({
          actionType: "scroll",
          element: "document",
          metadata: {
            scrollY: window.scrollY,
            scrollPercentage: Math.min(scrollPercentage, 100),
            pageHeight: document.body.scrollHeight,
            viewportHeight: window.innerHeight,
          },
        });
      }, 250);
    });

    // Track page visibility
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        this.sendBatchedActions();
      }
    });

    // Track page unload
    window.addEventListener("beforeunload", () => {
      this.endSession();
    });
  }

  private getElementInfo(element: HTMLElement): { selector: string; text: string } {
    const selector = this.getElementSelector(element);
    const text = element.textContent?.trim().substring(0, 100) || "";
    return { selector, text };
  }

  private getElementSelector(element: HTMLElement): string {
    if (element.id) {
      return `#${element.id}`;
    }

    if (element.className) {
      const classes = element.className.split(" ").filter((c) => c.length > 0);
      if (classes.length > 0) {
        return `.${classes[0]}`;
      }
    }

    const tagName = element.tagName.toLowerCase();
    const parent = element.parentElement;

    if (parent) {
      const siblings = Array.from(parent.children);
      const index = siblings.indexOf(element);
      return `${tagName}:nth-child(${index + 1})`;
    }

    return tagName;
  }

  private trackFeatureUsage(elementSelector: string) {
    // Map element selectors to feature names
    const featureMap: Record<string, string> = {
      "#entity-search-button": "entity_search",
      "#graph-view-button": "graph_visualization",
      "#export-button": "data_export",
      "#domain-analysis-tool": "domain_analysis",
      "#social-media-tool": "social_media_analysis",
      "#document-upload": "document_analysis",
      "#geospatial-tool": "geospatial_analysis",
      ".plugin-runner": "plugin_execution",
      "#advanced-search": "advanced_search",
      ".filter-panel": "data_filtering",
      "#investigation-dashboard": "dashboard_usage",
    };

    Object.entries(featureMap).forEach(([selector, feature]) => {
      if (elementSelector.includes(selector)) {
        this.session.featureUsage[feature] = (this.session.featureUsage[feature] || 0) + 1;
      }
    });
  }

  trackAction(actionData: Partial<UserAction>) {
    if (!this.isTracking) return;

    const action: UserAction = {
      timestamp: Date.now(),
      sessionId: this.sessionId,
      userId: this.userId,
      page: window.location.pathname,
      ...actionData,
    } as UserAction;

    this.session.actions.push(action);
    this.batchBuffer.push(action);

    // Batch send actions to avoid performance impact
    if (this.batchBuffer.length >= 10) {
      this.sendBatchedActions();
    } else if (!this.batchTimeout) {
      this.batchTimeout = setTimeout(() => {
        this.sendBatchedActions();
      }, 5000);
    }
  }

  trackPageView(page: string) {
    if (!this.isTracking) return;

    // Calculate dwell time for previous page
    if (this.session.pageViews.length > 0) {
      const dwellTime = Date.now() - this.pageStartTime;
      this.session.totalDwellTime += dwellTime;
    }

    this.pageStartTime = Date.now();
    this.session.pageViews.push(page);

    this.trackAction({
      actionType: "page_view",
      element: "page",
      dwellTime: 0,
      metadata: {
        referrer: document.referrer,
        userAgent: navigator.userAgent,
        screenResolution: `${screen.width}x${screen.height}`,
        viewportSize: `${window.innerWidth}x${window.innerHeight}`,
      },
    });
  }

  trackWorkflowCompletion(workflowName: string) {
    if (!this.isTracking) return;

    this.session.completedWorkflows.push(workflowName);

    this.trackAction({
      actionType: "workflow_completion",
      element: "workflow",
      metadata: {
        workflowName,
        completionTime: Date.now() - this.session.startTime,
        totalSteps: this.session.actions.filter((a) => a.metadata?.workflowName === workflowName)
          .length,
      },
    });
  }

  trackWorkflowAbandonment(workflowName: string, step: string) {
    if (!this.isTracking) return;

    this.session.abandonedAt = `${workflowName}:${step}`;

    this.trackAction({
      actionType: "workflow_abandonment",
      element: "workflow",
      metadata: {
        workflowName,
        abandonedAt: step,
        timeSpent: Date.now() - this.session.startTime,
        completedSteps: this.session.actions.filter(
          (a) => a.metadata?.workflowName === workflowName,
        ).length,
      },
    });
  }

  trackSearch(query: string, results: number, responseTime: number) {
    if (!this.isTracking) return;

    this.trackAction({
      actionType: "search",
      element: "search",
      metadata: {
        query: query.substring(0, 100), // Limit query length for privacy
        resultsCount: results,
        responseTimeMs: responseTime,
        queryLength: query.length,
        hasFilters: query.includes(":") || query.includes("AND") || query.includes("OR"),
      },
    });
  }

  trackDownload(fileName: string, fileType: string, fileSize?: number) {
    if (!this.isTracking) return;

    this.trackAction({
      actionType: "download",
      element: "download",
      metadata: {
        fileName: fileName.substring(0, 100),
        fileType,
        fileSize,
        downloadTime: Date.now(),
      },
    });
  }

  private async sendBatchedActions() {
    if (this.batchBuffer.length === 0) return;

    const actionsToSend = [...this.batchBuffer];
    this.batchBuffer = [];

    if (this.batchTimeout) {
      clearTimeout(this.batchTimeout);
      this.batchTimeout = null;
    }

    try {
      await fetch("/api/analytics/track", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sessionId: this.sessionId,
          actions: actionsToSend,
        }),
        keepalive: true,
      });
    } catch (error) {
      console.warn("Failed to send tracking data:", error);
      // Could implement local storage fallback here
    }
  }

  private startHeartbeat() {
    // Send heartbeat every 30 seconds to track session duration
    setInterval(() => {
      if (this.isTracking && !document.hidden) {
        this.trackAction({
          actionType: "heartbeat",
          element: "session",
          metadata: {
            sessionDuration: Date.now() - this.session.startTime,
            activeTab: !document.hidden,
          },
        });
      }
    }, 30000);
  }

  endSession() {
    this.session.endTime = Date.now();
    this.sendBatchedActions();

    // Send final session summary
    fetch("/api/analytics/session-end", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(this.session),
      keepalive: true,
    }).catch((error) => {
      console.warn("Failed to send session end data:", error);
    });
  }

  getSessionSummary(): UserSession {
    return {
      ...this.session,
      totalDwellTime: this.session.totalDwellTime + (Date.now() - this.pageStartTime),
    };
  }

  // Hook for React components
  static useUserJourney() {
    const [tracker] = useState(() => UserJourneyTracker.getInstance());
    const router = useRouter();

    useEffect(() => {
      tracker.trackPageView(router.pathname);
    }, [router.pathname, tracker]);

    const trackClick = useCallback(
      (elementId: string, metadata?: Record<string, any>) => {
        tracker.trackAction({
          actionType: "click",
          element: elementId,
          metadata,
        });
      },
      [tracker],
    );

    const trackWorkflowStep = useCallback(
      (workflowName: string, step: string) => {
        tracker.trackAction({
          actionType: "workflow_step",
          element: "workflow",
          metadata: {
            workflowName,
            step,
            stepTime: Date.now(),
          },
        });
      },
      [tracker],
    );

    return {
      trackClick,
      trackWorkflowStep,
      trackWorkflowCompletion: tracker.trackWorkflowCompletion.bind(tracker),
      trackWorkflowAbandonment: tracker.trackWorkflowAbandonment.bind(tracker),
      trackSearch: tracker.trackSearch.bind(tracker),
      trackDownload: tracker.trackDownload.bind(tracker),
      getSessionSummary: tracker.getSessionSummary.bind(tracker),
    };
  }
}

export default UserJourneyTracker;
export { type UserAction, type UserSession };
