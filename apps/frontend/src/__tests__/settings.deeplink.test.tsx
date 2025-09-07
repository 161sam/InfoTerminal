import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SettingsGraphDeepLink from '@/components/settings/SettingsGraphDeepLink';
import { ToastProvider, ToastViewport } from '@/components/ui/toast';

const STORAGE_KEY = 'it.settings.graph.deeplinkBase';

describe('Settings Graph Deep-Link', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test('invalid value shows error and does not persist', async () => {
    render(
      <ToastProvider>
        <ToastViewport />
        <SettingsGraphDeepLink />
      </ToastProvider>
    );
    const input = await screen.findByLabelText('Graph Deep-Link Base');
    fireEvent.change(input, { target: { value: 'bad' } });
    fireEvent.click(screen.getByText('Speichern'));
    await waitFor(() => screen.getByText(/Invalid/));
    expect(localStorage.getItem(STORAGE_KEY)).toBeNull();
  });

  test('valid value persists with success toast', async () => {
    render(
      <ToastProvider>
        <ToastViewport />
        <SettingsGraphDeepLink />
      </ToastProvider>
    );
    const input = await screen.findByLabelText('Graph Deep-Link Base');
    fireEvent.change(input, { target: { value: '/graphx?focus=' } });
    fireEvent.click(screen.getByText('Speichern'));
    await waitFor(() => screen.getByText(/Saved/));
    expect(localStorage.getItem(STORAGE_KEY)).toBe('/graphx?focus=');
  });

  test('test button shows generated link', async () => {
    render(
      <ToastProvider>
        <ToastViewport />
        <SettingsGraphDeepLink />
      </ToastProvider>
    );
    const input = await screen.findByLabelText('Graph Deep-Link Base');
    fireEvent.change(input, { target: { value: '/graphx?focus=' } });
    fireEvent.click(screen.getByText('Test'));
    await waitFor(() => screen.getByTestId('test-link'));
    expect(screen.getByTestId('test-link')).toHaveTextContent('/graphx?focus=demo');
  });
});
