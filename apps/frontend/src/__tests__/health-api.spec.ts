import { vi, expect, it } from 'vitest';
import { getHealth } from '../../pages/api/health';

it('aggregates service states', async () => {
  const responses = [
    { ok: true, json: async () => ({ status: 'ok' }) },
    { ok: true, json: async () => ({ status: 'degraded' }) },
    Promise.reject(new Error('fail')),
    { ok: false, json: async () => ({}) },
  ];
  const fetchMock = vi.fn();
  responses.forEach((r) => fetchMock.mockResolvedValueOnce(r as any));
  global.fetch = fetchMock as any;

  const res = await getHealth();
  expect(res.services.search.state).toBe('ok');
  expect(res.services.graph.state).toBe('degraded');
  expect(res.services.docentities.state).toBe('unreachable');
  expect(res.services.nlp.state).toBe('unreachable');
});
