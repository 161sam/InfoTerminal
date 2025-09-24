import type { NextApiRequest, NextApiResponse } from "next";
import { ensureNoCache, getOidcMetadata } from "@/server/oidc";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const authorization = req.headers.authorization;
  if (!authorization || !authorization.startsWith("Bearer ")) {
    ensureNoCache(res);
    return res.status(401).json({ error: "Missing access token" });
  }

  const accessToken = authorization.slice("Bearer ".length);

  try {
    const metadata = await getOidcMetadata();
    if (!metadata.userinfo_endpoint) {
      ensureNoCache(res);
      return res.status(501).json({ error: "Userinfo endpoint not available" });
    }

    const response = await fetch(metadata.userinfo_endpoint, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        Accept: "application/json",
      },
    });

    ensureNoCache(res);

    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      return res.status(response.status).json(body);
    }

    const data = await response.json();
    return res.status(200).json(data);
  } catch (error: any) {
    console.error("Failed to load userinfo", error);
    ensureNoCache(res);
    return res.status(500).json({ error: error?.message || "Failed to load user profile" });
  }
}
