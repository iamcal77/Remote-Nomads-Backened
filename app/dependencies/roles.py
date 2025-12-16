from fastapi import Depends, HTTPException
from app.dependencies.auth import get_current_user

def require_role(*roles):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_checker
