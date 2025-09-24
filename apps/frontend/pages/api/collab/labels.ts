import type { NextApiRequest, NextApiResponse } from "next";

function hubUrl() {
  const port = process.env.IT_PORT_COLLAB || "8625";
  return process.env.COLLAB_URL || `http://localhost:${port}`;
}

export default async function handler(_req: NextApiRequest, res: NextApiResponse) {
  try {
    const r = await fetch(`${hubUrl()}/labels`);
    const data = await r.json();
    res.status(r.status).json(data);
  } catch (e: any) {
    res.status(502).json({ error: e?.message || "collab-hub unavailable" });
  }
}
