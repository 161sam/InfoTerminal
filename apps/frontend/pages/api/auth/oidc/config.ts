import type { NextApiRequest, NextApiResponse } from "next";
import {
  ensureNoCache,
  getClientId,
  getIssuer,
  getOidcMetadata,
  getRedirectUri,
} from "@/server/oidc";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const metadata = await getOidcMetadata();
    ensureNoCache(res);

    return res.status(200).json({
      issuer: getIssuer(),
      authorizationEndpoint: metadata.authorization_endpoint,
      tokenEndpoint: metadata.token_endpoint,
      userinfoEndpoint: metadata.userinfo_endpoint ?? null,
      endSessionEndpoint: metadata.end_session_endpoint ?? null,
      clientId: getClientId(),
      redirectUri: getRedirectUri(),
      scope: process.env.OIDC_SCOPE || "openid profile email",
    });
  } catch (error: any) {
    console.error("Failed to load OIDC config", error);
    return res.status(500).json({
      error: error?.message || "Failed to load OIDC configuration",
    });
  }
}
