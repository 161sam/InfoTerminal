import type { NextApiRequest, NextApiResponse } from "next";

function hubUrl() {
  const port = process.env.IT_PORT_COLLAB || "8625";
  return process.env.COLLAB_URL || `http://localhost:${port}`;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { id } = req.query as { id: string };
  try {
    if (req.method === "DELETE") {
      const r = await fetch(`${hubUrl()}/tasks/${id}`, { method: "DELETE" });
      const data = await r.json();
      return res.status(r.status).json(data);
    }
    return res.status(405).end();
  } catch (e: any) {
    return res.status(502).json({ error: e?.message || "collab-hub unavailable" });
  }
}
