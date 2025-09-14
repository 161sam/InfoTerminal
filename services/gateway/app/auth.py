import os
import time
import logging
from typing import Optional, Dict, Any
import httpx
from jose import jwt, JWTError

log = logging.getLogger("gateway.auth")

ISSUER = os.getenv("IT_OIDC_ISSUER", "")
AUDIENCE = os.getenv("IT_OIDC_AUDIENCE", "")
JWKS_URL = os.getenv("IT_OIDC_JWKS_URL", "")
AUTH_REQUIRED = os.getenv("IT_AUTH_REQUIRED", "0") == "1"
SKEW = int(os.getenv("IT_OIDC_SKEW", "60"))

_JWKS_CACHE: Dict[str, Any] = {"keys": [], "ts": 0}
_CACHE_TTL = 300


async def _fetch_jwks() -> Dict[str, Any]:
    global _JWKS_CACHE
    now = time.time()
    if now - _JWKS_CACHE["ts"] < _CACHE_TTL and _JWKS_CACHE["keys"]:
        return _JWKS_CACHE
    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.get(JWKS_URL)
        r.raise_for_status()
        data = r.json()
        _JWKS_CACHE = {"keys": data.get("keys", []), "ts": now}
        return _JWKS_CACHE


async def validate_bearer(token: str) -> Optional[Dict[str, Any]]:
    try:
        jwks = await _fetch_jwks()
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        key = next((k for k in jwks["keys"] if k.get("kid") == kid), None)
        if not key:
            raise JWTError("unknown kid")
        claims = jwt.decode(
            token,
            key,
            audience=AUDIENCE,
            issuer=ISSUER,
            options={"verify_at_hash": False},
            leeway=SKEW,
        )
        return claims
    except Exception as e:
        log.warning("JWT validation failed: %s", e)
        return None


async def auth_context(request):
    """Returns (user_id, scopes, claims) or dev-fallback."""
    if not AUTH_REQUIRED:
        return ("dev", ["dev"], {})
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth.split(" ", 1)[1].strip()
    claims = await validate_bearer(token)
    if not claims:
        return None
    sub = claims.get("sub") or claims.get("email") or "anon"
    scopes = claims.get("scope", "").split() if claims.get("scope") else []
    return (sub, scopes, claims)
