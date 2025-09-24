// pages/api/auth/me.ts
import type { NextApiRequest, NextApiResponse } from "next";

const AUTH_SERVICE_URL = process.env.AUTH_SERVICE_URL || "http://localhost:8080";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const authToken = req.cookies.auth_token;

    if (!authToken) {
      return res.status(401).json({ error: "Not authenticated" });
    }

    // Forward request to auth service
    const response = await fetch(`${AUTH_SERVICE_URL}/auth/me`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${authToken}`,
        "Content-Type": "application/json",
        "X-Request-ID": generateRequestId(),
      },
    });

    const data = await response.json();

    if (!response.ok) {
      // If token is invalid, clear cookies
      if (response.status === 401) {
        const isProduction = process.env.NODE_ENV === "production";
        const domain = process.env.COOKIE_DOMAIN;

        res.setHeader("Set-Cookie", [
          `auth_token=; HttpOnly; Path=/; Max-Age=0; SameSite=Strict${isProduction ? "; Secure" : ""}${domain ? `; Domain=${domain}` : ""}`,
          `refresh_token=; HttpOnly; Path=/; Max-Age=0; SameSite=Strict${isProduction ? "; Secure" : ""}${domain ? `; Domain=${domain}` : ""}`,
        ]);
      }
      return res.status(response.status).json(data);
    }

    return res.status(200).json(data);
  } catch (error) {
    console.error("Get user error:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
}

function generateRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
