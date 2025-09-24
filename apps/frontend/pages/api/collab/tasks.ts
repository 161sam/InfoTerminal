import type { NextApiRequest, NextApiResponse } from "next";

function hubUrl() {
  const port = process.env.IT_PORT_COLLAB || "8625";
  return process.env.COLLAB_URL || `http://localhost:${port}`;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const base = hubUrl();
  try {
    if (req.method === "GET") {
      const r = await fetch(`${base}/tasks`);
      const data = await r.json();
      return res.status(r.status).json(data);
    }
    if (req.method === "POST") {
      const r = await fetch(`${base}/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(req.body || {}),
      });
      const data = await r.json();
      return res.status(r.status).json(data);
    }
    return res.status(405).end();
  } catch (e: any) {
    return res.status(502).json({ error: e?.message || "collab-hub unavailable" });
  }
}
