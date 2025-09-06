import os, httpx, time
from jose import jwt
from cachetools import TTLCache

ISSUER = os.getenv("KEYCLOAK_ISSUER", "http://localhost:8081/realms/infoterminal")
AUDIENCE = os.getenv("KEYCLOAK_AUDIENCE", "search-api")
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"

_jwks_cache = TTLCache(maxsize=1, ttl=300)
_alg = "RS256"

def _get_jwks():
    if "jwks" in _jwks_cache:
        return _jwks_cache["jwks"]
    with httpx.Client(timeout=5.0) as c:
        r = c.get(JWKS_URL)
        r.raise_for_status()
        data = r.json()
        _jwks_cache["jwks"] = data
        return data

def verify_token(token: str):
    jwks = _get_jwks()
    try:
        return jwt.decode(
            token,
            jwks,
            algorithms=[_alg],
            audience=AUDIENCE,
            issuer=ISSUER,
            options={"verify_at_hash": False}
        )
    except Exception as e:
        raise ValueError(f"invalid token: {e}")

def user_from_token(token: str):
    claims = verify_token(token)
    roles = claims.get("roles") or claims.get("realm_access", {}).get("roles", [])
    return {
        "sub": claims.get("sub"),
        "preferred_username": claims.get("preferred_username"),
        "roles": roles
    }
