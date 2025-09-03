import { render, screen } from '@testing-library/react';
import AssetPage from '../../pages/asset/[id]';

vi.mock('next/router', () => ({
  useRouter: () => ({ query: { id: 'A1' }, push: vi.fn() })
}));

vi.mock('@/lib/api', () => ({
  fetchAsset: async () => ({ name: 'A1' }),
  fetchAssetPrices: async () => [{ ts: '1', open: 1, high: 1, low: 1, close: 1 }],
  fetchGraph: async () => ({ nodes: [], edges: [] }),
  fetchNews: async () => []
}));

test('loads header and default tab', async () => {
  render(<AssetPage />);
  expect(await screen.findByTestId('asset-page')).toBeInTheDocument();
  expect(await screen.findByTestId('timeseries-chart')).toBeInTheDocument();
});
