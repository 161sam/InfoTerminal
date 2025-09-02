import os, httpx
from jose import jwt
from cachetools import TTLCache

ISSUER = os.getenv("KEYCLOAK_ISSUER","http://localhost:8081/realms/infoterminal")
AUDIENCE = os.getenv("KEYCLOAK_AUDIENCE","search-api")  # reuse audience; adjust if you create dedicated client
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"
_cache = TTLCache(1, 300)

def _jwks():
    if "jwks" in _cache: return _cache["jwks"]
    d = httpx.get(JWKS_URL, timeout=5).json(); _cache["jwks"]=d; return d

def user_from_token(token:str):
    claims = jwt.decode(token, _jwks(), algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER)
    roles = claims.get("roles") or claims.get("realm_access",{}).get("roles",[])
    return {"sub":claims.get("sub"), "roles":roles, "username":claims.get("preferred_username")}
