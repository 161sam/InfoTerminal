import type { NextApiRequest, NextApiResponse } from "next";
import fs from "fs";
import path from "path";

const STATE_FILE = path.resolve(process.cwd(), "..", "..", "tmp", "plugins-state.json");

function ensureDir(p: string) {
  const dir = path.dirname(p);
  try {
    fs.mkdirSync(dir, { recursive: true });
  } catch {}
}

function readState(): any {
  try {
    const raw = fs.readFileSync(STATE_FILE, "utf8");
    return JSON.parse(raw);
  } catch {
    return { items: [] };
  }
}

function writeState(data: any) {
  try {
    ensureDir(STATE_FILE);
    fs.writeFileSync(STATE_FILE, JSON.stringify(data, null, 2));
  } catch {
    // ignore write errors in read-only environments
  }
}

function envInt(name: string, def: number): number {
  const v = process.env[name];
  if (!v) return def;
  const n = parseInt(v, 10);
  return Number.isFinite(n) ? n : def;
}

function defaultState() {
  const alephPort = envInt("IT_PORT_ALEPH", 8641);
  const supersetPort = envInt("IT_PORT_SUPERSET", 8644);
  const nifiPort = envInt("IT_PORT_NIFI", 8619);
  const airflowPort = envInt("IT_PORT_AIRFLOW", 8642);
  return {
    items: [
      {
        name: "aleph",
        enabled: true,
        endpoints: { baseUrl: `http://localhost:${alephPort}` },
        config: {},
      },
      {
        name: "superset",
        enabled: true,
        endpoints: { baseUrl: `http://localhost:${supersetPort}` },
        config: {},
      },
      {
        name: "nifi",
        enabled: true,
        endpoints: { baseUrl: `http://localhost:${nifiPort}/nifi` },
        config: {},
      },
      {
        name: "airflow",
        enabled: true,
        endpoints: { baseUrl: `http://localhost:${airflowPort}` },
        config: {},
      },
    ],
  };
}

export default function handler(_req: NextApiRequest, res: NextApiResponse) {
  const st = readState();
  if (!st.items || !Array.isArray(st.items) || st.items.length === 0) {
    const def = defaultState();
    writeState(def);
    return res.status(200).json(def);
  }
  return res.status(200).json(st);
}
