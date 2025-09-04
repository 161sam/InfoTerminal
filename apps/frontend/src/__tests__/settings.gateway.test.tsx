import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SettingsGateway from '../app/settings/components/SettingsGateway';

const STORAGE_KEY = 'it.settings.gateway';

describe('SettingsGateway component', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test('toggle and url persist', () => {
    render(<SettingsGateway />);
    const toggle = screen.getByLabelText(/Use Gateway proxy/);
    const url = screen.getByLabelText('Gateway URL') as HTMLInputElement;
    fireEvent.click(toggle);
    fireEvent.change(url, { target: { value: 'http://mygw' } });
    const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    expect(stored).toMatchObject({ enabled: true, url: 'http://mygw' });
  });

  test('test button reports status', async () => {
    const mock = vi.fn().mockResolvedValue({ ok: true });
    (global as any).fetch = mock;
    render(<SettingsGateway />);
    fireEvent.click(screen.getByText('Test'));
    await waitFor(() =>
      expect(screen.getByTestId('test-result')).toHaveTextContent('ok')
    );
    mock.mockResolvedValue({ ok: false });
    fireEvent.click(screen.getByText('Test'));
    await waitFor(() =>
      expect(screen.getByTestId('test-result')).toHaveTextContent('fail')
    );
  });
});
