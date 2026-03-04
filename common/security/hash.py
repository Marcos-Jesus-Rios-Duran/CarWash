"""
Utilities for secure password hashing using pure bcrypt.
"""
import bcrypt

def get_password_hash(password: str) -> str:
    """Genera un hash seguro de la contraseña."""
    # bcrypt requiere bytes, así que codificamos el string
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Lo devolvemos como string para guardarlo en la Base de Datos
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara una contraseña plana con su hash guardado."""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except ValueError:
        # Atrapa errores si el hash en la BD está corrupto o no es formato bcrypt
        return False