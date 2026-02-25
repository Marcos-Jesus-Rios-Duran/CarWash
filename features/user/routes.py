"""User router module."""

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from common.security.oauth2 import get_current_user
from common.config.database import get_db
from features.user.controller import UserController
from features.user.schemas import UserCreate, UserResponse
from features.user.models import User

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
    Retorna el perfil del usuario autenticado.
    Cualquier rol (Customer, Washer, etc.) puede entrar aquí.
    """
    return current_user

@router.get("/", response_model=list[UserResponse])
async def list_all_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista todos los usuarios.
    RESTRICCIÓN: Solo el rol 'Admin' tiene permiso.
    """
    # Verificamos el rol del usuario que hace la petición
    if current_user.role.name != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos suficientes para realizar esta acción."
        )

    controller = UserController(db)
    return await controller.get_all_users()