export async function invokeTool(plugin: string, tool: string, payload: any, init?: RequestInit) {
  const res = await fetch(`/api/plugins/invoke/${plugin}/${tool}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
export async function listTools() {
  const res = await fetch(`/api/plugins/tools`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
