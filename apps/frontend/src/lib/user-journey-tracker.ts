// Minimal user journey tracker shim for analytics/tracking hooks.
// Provides no-op implementations used across the app.

type Journey = {
  trackSearch: (query: string, resultCount?: number, responseTimeMs?: number) => void;
  trackClick: (event: string, payload?: Record<string, unknown>) => void;
  trackWorkflowStep: (workflow: string, stepId: string, metadata?: Record<string, unknown>) => void;
};

function useUserJourney(): Journey {
  const noop = () => {};
  return {
    trackSearch: () => noop(),
    trackClick: () => noop(),
    trackWorkflowStep: () => noop(),
  };
}

const UserJourney = { useUserJourney };
export default UserJourney;
