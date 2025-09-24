# OIDC Quickstart (Frontend)

This guide shows how to run the InfoTerminal frontend against a minimal OpenID Connect
identity provider using the built-in PKCE flow. The setup is idempotent and designed for
offline smoke testing via the provided mock IdP.

## 1. Environment flags

Add the following variables to your frontend `.env.local` (values shown are the defaults
used by the mock server):

```env
AUTH_REQUIRED=0
OIDC_ISSUER=http://localhost:8089/realms/mock
OIDC_CLIENT_ID=infoterminal-frontend
OIDC_REDIRECT_URI=http://localhost:3411/auth/callback
NEXT_PUBLIC_AUTH_REQUIRED=${AUTH_REQUIRED}
NEXT_PUBLIC_OIDC_ISSUER=${OIDC_ISSUER}
NEXT_PUBLIC_OIDC_CLIENT_ID=${OIDC_CLIENT_ID}
NEXT_PUBLIC_OIDC_REDIRECT_URI=${OIDC_REDIRECT_URI}
```

The root `.env.example` mirrors these flags so they can also be exported globally when
running the full compose stack.

- `AUTH_REQUIRED`: toggle for enforcing the login UI (`1` in secure environments, `0`
  for local smoke tests).
- `OIDC_ISSUER`: base URL of the IdP realm.
- `OIDC_CLIENT_ID`: public client configured at the IdP.
- `OIDC_REDIRECT_URI`: callback served by Next.js (`/auth/callback`).

> **Token handling** – Access tokens are stored in memory only. The refresh token is
> persisted as an `HttpOnly` cookie issued by `/api/auth/oidc/token` so the browser cannot
> script it. When the frontend reloads, `/api/auth/session` exchanges the refresh token for
> a fresh access token.

## 2. Start the mock IdP (offline smoke)

The repository contains a deterministic stub that implements the OIDC authorisation code
flow with PKCE:

```bash
python scripts/mock_oidc.py
```

The server listens on `http://localhost:8089` and exposes:

- `/.well-known/openid-configuration`
- `/protocol/openid-connect/auth`
- `/protocol/openid-connect/token`
- `/protocol/openid-connect/userinfo`
- `/protocol/openid-connect/logout`

It automatically redirects back to `/auth/callback` with a mock code and returns static
ID/access tokens so the frontend round-trip can be tested without Keycloak.

## 3. Run the frontend

Install dependencies and start the dev server:

```bash
pnpm install
pnpm --filter @infoterminal/frontend dev
```

Visit `http://localhost:3411/login` and click **Continue with SSO**. The browser will be
redirected to the mock IdP, receive the code, and return to `/auth/callback`. On success
it stores the new access token in memory, sets a `refresh_token` HttpOnly cookie, and
redirects back to the original page.

You can trigger a logout by visiting `/logout` or using the avatar menu. The logout route
clears the refresh cookie and offers the IdP end-session URL when available.

### Session renewal, route guards & remember-me

- The login form exposes a **Stay signed in for 30 days** toggle. When enabled the
  backend issues a `refresh_token` cookie with a 30-day TTL (instead of the default 7
  days) plus a companion `it_remember_me` flag. Subsequent silent refreshes honour this
  preference until logout.
- Search, Graph, Dossier and Settings pages now ship SSR/CSR guards. Requests without a
  valid refresh cookie are redirected to `/login?returnTo=…` on the server, while the
  client-side guard shows a neutral loading spinner before enforcing the redirect.
- A global fetch interceptor catches `401` responses, calls `/api/auth/refresh`, and
  retries the original request once. If the refresh fails, the session is cleared and the
  user is routed back to `/login`.

## 4. CSRF and SameSite policy

The refresh cookie is issued with `SameSite=Lax` during development to allow local
redirects (frontends and IdP usually share `localhost`). In production (`NODE_ENV=production`)
the cookie is upgraded to `SameSite=Strict` and `Secure`, matching the gateway/Keycloak
deployment. When integrating with a reverse proxy, make sure the proxy forwards the
`refresh_token` cookie unchanged and that the IdP callback is served over HTTPS to avoid
mixed content.

If you deploy behind a different domain than the IdP, adjust `COOKIE_DOMAIN` so the
Next.js API routes can scope the refresh cookie correctly.

## 5. Troubleshooting

- **State mismatch / session expired** – the PKCE verifier and state are stored in
  `sessionStorage` under the prefix `it.oidc.*`. Clear the browser storage and restart the
  login if the state check fails.
- **No redirect after logout** – the mock IdP does not invalidate refresh tokens; simply
  return to `/login` and restart the flow. Real providers should honour the `post_logout_redirect_uri`.
- **Custom IdP** – replace the values above with your issuer, client id, and callback
  URL. The frontend fetches the `.well-known` metadata, so non-Keycloak providers work as
  long as they implement the standard endpoints.
