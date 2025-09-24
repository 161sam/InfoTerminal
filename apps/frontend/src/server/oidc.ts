import type { NextApiResponse } from "next";
import type { User } from "@/types/auth";
import { canonicalizeRoles } from "@/lib/auth/rbac";

const REFRESH_COOKIE_NAME = "refresh_token";
const ACCESS_COOKIE_NAME = "auth_token";
const DEFAULT_REFRESH_MAX_AGE = 60 * 60 * 24 * 7; // 7 days
const REMEMBER_COOKIE_NAME = "it_remember_me";
const REMEMBER_REFRESH_MAX_AGE = 60 * 60 * 24 * 30; // 30 days
const METADATA_TTL = 5 * 60 * 1000; // 5 minutes

interface OidcMetadata {
  authorization_endpoint: string;
  token_endpoint: string;
  userinfo_endpoint?: string;
  end_session_endpoint?: string;
}

interface TokenResponse {
  access_token: string;
  refresh_token?: string;
  id_token?: string;
  expires_in: number;
  refresh_expires_in?: number;
  token_type?: string;
  scope?: string;
}

interface CachedMetadata {
  metadata: OidcMetadata;
  expiresAt: number;
}

const issuer =
  process.env.OIDC_ISSUER ||
  process.env.IT_OIDC_ISSUER ||
  process.env.NEXT_PUBLIC_OIDC_ISSUER ||
  "";

const clientId = process.env.OIDC_CLIENT_ID || process.env.NEXT_PUBLIC_OIDC_CLIENT_ID || "";

const redirectUri =
  process.env.OIDC_REDIRECT_URI || process.env.NEXT_PUBLIC_OIDC_REDIRECT_URI || "";

let metadataCache: CachedMetadata | null = null;

function requireValue(value: string, name: string): string {
  if (!value) {
    throw new Error(`Missing required OIDC setting: ${name}`);
  }
  return value;
}

export function getIssuer(): string {
  return requireValue(issuer, "OIDC_ISSUER");
}

export function getClientId(): string {
  return requireValue(clientId, "OIDC_CLIENT_ID");
}

export function getRedirectUri(): string {
  return requireValue(redirectUri, "OIDC_REDIRECT_URI");
}

function withDefaultEndpoints(base: string): OidcMetadata {
  const normalized = base.replace(/\/?$/, "");
  return {
    authorization_endpoint: `${normalized}/protocol/openid-connect/auth`,
    token_endpoint: `${normalized}/protocol/openid-connect/token`,
    userinfo_endpoint: `${normalized}/protocol/openid-connect/userinfo`,
    end_session_endpoint: `${normalized}/protocol/openid-connect/logout`,
  };
}

export async function getOidcMetadata(): Promise<OidcMetadata> {
  const now = Date.now();
  if (metadataCache && metadataCache.expiresAt > now) {
    return metadataCache.metadata;
  }

  const base = getIssuer();
  const wellKnown = `${base.replace(/\/?$/, "")}/.well-known/openid-configuration`;

  try {
    const response = await fetch(wellKnown, {
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`OIDC metadata request failed: ${response.status}`);
    }

    const data = (await response.json()) as Partial<OidcMetadata>;
    const metadata: OidcMetadata = {
      authorization_endpoint:
        data.authorization_endpoint || withDefaultEndpoints(base).authorization_endpoint,
      token_endpoint: data.token_endpoint || withDefaultEndpoints(base).token_endpoint,
      userinfo_endpoint: data.userinfo_endpoint || withDefaultEndpoints(base).userinfo_endpoint,
      end_session_endpoint:
        data.end_session_endpoint || withDefaultEndpoints(base).end_session_endpoint,
    };

    metadataCache = {
      metadata,
      expiresAt: now + METADATA_TTL,
    };
    return metadata;
  } catch (error) {
    console.warn("Falling back to default OIDC endpoints", error);
    const metadata = withDefaultEndpoints(base);
    metadataCache = {
      metadata,
      expiresAt: now + METADATA_TTL,
    };
    return metadata;
  }
}

async function requestToken(params: URLSearchParams): Promise<TokenResponse> {
  const metadata = await getOidcMetadata();

  const response = await fetch(metadata.token_endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Accept: "application/json",
    },
    body: params.toString(),
  });

  const payload = await response.json();
  if (!response.ok) {
    const error = new Error("OIDC token request failed");
    (error as any).status = response.status;
    (error as any).payload = payload;
    throw error;
  }

  return payload as TokenResponse;
}

export async function exchangeAuthorizationCode(
  code: string,
  codeVerifier: string,
  overrideRedirectUri?: string,
): Promise<TokenResponse> {
  const params = new URLSearchParams({
    grant_type: "authorization_code",
    code,
    client_id: getClientId(),
    code_verifier: codeVerifier,
    redirect_uri: overrideRedirectUri || getRedirectUri(),
  });

  return requestToken(params);
}

export async function refreshWithToken(refreshToken: string): Promise<TokenResponse> {
  const params = new URLSearchParams({
    grant_type: "refresh_token",
    refresh_token: refreshToken,
    client_id: getClientId(),
  });

  return requestToken(params);
}

function base64UrlDecode(input: string): string {
  const normalized = input.replace(/-/g, "+").replace(/_/g, "/");
  const padded = normalized.padEnd(normalized.length + ((4 - (normalized.length % 4)) % 4), "=");
  return Buffer.from(padded, "base64").toString("utf-8");
}

export function decodeIdToken(idToken?: string): Record<string, any> | null {
  if (!idToken) return null;
  const parts = idToken.split(".");
  if (parts.length < 2) return null;
  try {
    const payload = base64UrlDecode(parts[1]);
    return JSON.parse(payload);
  } catch (error) {
    console.error("Failed to decode id_token", error);
    return null;
  }
}

export function mapClaimsToUser(claims: Record<string, any> | null): User | null {
  if (!claims) return null;

  const collectedRoles: string[] = [];

  const collectRoles = (value: unknown) => {
    if (!value) return;
    if (Array.isArray(value)) {
      value.forEach((item) => collectRoles(item));
      return;
    }
    if (typeof value === "string") {
      value
        .split(/[\s,]+/)
        .map((entry) => entry.trim())
        .filter(Boolean)
        .forEach((entry) => collectedRoles.push(entry));
    }
  };

  collectRoles(claims.roles);
  collectRoles(claims.role);
  collectRoles(claims?.realm_access?.roles);
  collectRoles(claims?.resource_access?.account?.roles);
  collectRoles(claims["x-roles"]);
  collectRoles(claims["X-Roles"]);

  const collectScopes = (value: unknown) => {
    if (!value) return;
    if (Array.isArray(value)) {
      value.forEach((item) => collectScopes(item));
      return;
    }
    if (typeof value === "string") {
      collectRoles(value);
    }
  };

  collectScopes(claims.scope);
  collectScopes(claims.scp);

  const canonicalRoles = canonicalizeRoles(collectedRoles);

  const permissions: string[] = Array.isArray(claims.permissions)
    ? claims.permissions
    : typeof claims.permissions === "string"
      ? claims.permissions
          .split(/[\s,]+/)
          .map((entry: string) => entry.trim())
          .filter(Boolean)
      : [];

  return {
    id: String(claims.sub || claims.user_id || ""),
    email: claims.email || "",
    name: claims.name || claims.preferred_username || claims.email || "",
    display_name: claims.name || claims.preferred_username || claims.email || undefined,
    first_name: claims.given_name || undefined,
    last_name: claims.family_name || undefined,
    avatar: claims.picture || undefined,
    avatar_url: claims.picture || undefined,
    roles: canonicalRoles,
    permissions,
    tenant: claims.tenant || claims.org || claims.organization || undefined,
    lastLogin: claims.auth_time ? new Date(claims.auth_time * 1000).toISOString() : undefined,
    createdAt: claims.created_at ? new Date(claims.created_at * 1000).toISOString() : undefined,
    updatedAt: claims.updated_at ? new Date(claims.updated_at * 1000).toISOString() : undefined,
    metadata: claims,
  };
}

function appendCookies(res: NextApiResponse, cookies: string[]) {
  const existing = res.getHeader("Set-Cookie");
  if (existing) {
    if (Array.isArray(existing)) {
      res.setHeader("Set-Cookie", [...existing, ...cookies]);
    } else {
      res.setHeader("Set-Cookie", [existing as string, ...cookies]);
    }
  } else {
    res.setHeader("Set-Cookie", cookies);
  }
}

function buildCookieString(
  name: string,
  value: string,
  options: { maxAge?: number; clear?: boolean } = {},
): string {
  const isProduction = process.env.NODE_ENV === "production";
  const sameSite = process.env.OIDC_COOKIE_SAMESITE || (isProduction ? "Strict" : "Lax");
  const domain = process.env.COOKIE_DOMAIN;
  if (options.clear) {
    return `${name}=; HttpOnly; Path=/; Max-Age=0; SameSite=${sameSite}${isProduction ? "; Secure" : ""}${domain ? `; Domain=${domain}` : ""}`;
  }
  const maxAge = options.maxAge ?? DEFAULT_REFRESH_MAX_AGE;
  return `${name}=${value}; HttpOnly; Path=/; Max-Age=${maxAge}; SameSite=${sameSite}${isProduction ? "; Secure" : ""}${domain ? `; Domain=${domain}` : ""}`;
}

export function buildSessionPayload(
  res: NextApiResponse,
  token: TokenResponse,
  options: { remember?: boolean } = {},
) {
  if (token.refresh_token) {
    setRefreshCookie(res, token.refresh_token, token.refresh_expires_in, options);
  }
  ensureNoCache(res);
  const claims = decodeIdToken(token.id_token);
  const user = mapClaimsToUser(claims);

  return {
    accessToken: token.access_token,
    expiresIn: token.expires_in,
    idToken: token.id_token ?? null,
    scope: token.scope ?? null,
    tokenType: token.token_type ?? "Bearer",
    user,
  };
}

export function setRefreshCookie(
  res: NextApiResponse,
  refreshToken: string,
  refreshExpiresIn?: number,
  options: { remember?: boolean } = {},
) {
  const baseAge =
    refreshExpiresIn && refreshExpiresIn > 0 ? refreshExpiresIn : DEFAULT_REFRESH_MAX_AGE;
  const effectiveMaxAge = options.remember ? Math.max(baseAge, REMEMBER_REFRESH_MAX_AGE) : baseAge;
  const cookies = [
    buildCookieString(REFRESH_COOKIE_NAME, refreshToken, {
      maxAge: effectiveMaxAge,
    }),
    buildCookieString(ACCESS_COOKIE_NAME, "", { clear: true }),
  ];
  if (typeof options.remember === "boolean") {
    cookies.push(
      options.remember
        ? buildCookieString(REMEMBER_COOKIE_NAME, "1", { maxAge: REMEMBER_REFRESH_MAX_AGE })
        : buildCookieString(REMEMBER_COOKIE_NAME, "", { clear: true }),
    );
  }
  appendCookies(res, cookies);
}

export function clearAuthCookies(res: NextApiResponse) {
  appendCookies(res, [
    buildCookieString(REFRESH_COOKIE_NAME, "", { clear: true }),
    buildCookieString(ACCESS_COOKIE_NAME, "", { clear: true }),
    buildCookieString(REMEMBER_COOKIE_NAME, "", { clear: true }),
  ]);
}

export function ensureNoCache(res: NextApiResponse) {
  res.setHeader("Cache-Control", "no-store, no-cache, must-revalidate");
  res.setHeader("Pragma", "no-cache");
}

export { REMEMBER_COOKIE_NAME };
export type { TokenResponse };
