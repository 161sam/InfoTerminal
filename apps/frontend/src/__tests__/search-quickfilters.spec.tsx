import { describe, it, expect } from 'vitest';
import { buildSearchUrl } from '../lib/searchNav';

describe('buildSearchUrl', () => {
  it('adds entity and value params', () => {
    const url = buildSearchUrl({}, { addEntity: 'Person' });
    expect(url).toBe('/search?entity=Person');
    const url2 = buildSearchUrl({ entity: ['Person'] }, { addValue: 'ACME' });
    expect(url2).toBe('/search?entity=Person&value=ACME');
  });

  it('removes params', () => {
    const url = buildSearchUrl({ entity: ['Person'], value: ['ACME'] }, { remove: { entity: 'Person' } });
    expect(url).toBe('/search?value=ACME');
  });
});
