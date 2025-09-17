import { render, waitFor } from '@testing-library/react';
import MapPanel from '@/components/MapPanel';
import React from 'react';
import { vi } from 'vitest';

describe('MapPanel', () => {
  it('renders and fetches layers', async () => {
    const mockFetch = vi.fn(
      async (input: RequestInfo | URL, _init?: RequestInit): Promise<Response> => {
        const url = typeof input === 'string'
          ? input
          : input instanceof URL
          ? input.href
          : (input as Request).url;

        const body = url.includes('/geo/entities')
          ? { type: 'FeatureCollection', features: [] }
          : { items: [] };

        return new Response(JSON.stringify(body), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        });
      }
    );

    // Assign with correct type
    global.fetch = mockFetch as unknown as typeof fetch;

    render(<MapPanel />);
    await waitFor(() => expect(mockFetch).toHaveBeenCalled());
  });
});
