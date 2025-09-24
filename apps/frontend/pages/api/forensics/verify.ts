import type { NextApiRequest, NextApiResponse } from "next";

function forensicsUrl() {
  const port = process.env.IT_PORT_FORENSICS || "8627";
  return process.env.FORENSICS_URL || `http://localhost:${port}`;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") return res.status(405).end();
  try {
    const r = await fetch(`${forensicsUrl()}/verify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body || {}),
    });
    const data = await r.json();
    return res.status(r.status).json(data);
  } catch (e: any) {
    return res.status(502).json({ error: e?.message || "forensics unavailable" });
  }
}
