""""
carwash_backend/features/auth/dao.py
_data access object for auth feature_
"""
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from features.auth.models import UserToken
from features.auth.schemas import UserTokenBase

class AuthDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_token(self, user_id: int, token: str, expires_at):
        """add a new refresh token to the database."""
        new_token = UserToken(
            user_id=user_id,
            refresh_token=token,
            expires_at=expires_at
        )
        self.session.add(new_token)
        await self.session.commit()
        return new_token

    async def get_refresh_token(self, token: str) -> UserToken | None:
        """Search for a refresh token in the database."""
        query = select(UserToken).where(UserToken.refresh_token == token)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def revoke_token(self, token: str):
        """Logout by deleting the refresh token from the database."""
        query = delete(UserToken).where(UserToken.refresh_token == token)
        await self.session.execute(query)
        await self.session.commit()