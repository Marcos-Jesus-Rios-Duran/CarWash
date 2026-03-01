"""
User Controller Module.
Orchestrates business logic for user registration and role assignment.
"""
import logging
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from common.utils.responses import ErrorMessages, SuccessMessages
from features.user.dao import UserDAO
from features.role.dao import RoleDAO
from features.user.models import User
from features.user.schemas import UserCreate, UserUpdate

# Configure professional logging
logger = logging.getLogger(__name__)


class UserController:
    """Business logic layer for managing users."""

    def __init__(self, db: AsyncSession):
        self.user_dao = UserDAO(db)
        self.role_dao = RoleDAO(db)

    async def register_new_user(self, user_in: UserCreate, role_name: str = "Customer"):
        """
        Validates business rules and registers a new user with a specific role.

        Args:
            user_in (UserCreate): The user data from the request.
            role_name (str): The name of the role to assign (e.g., 'Admin', 'Washer').
        """
        # 1. Check if username already exists
        if await self.user_dao.get_by_username(user_in.username):
            logger.warning(f"Registration failed: Username '{user_in.username}' already taken.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The username '{user_in.username}' is already in use."
            )

        # 2. Check if email already exists
        if user_in.email and await self.user_dao.get_by_email(user_in.email):
            logger.warning(f"Registration failed: Email '{user_in.email}' already exists.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The email '{user_in.email}' is already registered."
            )

    # 3. Resolve Role Name usando el valor que viene en el JSON (user_in.role_name)
        role = await self.role_dao.get_by_name(user_in.role_name)
        if not role:
            logger.error(f"Role '{user_in.role_name}' not found.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Configuration error: Role '{user_in.role_name}' does not exist."
            )

        # 4. Assign the resolved role_id
        user_in.role_id = role.id

        # 5. Persist user data via DAO
        logger.info(f"Creating new user: {user_in.username} with role {user_in.role_name}")
        return await self.user_dao.create(user_in)

    async def get_all_users(self, include_inactive: bool = False):
        """
        Business logic to retrieve all users.
        """
        return await self.user_dao.get_all(include_inactive)

    async def update_user(self, user_id: int, user_in: UserUpdate, current_user: User):
        """
        Apply business rules to update a user's information.
        """
        target_user = await self.user_dao.get_by_id(user_id)
        if not target_user:
            raise HTTPException(status_code=404, detail=ErrorMessages.RESOURCE_NOT_FOUND)

        # the golden rule: Only Admins can update any user, but users can update their own profile
        if current_user.role.name != "Admin" and current_user.id != user_id:
            raise HTTPException(status_code=403, detail=ErrorMessages.FORBIDDEN_ROLE)

        return await self.user_dao.update(target_user, user_in)

    async def delete_user(self, user_id: int, current_user: User):
        """
        Apply business rules to delete a user.
        """
        target_user = await self.user_dao.get_by_id(user_id)
        if not target_user:
            raise HTTPException(status_code=404, detail=ErrorMessages.RESOURCE_NOT_FOUND)

        # the golden rule: Only Admins can delete any user, but users can delete their own profile
        if current_user.role.name != "Admin" and current_user.id != user_id:
            raise HTTPException(status_code=403, detail=ErrorMessages.FORBIDDEN_ROLE)

        await self.user_dao.delete(target_user)
        return {"detail": SuccessMessages.DELETED}