"""User router module."""

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from common.security.oauth2 import get_current_user
from common.config.database import get_db
from features.user.controller import UserController
from features.user.schemas import UserCreate, UserResponse, UserUpdate
from features.user.models import User
from common.security.permissions import RoleChecker
router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """
    Entry point for registering new users.

    Args:
        user (UserCreate): The schema containing the new user data.
        db (AsyncSession): The asynchronous database session dependency.

    Returns:
        UserResponse: The newly created user information.
    """
    controller = UserController(db)
    return await controller.register_new_user(user)
@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Get the profile of the currently authenticated user.
    """
    return current_user

@router.get("/", response_model=list[UserResponse])
async def list_all_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["Admin"]))):
    """
    List of all users in the system. Only accessible by Admins.
    """
    controller = UserController(db)
    return await controller.get_all_users()

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    Update an existing user.
    - **Admin**: Can update ANY user.
    - **Others**: Can only update their OWN profile.
    """
    controller = UserController(db)
    return await controller.update_user(user_id, user_in, current_user)

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a user from the system.
    - **Admin**: Can delete ANY user.
    - **Others**: Can only delete their OWN profile.
    """
    controller = UserController(db)
    return await controller.delete_user(user_id, current_user)