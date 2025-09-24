import type { NextApiRequest, NextApiResponse } from "next";
import {
  buildSessionPayload,
  clearAuthCookies,
  ensureNoCache,
  refreshWithToken,
  REMEMBER_COOKIE_NAME,
} from "@/server/oidc";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const refreshToken = req.cookies?.refresh_token;
  if (!refreshToken) {
    ensureNoCache(res);
    return res.status(401).json({ error: "Not authenticated" });
  }

  try {
    const tokenResponse = await refreshWithToken(refreshToken);
    const payload = buildSessionPayload(res, tokenResponse, {
      remember: req.cookies?.[REMEMBER_COOKIE_NAME] === "1",
    });
    ensureNoCache(res);
    return res.status(200).json(payload);
  } catch (error: any) {
    const status = typeof error?.status === "number" ? error.status : 500;
    if (status === 401) {
      clearAuthCookies(res);
    }
    const responseBody = error?.payload || { error: error?.message || "Session restore failed" };
    return res.status(status).json(responseBody);
  }
}
