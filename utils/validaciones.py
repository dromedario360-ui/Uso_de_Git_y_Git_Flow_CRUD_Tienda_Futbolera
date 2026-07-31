import re


def validar_email(email: str) -> bool:
    """Valida que el email tenga un formato basico correcto."""
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(patron, email or ""))


def validar_password(password: str, longitud_minima: int = 6) -> bool:
    """Valida que la contrasena cumpla con la longitud minima."""
    return bool(password) and len(password) >= longitud_minima
