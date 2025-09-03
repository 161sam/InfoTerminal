import type { NextApiRequest, NextApiResponse } from 'next';

/**
 * Proxies search requests to the search-api service running locally.
 * All query parameters are forwarded 1:1.
 */
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const base = process.env.SEARCH_API_URL || 'http://localhost:8001/search';
  const url = new URL(base);
  for (const [key, value] of Object.entries(req.query)) {
    if (Array.isArray(value)) {
      value.forEach((v) => url.searchParams.append(key, v));
    } else if (value !== undefined) {
      url.searchParams.set(key, String(value));
    }
  }

  try {
    const r = await fetch(url.toString(), { headers: { accept: 'application/json' } });
    if (!r.ok) {
      const text = await r.text();
      res.status(r.status).json({ message: text });
      return;
    }
    const json = await r.json();
    res.status(200).json(json);
  } catch (e: any) {
    res.status(500).json({ message: e.message || 'search proxy error' });
  }
}
