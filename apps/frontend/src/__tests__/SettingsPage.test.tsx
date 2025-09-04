import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SettingsPage from '../../pages/settings';

beforeEach(() => {
  localStorage.clear();
});

test('test connection shows status', async () => {
  (global as any).fetch = vi.fn().mockResolvedValue({ ok: true });
  render(<SettingsPage />);
  const btn = await screen.findAllByText('Test');
  fireEvent.click(btn[0]);
  await waitFor(() => screen.getByText('ok'));
});

test('saving persists endpoints', async () => {
  render(<SettingsPage />);
  const input = await screen.findByLabelText('Search API');
  fireEvent.change(input, { target: { value: 'http://example.com' } });
  fireEvent.click(screen.getByText('Save'));
  expect(JSON.parse(localStorage.getItem('it.settings.endpoints')!)).toHaveProperty('SEARCH_API', 'http://example.com');
});
