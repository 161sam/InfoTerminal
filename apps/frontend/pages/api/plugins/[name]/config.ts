import type { NextApiRequest, NextApiResponse } from "next";
import fs from "fs";
import path from "path";

const STATE_FILE = path.resolve(process.cwd(), "..", "..", "tmp", "plugins-state.json");

function readState(): any {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, "utf8"));
  } catch {
    return { items: [] };
  }
}
function writeState(data: any) {
  try {
    fs.mkdirSync(path.dirname(STATE_FILE), { recursive: true });
    fs.writeFileSync(STATE_FILE, JSON.stringify(data, null, 2));
  } catch {
    /* ignore in read-only env */
  }
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") return res.status(405).end();
  const { name } = req.query as { name: string };
  const { config } = req.body as { config?: Record<string, any> };
  if (!config || typeof config !== "object")
    return res.status(400).json({ error: "config must be object" });

  // Do not persist obvious secrets
  const sanitized = JSON.parse(JSON.stringify(config));
  const deny = ["password", "apiKey", "token", "secret"];
  for (const key of Object.keys(sanitized)) {
    if (deny.includes(key.toLowerCase())) sanitized[key] = "***";
  }

  const st = readState();
  const idx = (st.items || []).findIndex((p: any) => p.name === name);
  if (idx >= 0) {
    st.items[idx].config = sanitized;
  } else {
    (st.items ||= []).push({ name, enabled: true, config: sanitized });
  }
  writeState(st);
  return res.status(200).json({ name, config: sanitized });
}
