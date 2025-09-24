import type { NextApiRequest, NextApiResponse } from "next";
import {
  clearAuthCookies,
  ensureNoCache,
  getClientId,
  getOidcMetadata,
  getRedirectUri,
} from "@/server/oidc";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    clearAuthCookies(res);
    ensureNoCache(res);

    let endSessionUrl: string | null = null;
    const { idToken } = (req.body as { idToken?: string }) || {};

    if (idToken) {
      try {
        const metadata = await getOidcMetadata();
        if (metadata.end_session_endpoint) {
          const params = new URLSearchParams({
            id_token_hint: idToken,
            post_logout_redirect_uri: getRedirectUri(),
            client_id: getClientId(),
          });
          endSessionUrl = `${metadata.end_session_endpoint}?${params.toString()}`;
        }
      } catch (error) {
        console.warn("Failed to resolve OIDC end session endpoint", error);
      }
    }

    return res.status(200).json({ success: true, endSessionUrl });
  } catch (error: any) {
    console.error("Logout handler failed", error);
    return res.status(500).json({ error: error?.message || "Logout failed" });
  }
}
