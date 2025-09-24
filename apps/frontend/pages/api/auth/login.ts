// pages/api/auth/login.ts
import type { NextApiRequest, NextApiResponse } from "next";

const AUTH_SERVICE_URL = process.env.AUTH_SERVICE_URL || "http://localhost:8080";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { email, password, mfa_token, remember_me } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: "Email and password are required" });
    }

    // Forward request to auth service
    const response = await fetch(`${AUTH_SERVICE_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Request-ID": (req.headers["x-request-id"] as string) || generateRequestId(),
        "User-Agent": req.headers["user-agent"] || "InfoTerminal-Frontend",
      },
      body: JSON.stringify({
        email,
        password,
        mfa_token,
        remember_me: remember_me || false,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json(data);
    }

    // Set secure cookies for tokens if login successful
    if (data.access_token && !data.requires_mfa) {
      const isProduction = process.env.NODE_ENV === "production";
      const domain = process.env.COOKIE_DOMAIN;

      // Set access token cookie (short-lived)
      res.setHeader("Set-Cookie", [
        `auth_token=${data.access_token}; HttpOnly; Path=/; Max-Age=1800; SameSite=Strict${isProduction ? "; Secure" : ""}${domain ? `; Domain=${domain}` : ""}`,
        `refresh_token=${data.refresh_token}; HttpOnly; Path=/; Max-Age=604800; SameSite=Strict${isProduction ? "; Secure" : ""}${domain ? `; Domain=${domain}` : ""}`,
      ]);
    }

    return res.status(200).json(data);
  } catch (error) {
    console.error("Login error:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
}

function generateRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
