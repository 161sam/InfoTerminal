// pages/api/security/incognito/[sessionId]/containers.ts
import type { NextApiRequest, NextApiResponse } from "next";

interface EphemeralContainer {
  id: string;
  name: string;
  image: string;
  status: "running" | "stopped" | "created";
  created: number;
  memoryUsage: number;
  memoryLimit: number;
  ephemeral: boolean;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<{ containers: EphemeralContainer[] } | { error: string }>,
) {
  if (req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { sessionId } = req.query;

  if (!sessionId || typeof sessionId !== "string") {
    return res.status(400).json({ error: "Session ID is required" });
  }

  try {
    // Call ops controller to get containers for incognito session
    const opsControllerUrl = process.env.OPS_CONTROLLER_URL || "http://localhost:8614";
    const response = await fetch(`${opsControllerUrl}/security/incognito/${sessionId}/containers`, {
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Failed to get containers");
    }

    const data = await response.json();

    res.status(200).json({ containers: data.containers || [] });
  } catch (error) {
    console.error("Failed to get containers:", error);
    // Return empty containers list as fallback
    res.status(200).json({ containers: [] });
  }
}
