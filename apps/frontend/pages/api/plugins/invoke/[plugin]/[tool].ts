import type { NextApiRequest, NextApiResponse } from "next";

function prUrl(): string {
  const port = process.env.IT_PORT_PLUGIN_RUNNER || "8621";
  return process.env.PLUGIN_RUNNER_URL || `http://localhost:${port}`;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") return res.status(405).end();
  const { plugin, tool } = req.query as { plugin: string; tool: string };
  const payload = req.body || {};

  try {
    const base = prUrl();
    const exec = await fetch(`${base}/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        plugin_name: plugin,
        // Use tool name as scan_type to select command template in registry
        parameters: { scan_type: tool, ...(typeof payload === "object" ? payload : {}) },
        output_format: "json",
      }),
    });

    if (!exec.ok) {
      const txt = await exec.text();
      return res.status(exec.status).send(txt);
    }
    const job = await exec.json();
    return res.status(200).json(job);
  } catch (e: any) {
    return res.status(502).json({ error: e?.message || "plugin-runner unavailable" });
  }
}
