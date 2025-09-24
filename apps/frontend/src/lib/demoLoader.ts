import fs from "fs";
import path from "path";
import { createHash } from "crypto";

const ROOT = path.join(process.cwd(), "..", "..");
const DEMO_DIR = path.join(ROOT, "examples", "docs");
const LOADED_FILE = path.join(ROOT, "data", "demo", "loaded.json");
const SEED_FILE = path.join(ROOT, "examples", "seeds", "entities.json");

export type LoadedEntry = { file: string; aleph_id?: string };
export type LoadedState = Record<string, LoadedEntry>;

export function listDemoFiles(): string[] {
  try {
    return fs.readdirSync(DEMO_DIR).map((f) => path.join(DEMO_DIR, f));
  } catch {
    return [];
  }
}

export function fileSha1(filePath: string): string {
  const buf = fs.readFileSync(filePath);
  return createHash("sha1").update(buf).digest("hex");
}

export function readLoaded(): LoadedState {
  try {
    return JSON.parse(fs.readFileSync(LOADED_FILE, "utf-8")) as LoadedState;
  } catch {
    return {};
  }
}

export function writeLoaded(state: LoadedState) {
  fs.mkdirSync(path.dirname(LOADED_FILE), { recursive: true });
  fs.writeFileSync(LOADED_FILE, JSON.stringify(state, null, 2));
}

export async function ingestToAleph(filePath: string) {
  const base = process.env.ALEPH_BASE_URL || "";
  const apiKey = process.env.ALEPH_API_KEY || "";
  const buf = fs.readFileSync(filePath);
  const form = new FormData();
  form.append("file", new Blob([buf]), path.basename(filePath));
  form.append("title", path.basename(filePath));
  form.append("source", "demo-loader");
  const res = await fetch(base + "/ingest", {
    method: "POST",
    headers: { Authorization: `ApiKey ${apiKey}` },
    body: form,
  });
  if (!res.ok) throw new Error("Aleph ingest failed");
  return res.json();
}

export async function annotateText(text: string, meta: any) {
  const base = process.env.DOCENTITIES_API || process.env.NEXT_PUBLIC_DOCENTITIES_API || "";
  const res = await fetch(base + "/annotate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, meta }),
  });
  if (!res.ok) throw new Error("Annotate failed");
  return res.json();
}

export async function loadSeeds(opts: { seedGraph?: boolean; seedSearch?: boolean }) {
  if (!fs.existsSync(SEED_FILE)) return [] as string[];
  const data = JSON.parse(fs.readFileSync(SEED_FILE, "utf-8"));
  const notes: string[] = [];
  if (opts.seedSearch && data.items) {
    try {
      await fetch((process.env.SEARCH_API || "") + "/seed", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source: "demo-loader", items: data.items }),
      });
    } catch {
      notes.push("seed search failed");
    }
  }
  if (opts.seedGraph && data.nodes) {
    try {
      await fetch((process.env.GRAPH_API || "") + "/seed", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nodes: data.nodes, rels: data.rels }),
      });
    } catch {
      notes.push("seed graph failed");
    }
  }
  return notes;
}

export const paths = { LOADED_FILE };
