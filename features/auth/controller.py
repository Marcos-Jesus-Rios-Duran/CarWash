"""
Auth Controller Module.
Handles authentication business logic, token generation, and session management.
"""

from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from features.user.dao import UserDAO
from features.auth.dao import AuthDAO
from features.auth.schemas import LoginRequest, TokenResponse
from common.security.hash import verify_password
from common.security.jwt_manager import create_access_token
from common.config.config import get_settings

settings = get_settings()


class AuthController:
    """
    Controller to manage user authentication and session tokens.
    """

    def __init__(self, db: AsyncSession):
        """
        Initializes the controller with necessary DAOs.
        """
        self.user_dao = UserDAO(db)
        self.auth_dao = AuthDAO(db)

    async def login_user(self, credentials: LoginRequest) -> TokenResponse:
        """
        Authenticates a user using either a username or an email address.

        Args:
            credentials (LoginRequest): User login data (username/email and password).

        Returns:
            TokenResponse: A dictionary containing access and refresh tokens.

        Raises:
            HTTPException: If authentication fails or the account is inactive.
        """
        # Generic error message to prevent user enumeration security risks
        error_msg = "Invalid username or password"

        # 1. Dual login logic: Detect if the input is an email or a username
        # Based on GitHub-style login logic
        if "@" in credentials.username:
            user = await self.user_dao.get_by_email(credentials.username)
        else:
            user = await self.user_dao.get_by_username(credentials.username)

        # 2. Validate user existence and password hash
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_msg
            )

        if not verify_password(credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_msg
            )

        # 3. Check account status
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive. Please contact the administrator."
            )

        # 4. Create Access Token (Short-lived)
        access_payload = {
            "sub": str(user.id),
            "role_id": user.role_id,
            "username": user.username,
            "type": "access"
        }
        access_token = create_access_token(access_payload)

        # 5. Create Refresh Token (Long-lived for 'Remember Me' functionality)
        # Default expiration is set to 7 days
        refresh_expire = datetime.now(timezone.utc) + timedelta(days=7)
        refresh_payload = {
            "sub": str(user.id),
            "type": "refresh"
        }
        refresh_token = create_access_token(refresh_payload)

        # 6. Persist the refresh token in the database for session tracking
        await self.auth_dao.save_token(user.id, refresh_token, refresh_expire)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )