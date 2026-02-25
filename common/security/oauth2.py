"""
Security dependencies for route protection.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from common.security.jwt_manager import decode_token
from common.config.database import get_db
from features.user.dao import UserDAO

# Este objeto activa el botón "Authorize" en Swagger
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_db)
):
    """
    Validates the token and returns the current authenticated user.
    """
    token = credentials.credentials
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extraemos el ID del usuario del token (sub)
    user_id = int(payload.get("sub"))
    user_dao = UserDAO(db)
    user = await user_dao.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user