import os
from fastapi import HTTPException, Header

ADMIN_KEY = os.getenv("ADMIN_KEY")

def require_admin(admin_key: str = Header(None)):
    if admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
