export async function listStacks() {
  return (await fetch(`/api/ops/stacks`)).json();
}

export async function stackStatus(name: string) {
  return (await fetch(`/api/ops/stacks/${name}/status`)).json();
}

export async function stackUp(name: string) {
  return (await fetch(`/api/ops/stacks/${name}/up`, { method: "POST" })).json();
}

export async function stackDown(name: string) {
  return (await fetch(`/api/ops/stacks/${name}/down`, { method: "POST" })).json();
}

export async function stackRestart(name: string) {
  return (await fetch(`/api/ops/stacks/${name}/restart`, { method: "POST" })).json();
}

export async function stackScale(name: string, service: string, replicas: number) {
  const p = new URLSearchParams({ service, replicas: String(replicas) });
  return (await fetch(`/api/ops/stacks/${name}/scale?${p}`, { method: "POST" })).json();
}

export function streamLogs(
  name: string,
  opts?: { service?: string; tail?: number; signal?: AbortSignal },
) {
  const p = new URLSearchParams();
  if (opts?.service) p.set("service", opts.service);
  if (opts?.tail) p.set("tail", String(opts.tail));
  return fetch(`/api/ops/stacks/${name}/logs?${p}`, { signal: opts?.signal });
}
