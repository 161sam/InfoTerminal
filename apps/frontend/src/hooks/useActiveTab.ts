import { useState, useEffect } from "react";
import { NextRouter } from "next/router";

interface UseActiveTabOptions<T extends string> {
  defaultTab: T;
  validTabs: T[];
  urlParam: string;
  router: NextRouter;
}

export function useActiveTab<T extends string>({
  defaultTab,
  validTabs,
  urlParam,
  router,
}: UseActiveTabOptions<T>): [T, (tab: T) => void] {
  const [activeTab, setActiveTabState] = useState<T>(defaultTab);

  const isValidTab = (value: string): value is T => validTabs.includes(value as T);

  useEffect(() => {
    if (!router.isReady) {
      return;
    }

    const tabFromQuery = Array.isArray(router.query[urlParam])
      ? router.query[urlParam][0]
      : router.query[urlParam];

    if (typeof tabFromQuery === "string" && isValidTab(tabFromQuery)) {
      if (tabFromQuery !== activeTab) {
        setActiveTabState(tabFromQuery);
      }
      return;
    }

    if (typeof window === "undefined") {
      return;
    }

    const hashValue = window.location.hash.replace("#", "");
    if (hashValue && isValidTab(hashValue) && hashValue !== activeTab) {
      setActiveTabState(hashValue);
      router.replace(
        { pathname: router.pathname, query: { ...router.query, [urlParam]: hashValue } },
        undefined,
        { shallow: true },
      );
    }
  }, [router, router.isReady, router.pathname, router.query, urlParam, activeTab, isValidTab]);

  const setActiveTab = (tab: T) => {
    setActiveTabState(tab);

    if (!router.isReady) {
      return;
    }

    const nextQuery = { ...router.query, [urlParam]: tab };
    router.replace({ pathname: router.pathname, query: nextQuery }, undefined, { shallow: true });
  };

  return [activeTab, setActiveTab];
}
