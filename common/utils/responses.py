"""
carwash_backend/common/utils/responses.py
Standardized response messages for the application.
"""

class ErrorMessages:
    """error messages for authentication and authorization."""
    UNAUTHORIZED = "Credenciales inválidas o sesión expirada."
    FORBIDDEN_ROLE = "No tienes los permisos suficientes para realizar esta acción."
    USER_NOT_FOUND = "Usuario no encontrado en el sistema."
    INACTIVE_ACCOUNT = "La cuenta está inactiva. Contacta al administrador."
    RESOURCE_NOT_FOUND = "El recurso solicitado no existe."

class SuccessMessages:
    """exito messages for CRUD operations."""
    CREATED = "Registro creado exitosamente."
    UPDATED = "Registro actualizado exitosamente."
    DELETED = "Registro eliminado exitosamente."