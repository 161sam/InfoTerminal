import { useRouter } from "next/router";
import { useEffect, useState } from "react";

// URL Route Configuration
export const URL_PATTERNS = {
  graphx: {
    base: "/graphx",
    tabs: {
      graph: "/graphx/graph",
      viz3d: "/graphx/viz3d",
      ml: "/graphx/ml",
    },
    defaultTab: "graph",
  },
  nlp: {
    base: "/nlp",
    domains: {
      general: "/nlp/general",
      legal: "/nlp/legal",
      documents: "/nlp/documents",
      ethics: "/nlp/ethics",
      forensics: "/nlp/forensics",
    },
    defaultDomain: "general",
  },
  agent: {
    base: "/agent",
    tabs: {
      interaction: "/agent/interaction",
      management: "/agent/management",
    },
    defaultTab: "interaction",
  },
};

// Parse current URL to extract tab/domain information
export const parseRouteParams = (router: ReturnType<typeof useRouter>) => {
  const { pathname, query } = router;

  // Handle GraphX routes
  if (pathname.startsWith("/graphx")) {
    const pathSegments = pathname.split("/");
    const tabFromPath = pathSegments[2]; // /graphx/[tab]
    const tabFromQuery = query.tab as string;

    return {
      page: "graphx",
      tab: tabFromPath || tabFromQuery || URL_PATTERNS.graphx.defaultTab,
      domain: null,
    };
  }

  // Handle NLP routes
  if (pathname.startsWith("/nlp")) {
    const pathSegments = pathname.split("/");
    const domainFromPath = pathSegments[2]; // /nlp/[domain]
    const domainFromQuery = query.domain as string;

    return {
      page: "nlp",
      tab: null,
      domain: domainFromPath || domainFromQuery || URL_PATTERNS.nlp.defaultDomain,
    };
  }

  // Handle Agent routes
  if (pathname.startsWith("/agent")) {
    const pathSegments = pathname.split("/");
    const tabFromPath = pathSegments[2]; // /agent/[tab]
    const tabFromQuery = query.tab as string;

    return {
      page: "agent",
      tab: tabFromPath || tabFromQuery || URL_PATTERNS.agent.defaultTab,
      domain: null,
    };
  }

  return {
    page: pathname.replace("/", "") || "index",
    tab: null,
    domain: null,
  };
};

// Generate clean URL for navigation
export const generateCleanURL = (
  page: string,
  tab?: string,
  domain?: string,
  useCleanURL: boolean = true,
): string => {
  const config = URL_PATTERNS[page as keyof typeof URL_PATTERNS];

  if (!config) return `/${page}`;

  // GraphX URLs
  if (page === "graphx" && tab) {
    if (useCleanURL && config.tabs && tab in config.tabs) {
      return config.tabs[tab as keyof typeof config.tabs];
    }
    return tab === config.defaultTab ? config.base : `${config.base}?tab=${tab}`;
  }

  // NLP URLs
  if (page === "nlp" && domain) {
    if (useCleanURL && config.domains && domain in config.domains) {
      return config.domains[domain as keyof typeof config.domains];
    }
    return domain === config.defaultDomain ? config.base : `${config.base}?domain=${domain}`;
  }

  // Agent URLs
  if (page === "agent" && tab) {
    if (useCleanURL && config.tabs && tab in config.tabs) {
      return config.tabs[tab as keyof typeof config.tabs];
    }
    return tab === config.defaultTab ? config.base : `${config.base}?tab=${tab}`;
  }

  return config.base;
};

// Hook for handling URL-based tab/domain state
export const useURLBasedState = (defaultTab?: string, defaultDomain?: string) => {
  const router = useRouter();
  const [isReady, setIsReady] = useState(false);

  const routeParams = parseRouteParams(router);

  useEffect(() => {
    if (router.isReady) {
      setIsReady(true);
    }
  }, [router.isReady]);

  const updateURL = (newTab?: string, newDomain?: string) => {
    const { page } = routeParams;
    const cleanURL = generateCleanURL(page, newTab, newDomain, true);

    // Use router.replace to avoid adding to history stack for tab switches
    router.replace(cleanURL, undefined, { shallow: true });
  };

  const navigateToTab = (tab: string) => {
    updateURL(tab, routeParams.domain || defaultDomain);
  };

  const navigateToDomain = (domain: string) => {
    updateURL(routeParams.tab || defaultTab, domain);
  };

  return {
    isReady,
    currentPage: routeParams.page,
    currentTab: routeParams.tab || defaultTab,
    currentDomain: routeParams.domain || defaultDomain,
    navigateToTab,
    navigateToDomain,
    updateURL,
  };
};

// Generate URL for external navigation (e.g., from Header)
export const getPageURL = (page: string, tab?: string, domain?: string): string => {
  return generateCleanURL(page, tab, domain, true);
};

export default {
  URL_PATTERNS,
  parseRouteParams,
  generateCleanURL,
  useURLBasedState,
  getPageURL,
};
