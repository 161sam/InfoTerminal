import { renderHook, waitFor } from '@testing-library/react';
import { useServiceHealthMatrix } from '../hooks/useServiceHealthMatrix';

test('polls readyz endpoints', async () => {
  const mock = vi.fn().mockResolvedValue({ ok: true, json: () => Promise.resolve({}) });
  (global as any).fetch = mock;
  const { result } = renderHook(() => useServiceHealthMatrix(0));
  await waitFor(() => Object.keys(result.current).length > 0);
  expect(mock).toHaveBeenCalled();
});
