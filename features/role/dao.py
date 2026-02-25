"""
Role Data Access Object (DAO).
Handles database operations for the Role entity.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from features.role.models import Role


class RoleDAO:
    """Manages database access for roles."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_name(self, name: str) -> Role | None:
        """
        Retrieves a role record by its unique name.
        """
        query = select(Role).where(Role.name == name)
        result = await self.session.execute(query)
        return result.scalars().first()
