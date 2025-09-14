import { render, waitFor } from '@testing-library/react';
import MapPanel from '@/components/MapPanel';
import React from 'react';
import { vi } from 'vitest';

describe('MapPanel', () => {
  it('renders and fetches layers', async () => {
    global.fetch = vi.fn((url: string) =>
      Promise.resolve({
        ok: true,
        status: 200,
        json: async () =>
          url.includes('/geo/entities')
            ? { type: 'FeatureCollection', features: [] }
            : { items: [] },
      }) as any
    );

    render(<MapPanel />);
    await waitFor(() => expect(global.fetch).toHaveBeenCalled());
  });
});
