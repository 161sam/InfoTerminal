import { vi, describe, test, expect, beforeEach } from 'vitest';

beforeEach(() => {
  vi.resetModules();
  localStorage.clear();
  delete (process.env as any).NEXT_PUBLIC_GRAPH_DEEPLINK_BASE;
});

describe('deeplink helpers', () => {
  test('getGraphDeeplinkBase prefers localStorage over env', async () => {
    (process.env as any).NEXT_PUBLIC_GRAPH_DEEPLINK_BASE = '/env?focus=';
    const mod = await import('../../lib/deeplink');
    expect(mod.getGraphDeeplinkBase()).toBe('/env?focus=');
    localStorage.setItem(mod.DEEPLINK_STORAGE_KEY, '/local?focus=');
    expect(mod.getGraphDeeplinkBase()).toBe('/local?focus=');
  });

  test('buildGraphDeepLink encodes params', async () => {
    (process.env as any).NEXT_PUBLIC_GRAPH_DEEPLINK_BASE = '/graphx?focus=';
    const { buildGraphDeepLink } = await import('../../lib/deeplink');
    expect(buildGraphDeepLink({ id: '123' })).toBe('/graphx?focus=123');
    const url = buildGraphDeepLink({
      id: '123',
      type: 'entity',
      layout: 'force',
      highlight: ['1', '2'],
      filters: { tag: ['a', 'b'], source: 'news' },
      q: 'acme',
    });
    expect(url).toBe(
      '/graphx?focus=123&type=entity&layout=force&q=acme&highlight=1%2C2&f.tag=a&f.tag=b&f.source=news'
    );
  });

  test('abs=true with relative base prepends origin', async () => {
    (process.env as any).NEXT_PUBLIC_GRAPH_DEEPLINK_BASE = '/graphx?focus=';
    const { buildGraphDeepLink } = await import('../../lib/deeplink');
    expect(buildGraphDeepLink({ id: '123', abs: true })).toBe(
      `${location.origin}/graphx?focus=123`
    );
  });
});
