from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm # Opcional si quieres usar el form de Swagger

from common.config.database import get_db
from features.auth.schemas import LoginRequest, TokenResponse
from features.auth.controller import AuthController

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Init session for user login.
    """
    controller = AuthController(db)
    return await controller.login_user(credentials)