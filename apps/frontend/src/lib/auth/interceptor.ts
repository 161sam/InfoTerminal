type FetchInput = Parameters<typeof fetch>[0];
type FetchInitWithRetry = (RequestInit & { _retry?: boolean }) | undefined;

export interface AuthInterceptorOptions {
  refresh: () => Promise<boolean>;
  onUnauthorized: () => void;
  isAuthEnabled: boolean;
  shouldSkip?: (input: FetchInput) => boolean;
}

interface RuntimeOptions extends AuthInterceptorOptions {
  shouldSkip: (input: FetchInput) => boolean;
}

const runtime: RuntimeOptions = {
  refresh: async () => false,
  onUnauthorized: () => undefined,
  isAuthEnabled: false,
  shouldSkip: () => false,
};

let installed = false;
let originalFetch: typeof fetch | null = null;

const globalTarget: typeof globalThis & { fetch?: typeof fetch } =
  typeof window !== "undefined" ? window : globalThis;

function normaliseInit(init: FetchInitWithRetry): RequestInit & { _retry?: boolean } {
  if (!init) {
    return { _retry: false };
  }
  return init as RequestInit & { _retry?: boolean };
}

function shouldBypass(input: FetchInput) {
  try {
    return runtime.shouldSkip(input);
  } catch {
    return false;
  }
}

export function installAuthInterceptor(options: AuthInterceptorOptions) {
  runtime.refresh = options.refresh;
  runtime.onUnauthorized = options.onUnauthorized;
  runtime.isAuthEnabled = options.isAuthEnabled;
  runtime.shouldSkip = options.shouldSkip ?? (() => false);

  if (!options.isAuthEnabled) {
    return () => undefined;
  }

  if (installed) {
    return () => undefined;
  }

  const fetchImpl = globalTarget.fetch;
  if (typeof fetchImpl !== "function") {
    return () => undefined;
  }

  originalFetch = fetchImpl.bind(globalTarget);

  const wrappedFetch: typeof fetch = async (input, init) => {
    const initialResponse = await originalFetch!(input, init);

    if (!runtime.isAuthEnabled) {
      return initialResponse;
    }

    if (initialResponse.status !== 401) {
      return initialResponse;
    }

    if (shouldBypass(input)) {
      return initialResponse;
    }

    const requestInit = normaliseInit(init);

    if (requestInit._retry) {
      runtime.onUnauthorized();
      return initialResponse;
    }

    let refreshed = false;
    try {
      refreshed = await runtime.refresh();
    } catch {
      refreshed = false;
    }

    if (!refreshed) {
      runtime.onUnauthorized();
      return initialResponse;
    }

    const { _retry, ...retryRest } = requestInit;
    const retryResponse = await originalFetch!(input, { ...retryRest, _retry: true } as RequestInit);

    if (retryResponse.status === 401) {
      runtime.onUnauthorized();
    }

    return retryResponse;
  };

  globalTarget.fetch = wrappedFetch;
  installed = true;

  return () => {
    if (installed && originalFetch) {
      globalTarget.fetch = originalFetch;
    }
    installed = false;
    originalFetch = null;
  };
}

export function resetAuthInterceptorForTests() {
  if (installed && originalFetch) {
    globalTarget.fetch = originalFetch;
  }
  installed = false;
  originalFetch = null;
  runtime.refresh = async () => false;
  runtime.onUnauthorized = () => undefined;
  runtime.isAuthEnabled = false;
  runtime.shouldSkip = () => false;
}
