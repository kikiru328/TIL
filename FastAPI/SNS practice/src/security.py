from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

oauth2_scheme = HTTPBearer()

def get_access_token(
        auth_header: HTTPAuthorizationCredentials | None = Depends((oauth2_scheme))
) -> str:
    if auth_header is None:
        raise HTTPException(status_code=401, detail="Not Authorized")
    return auth_header.credentials