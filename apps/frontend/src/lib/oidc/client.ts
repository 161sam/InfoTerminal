const STORAGE_PREFIX = "it.oidc.";
export const OIDC_STORAGE_KEYS = {
  codeVerifier: `${STORAGE_PREFIX}code_verifier`,
  state: `${STORAGE_PREFIX}state`,
  returnTo: `${STORAGE_PREFIX}return_to`,
  issuedAt: `${STORAGE_PREFIX}issued_at`,
};

export interface StoredOidcRequest {
  codeVerifier: string;
  state: string;
  returnTo?: string | null;
  issuedAt?: number;
}

function ensureBrowser() {
  if (typeof window === "undefined" || typeof window.crypto === "undefined") {
    throw new Error("OIDC PKCE flow requires a browser environment");
  }
}

function base64UrlEncode(buffer: ArrayBuffer | Uint8Array): string {
  const bytes = buffer instanceof Uint8Array ? buffer : new Uint8Array(buffer);
  let binary = "";
  const length = bytes.byteLength;
  for (let i = 0; i < length; i += 1) {
    binary += String.fromCharCode(bytes[i]!);
  }
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function randomBytes(size = 32): Uint8Array {
  const arr = new Uint8Array(size);
  window.crypto.getRandomValues(arr);
  return arr;
}

export function generateState(length = 32): string {
  ensureBrowser();
  return base64UrlEncode(randomBytes(length)).slice(0, length);
}

export async function generatePkcePair() {
  ensureBrowser();
  const codeVerifier = base64UrlEncode(randomBytes(64));
  const data = new TextEncoder().encode(codeVerifier);
  const digest = await window.crypto.subtle.digest("SHA-256", data);
  const codeChallenge = base64UrlEncode(digest);
  return { codeVerifier, codeChallenge };
}

export function storeOidcRequest(request: {
  codeVerifier: string;
  state: string;
  returnTo?: string | null;
}) {
  if (typeof sessionStorage === "undefined") return;
  sessionStorage.setItem(OIDC_STORAGE_KEYS.codeVerifier, request.codeVerifier);
  sessionStorage.setItem(OIDC_STORAGE_KEYS.state, request.state);
  if (request.returnTo) {
    sessionStorage.setItem(OIDC_STORAGE_KEYS.returnTo, request.returnTo);
  } else {
    sessionStorage.removeItem(OIDC_STORAGE_KEYS.returnTo);
  }
  sessionStorage.setItem(OIDC_STORAGE_KEYS.issuedAt, String(Date.now()));
}

export function loadOidcRequest(): StoredOidcRequest | null {
  if (typeof sessionStorage === "undefined") return null;
  const codeVerifier = sessionStorage.getItem(OIDC_STORAGE_KEYS.codeVerifier);
  const state = sessionStorage.getItem(OIDC_STORAGE_KEYS.state);
  if (!codeVerifier || !state) {
    return null;
  }
  const returnTo = sessionStorage.getItem(OIDC_STORAGE_KEYS.returnTo);
  const issuedAtRaw = sessionStorage.getItem(OIDC_STORAGE_KEYS.issuedAt);
  const issuedAt = issuedAtRaw ? Number(issuedAtRaw) : undefined;
  return { codeVerifier, state, returnTo, issuedAt };
}

export function clearOidcRequest() {
  if (typeof sessionStorage === "undefined") return;
  sessionStorage.removeItem(OIDC_STORAGE_KEYS.codeVerifier);
  sessionStorage.removeItem(OIDC_STORAGE_KEYS.state);
  sessionStorage.removeItem(OIDC_STORAGE_KEYS.returnTo);
  sessionStorage.removeItem(OIDC_STORAGE_KEYS.issuedAt);
}
