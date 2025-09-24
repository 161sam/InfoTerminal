import type { NextApiRequest, NextApiResponse } from "next";

function hubUrl() {
  const port = process.env.IT_PORT_COLLAB || "8625";
  return process.env.COLLAB_URL || `http://localhost:${port}`;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const base = hubUrl();

  try {
    const response = await fetch(`${base}/dossier/templates`);
    const data = await response.json();
    return res.status(response.status).json(data);
  } catch (error) {
    const message = error instanceof Error ? error.message : "collab-hub unavailable";
    return res.status(502).json({ error: message });
  }
}
