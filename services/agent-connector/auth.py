from fastapi import Header, HTTPException, Depends
from typing import Dict, List

def require_user(authorization: str = Header("")) -> Dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "missing bearer token")
    token = authorization.split(" ", 1)[1]
    roles: List[str] = []
    if token == "admin":
        roles.append("admin")
    return {"sub": token, "roles": roles}

def require_admin(user: Dict = Depends(require_user)) -> Dict:
    if "admin" not in user.get("roles", []):
        raise HTTPException(403, "admin only")
    return user
