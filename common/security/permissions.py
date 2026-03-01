"""
carwash_backend/common/security/permissions.py
Role-based access control dependencies.
"""
from typing import List
from fastapi import Depends, HTTPException, status
from features.user.models import User
from common.security.oauth2 import get_current_user
from common.utils.responses import ErrorMessages

class RoleChecker:
    """
    Dependencia para verificar si el usuario tiene el rol adecuado.
    """
    def __init__(self, allowed_roles: List[str]):
        # Recibimos la lista de roles que sí pueden pasar
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        """
        Este método hace que la clase sea "llamable" (callable) como una función.
        FastAPI inyectará el `current_user` aquí automáticamente.
        """
        # Verificamos si el nombre del rol del usuario está en la lista permitida
        if current_user.role.name not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorMessages.FORBIDDEN_ROLE
            )

        # Si pasa la validación, retornamos el usuario para que la ruta lo pueda usar
        return current_user