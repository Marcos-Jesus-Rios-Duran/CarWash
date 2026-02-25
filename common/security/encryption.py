"""
Utilities for reversible encryption (Symmetric).
Used for PII like phone numbers or addresses.
"""
from cryptography.fernet import Fernet
from common.config.config import get_settings

settings = get_settings()
# Necesitarás una ENCRYPTION_KEY en tu .env
fernet = Fernet(settings.SECRET_KEY.encode()[:32].ljust(32, b'=')) # Ajuste simple de llave

def encrypt_data(data: str) -> str:
    """Encripta un texto para que sea ilegible en la DB."""
    if not data: return data
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    """Desencripta los datos para mostrarlos en el frontend."""
    if not token: return token
    return fernet.decrypt(token.encode()).decode()