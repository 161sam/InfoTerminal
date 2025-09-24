import type { NextApiRequest, NextApiResponse } from "next";

function hubUrl() {
  const port = process.env.IT_PORT_COLLAB || "8625";
  return process.env.COLLAB_URL || `http://localhost:${port}`;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const base = hubUrl();

  try {
    const response = await fetch(`${base}/dossier/export`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body || {}),
    });

    const contentType = response.headers.get("content-type") || "";

    if (!response.ok) {
      let details: unknown;
      try {
        details = await response.json();
      } catch (parseError) {
        details = await response.text();
      }
      return res.status(response.status).json({ error: "Export failed", details });
    }

    if (contentType.includes("application/pdf")) {
      const arrayBuffer = await response.arrayBuffer();
      const buffer = Buffer.from(arrayBuffer);
      const disposition = response.headers.get("content-disposition");
      if (disposition) {
        res.setHeader("Content-Disposition", disposition);
      }
      res.setHeader("Content-Type", "application/pdf");
      return res.status(200).send(buffer);
    }

    const data = await response.json();
    return res.status(200).json(data);
  } catch (error) {
    const message = error instanceof Error ? error.message : "collab-hub unavailable";
    return res.status(502).json({ error: message });
  }
}
