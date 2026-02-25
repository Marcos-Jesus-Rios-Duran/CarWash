"""
Utilities for reversible encryption (Symmetric).
Used for PII like phone numbers or addresses.
"""
import logging
from cryptography.fernet import Fernet
from common.config.config import get_settings

# Configure logging for security events
logger = logging.getLogger(__name__)
settings = get_settings()

try:
    # We use the dedicated ENCRYPTION_KEY from environment variables
    fernet = Fernet(settings.ENCRYPTION_KEY.encode())
except Exception as e:
    logger.error(f"Failed to initialize Fernet: {str(e)}")
    raise RuntimeError("Invalid ENCRYPTION_KEY format. Must be 32 url-safe base64-encoded bytes.")


def encrypt_data(data: str) -> str:
    """
    Encrypts a string to make it unreadable in the database.
    """
    if not data:
        return data
    return fernet.encrypt(data.encode()).decode()


def decrypt_data(token: str) -> str:
    """
    Decrypts tokens to show raw data in the frontend.
    """
    if not token:
        return token
    try:
        return fernet.decrypt(token.encode()).decode()
    except Exception as e:
        logger.warning(f"Decryption failed: {str(e)}")
        return "[ENCRYPTED DATA]"