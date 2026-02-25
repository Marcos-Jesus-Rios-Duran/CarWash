"""User router module."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from common.config.database import get_db
from features.user.controller import UserController
from features.user.schemas import UserCreate, UserResponse

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