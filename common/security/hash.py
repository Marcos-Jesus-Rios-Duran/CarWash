"""
Utilities for secure password hashing.
"""
from passlib.context import CryptContext

# Configuración de Passlib para usar Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Genera un hash seguro de la contraseña."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara una contraseña plana con su hash guardado."""
    return pwd_context.verify(plain_password, hashed_password)