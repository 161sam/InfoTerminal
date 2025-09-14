import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import OpsTab from '@/components/settings/OpsTab';
import { describe, it, expect, vi } from 'vitest';

describe('OpsTab', () => {
  it('lists stacks and triggers start', async () => {
    const mockFetch = vi.fn()
      .mockResolvedValueOnce({ json: async () => ({ stacks: { core: { title: 'Core', files: [] } } }) })
      .mockResolvedValue({ json: async () => ({ ok: true }) });
    // @ts-ignore
    global.fetch = mockFetch;

    render(<OpsTab />);
    await screen.findByText(/Core/);
    fireEvent.click(screen.getByText('Start'));
    await waitFor(() => expect(mockFetch).toHaveBeenCalledWith('/api/ops/stacks/core/up', { method: 'POST' }));
  });
});
