import type { NextApiRequest, NextApiResponse } from "next";
import {
  buildSessionPayload,
  clearAuthCookies,
  ensureNoCache,
  exchangeAuthorizationCode,
} from "@/server/oidc";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { code, codeVerifier, redirectUri } = req.body ?? {};

  if (!code || !codeVerifier) {
    return res.status(400).json({ error: "Missing authorization code or verifier" });
  }

  try {
    const tokenResponse = await exchangeAuthorizationCode(code, codeVerifier, redirectUri);
    const payload = buildSessionPayload(res, tokenResponse);
    ensureNoCache(res);
    return res.status(200).json(payload);
  } catch (error: any) {
    const status = typeof error?.status === "number" ? error.status : 500;
    if (status === 401 || status === 400) {
      clearAuthCookies(res);
    }
    const responseBody = error?.payload || {
      error: error?.message || "OIDC token exchange failed",
    };
    return res.status(status).json(responseBody);
  }
}
