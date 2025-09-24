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
  const { enabled } = req.body as { enabled?: boolean };
  if (typeof enabled !== "boolean")
    return res.status(400).json({ error: "enabled must be boolean" });

  const st = readState();
  const idx = (st.items || []).findIndex((p: any) => p.name === name);
  if (idx >= 0) {
    st.items[idx].enabled = enabled;
  } else {
    (st.items ||= []).push({ name, enabled });
  }
  writeState(st);
  return res.status(200).json({ name, enabled });
}
