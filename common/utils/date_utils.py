"""
carwash_backend/common/utils/date_utils.py
Utilities for handling dates and timezones (Mexico City).
"""
from datetime import datetime
import pytz

# Definimos la zona horaria de México
MX_TIMEZONE = pytz.timezone('America/Mexico_City')

def get_now_mx():
    """
    Retorna la fecha y hora actual en la zona horaria de México.
    Útil para los campos 'default' en los modelos.
    """
    return datetime.now(MX_TIMEZONE)

def format_date_mx(dt: datetime) -> str:
    """
    Toma un objeto datetime y lo convierte a string en formato legible MX.
    Ejemplo salida: '07/02/2026 10:30 AM'
    """
    if not dt:
        return ""
    # Si la fecha viene sin zona horaria (naive), asumimos UTC y convertimos a MX
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt).astimezone(MX_TIMEZONE)
    else:
        dt = dt.astimezone(MX_TIMEZONE)

    return dt.strftime('%d/%m/%Y %I:%M %p')