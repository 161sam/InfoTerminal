import { render, screen, waitFor } from '@testing-library/react';
import { renderToString } from 'react-dom/server';
import { act } from 'react';
import { ToastProvider, ToastViewport, toast } from '@/components/ui/toast';

describe('toast system', () => {
  test('provider renders server-side without extra markup', () => {
    const html = renderToString(
      <ToastProvider>
        <div>hello</div>
      </ToastProvider>
    );
    expect(html).toBe('<div>hello</div>');
  });

  test('toast displays message and disappears', async () => {
    render(
      <ToastProvider>
        <ToastViewport />
      </ToastProvider>
    );
    act(() => {
      toast('hi');
    });
    await screen.findByText('hi');
    await waitFor(() => expect(screen.queryByText('hi')).toBeNull(), { timeout: 4000 });
  });
});
