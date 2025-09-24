import type { NextApiRequest, NextApiResponse } from "next";

function prUrl(): string {
  const port = process.env.IT_PORT_PLUGIN_RUNNER || "8621";
  return process.env.PLUGIN_RUNNER_URL || `http://localhost:${port}`;
}

export default async function handler(_req: NextApiRequest, res: NextApiResponse) {
  try {
    const base = prUrl();
    const r = await fetch(`${base}/plugins`);
    if (!r.ok) throw new Error(`plugin-runner ${r.status}`);
    const data = await r.json();
    return res.status(200).json(data);
  } catch (e: any) {
    return res.status(200).json({ plugins: [], error: e?.message || "unavailable" });
  }
}
