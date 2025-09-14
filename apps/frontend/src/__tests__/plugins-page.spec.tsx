import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import PluginsPage from '../../pages/plugins';
import { vi } from 'vitest';

vi.mock('@/components/auth/AuthProvider', () => ({
  useAuth: () => ({ hasRole: () => false }),
}));

vi.mock('@/components/health/GlobalHealth', () => ({ default: () => <div /> }));

declare const global: any;

test('renders plugin cards and toggles', async () => {
  global.fetch = vi.fn((url) => {
    if (typeof url === 'string' && url.includes('/registry')) {
      return Promise.resolve({ json: async () => ({ items: [{ name: 'openbb', version: '0.1', provider: 'OpenBB' }] }) });
    }
    if (typeof url === 'string' && url.includes('/state')) {
      return Promise.resolve({ json: async () => ({ items: [{ name: 'openbb', enabled: true }] }) });
    }
    if (typeof url === 'string' && url.includes('/health')) {
      return Promise.resolve({ json: async () => ({ status: 'up' }) });
    }
    return Promise.resolve({ json: async () => ({}) });
  }) as any;

  render(<PluginsPage />);
  await waitFor(() => expect(screen.getByText('openbb')).toBeInTheDocument());
  const toggle = screen.getByRole('switch');
  fireEvent.click(toggle);
  await waitFor(() =>
    expect(global.fetch).toHaveBeenCalledWith(
      '/api/plugins/openbb/enable',
      expect.objectContaining({ method: 'POST' })
    )
  );
});

