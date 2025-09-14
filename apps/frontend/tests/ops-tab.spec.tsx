import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import OpsTab from '@/components/settings/OpsTab';
import { describe, it, expect, vi } from 'vitest';

describe('OpsTab', () => {
  it('handles start, scale and logs', async () => {
    const stream = new ReadableStream({
      start(controller) {
        controller.enqueue(new TextEncoder().encode('line1\n'));
        controller.close();
      }
    });
    const mockFetch = vi.fn((url: string, opts?: any) => {
      if (url === '/api/ops/stacks')
        return Promise.resolve({ json: async () => ({ stacks: { core: { title: 'Core', files: [] } } }) });
      if (url === '/api/ops/stacks/core/status')
        return Promise.resolve({ json: async () => ({ stack: 'core', services: [{ Service: 'web' }] }) });
      if (url.startsWith('/api/ops/stacks/core/scale'))
        return Promise.resolve({ json: async () => ({ ok: true }) });
      if (url.startsWith('/api/ops/stacks/core/logs')) return Promise.resolve({ body: stream });
      return Promise.resolve({ json: async () => ({ ok: true }) });
    });
    // @ts-ignore
    global.fetch = mockFetch;

    render(<OpsTab />);
    await screen.findByText(/Core/);
    fireEvent.click(screen.getByText('Start'));
    await waitFor(() =>
      expect(mockFetch).toHaveBeenCalledWith('/api/ops/stacks/core/up', { method: 'POST' })
    );

    fireEvent.click(screen.getByText('Status'));
    await waitFor(() => expect(mockFetch).toHaveBeenCalledWith('/api/ops/stacks/core/status', undefined));
    const select = await screen.findByRole('combobox');
    fireEvent.change(select, { target: { value: 'web' } });
    const input = screen.getByRole('spinbutton');
    fireEvent.change(input, { target: { value: '2' } });
    fireEvent.click(screen.getByText('Scale'));
    await waitFor(() =>
      expect(mockFetch).toHaveBeenCalledWith(
        '/api/ops/stacks/core/scale?service=web&replicas=2',
        { method: 'POST' }
      )
    );

    fireEvent.click(screen.getByText('Logs'));
    await screen.findByText('line1');
  });
});
