import type { NextApiRequest, NextApiResponse } from "next";

const OPS_CONTROLLER_URL = process.env.OPS_CONTROLLER_URL || "http://localhost:8614";

// Utility function to safely convert header values to strings
function getHeaderValue(value: string | string[] | undefined, defaultValue: string): string {
  if (Array.isArray(value)) {
    return value[0] || defaultValue;
  }
  return value || defaultValue;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { name, service, replicas } = req.query;

  if (typeof name !== "string") {
    return res.status(400).json({ error: "Invalid stack name" });
  }

  if (typeof service !== "string") {
    return res.status(400).json({ error: "Service parameter required" });
  }

  if (typeof replicas !== "string" || isNaN(Number(replicas))) {
    return res.status(400).json({ error: "Replicas parameter must be a number" });
  }

  try {
    const params = new URLSearchParams({ service, replicas });
    const response = await fetch(
      `${OPS_CONTROLLER_URL}/ops/stacks/${encodeURIComponent(name)}/scale?${params}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // Forward user context for RBAC
          "X-User-Id": getHeaderValue(req.headers["x-user-id"], "system"),
          "X-Roles": getHeaderValue(req.headers["x-roles"], "admin"),
          "X-Scope": getHeaderValue(req.headers["x-scope"], "infra"),
          "X-Tenant-Id": getHeaderValue(req.headers["x-tenant-id"], "default"),
        },
      },
    );

    if (!response.ok) {
      const error = await response.text();
      return res.status(response.status).json({
        error: `Ops controller error: ${error}`,
      });
    }

    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    console.error("Error proxying to ops-controller:", error);
    res.status(500).json({
      error: "Failed to scale service",
      details: error instanceof Error ? error.message : "Unknown error",
    });
  }
}
