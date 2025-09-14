import { render, screen, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import type { NextRouter } from 'next/router';
import PluginDetailPage from '../../pages/plugins/[name]';

declare const global: any;

vi.mock('@/components/auth/AuthProvider', () => ({
  useAuth: () => ({ hasRole: () => false }),
}));

vi.mock('@/components/health/GlobalHealth', () => ({ default: () => <div /> }));

function createMockRouter(router: Partial<NextRouter>): NextRouter {
  return {
    basePath: '',
    pathname: '/plugins/openbb',
    route: '/plugins/[name]',
    query: {},
    asPath: '/plugins/openbb',
    push: vi.fn(),
    replace: vi.fn(),
    reload: vi.fn(),
    back: vi.fn(),
    prefetch: vi.fn().mockResolvedValue(undefined),
    beforePopState: vi.fn(),
    events: { on: vi.fn(), off: vi.fn(), emit: vi.fn() },
    isFallback: false,
    isReady: true,
    isLocaleDomain: false,
    isPreview: false,
    forward: vi.fn(),
    ...router,
  } as NextRouter;
}

vi.mock('next/router', () => ({
  useRouter: () => createMockRouter({ query: { name: 'openbb' } }),
}));

test.skip('shows fallback link when iframe not ready', async () => {
  vi.useFakeTimers();
  global.fetch = vi.fn((url) => {
    if (typeof url === 'string' && url.includes('/registry')) {
      return Promise.resolve({ json: async () => ({ items: [{ name: 'openbb', version: '0.1', provider: 'OpenBB', endpoints: { baseUrl: 'http://example.com' } }] }) });
    }
    if (typeof url === 'string' && url.includes('/state')) {
      return Promise.resolve({ json: async () => ({ items: [{ name: 'openbb', enabled: true }] }) });
    }
    if (typeof url === 'string' && url.includes('/health')) {
      return Promise.resolve({ json: async () => ({ status: 'up' }) });
    }
    return Promise.resolve({ json: async () => ({}) });
  }) as any;

  render(<PluginDetailPage />);
  await waitFor(() => expect(global.fetch).toHaveBeenCalled());
  await vi.runAllTimersAsync();
  await waitFor(() => expect(screen.getByText(/Open externally/i)).toBeInTheDocument());
}, 10000);

