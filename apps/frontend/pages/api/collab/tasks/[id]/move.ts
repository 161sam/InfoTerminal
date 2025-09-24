import type { NextApiRequest, NextApiResponse } from "next";

function hubUrl() {
  const port = process.env.IT_PORT_COLLAB || "8625";
  return process.env.COLLAB_URL || `http://localhost:${port}`;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") return res.status(405).end();
  const { id } = req.query as { id: string };
  const { to } = req.body as { to?: string };
  try {
    const r = await fetch(`${hubUrl()}/tasks/${id}/move?to=${encodeURIComponent(to || "")}`, {
      method: "POST",
    });
    const data = await r.json();
    return res.status(r.status).json(data);
  } catch (e: any) {
    return res.status(502).json({ error: e?.message || "collab-hub unavailable" });
  }
}
