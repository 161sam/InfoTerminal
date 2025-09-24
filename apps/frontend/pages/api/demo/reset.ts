import type { NextApiRequest, NextApiResponse } from "next";
import fs from "fs";
import { paths } from "@/lib/demoLoader";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (process.env.NODE_ENV === "production" && process.env.ALLOW_DEMO_LOADER !== "1") {
    res.status(403).json({ ok: false, error: "disabled" });
    return;
  }
  if (req.method !== "POST") {
    res.status(405).json({ ok: false });
    return;
  }
  try {
    fs.rmSync(paths.LOADED_FILE, { force: true });
    res.status(200).json({ ok: true });
  } catch (e: any) {
    res.status(500).json({ ok: false, error: e.message });
  }
}
