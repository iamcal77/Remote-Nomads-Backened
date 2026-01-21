from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False
)

http_bearer = HTTPBearer(auto_error=False)

def get_current_user(
    oauth_token: str | None = Depends(oauth2_scheme),
    bearer: HTTPAuthorizationCredentials | None = Depends(http_bearer),
    query_token: str | None = Query(None, alias="token")
) -> dict:
    token = oauth_token

    if bearer:
        token = bearer.credentials
    elif query_token:
        token = query_token

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
