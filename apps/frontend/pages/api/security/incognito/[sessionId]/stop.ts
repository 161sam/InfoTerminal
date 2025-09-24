// pages/api/security/incognito/[sessionId]/stop.ts
import type { NextApiRequest, NextApiResponse } from "next";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<{ success: boolean } | { error: string }>,
) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { sessionId } = req.query;

  if (!sessionId || typeof sessionId !== "string") {
    return res.status(400).json({ error: "Session ID is required" });
  }

  try {
    // Call ops controller to stop incognito session
    const opsControllerUrl = process.env.OPS_CONTROLLER_URL || "http://localhost:8614";
    const response = await fetch(`${opsControllerUrl}/security/incognito/${sessionId}/stop`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Failed to stop incognito session");
    }

    res.status(200).json({ success: true });
  } catch (error) {
    console.error("Failed to stop incognito session:", error);
    res.status(500).json({ error: "Failed to stop incognito session" });
  }
}
