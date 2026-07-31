from repositories.autenticacion_repository import IAutenticacionRepository


class AutenticacionRepositoryEstatica(IAutenticacionRepository):
    """Implementacion simple: valida contra un usuario y contrasena fijos.
    Se puede reemplazar despues por una tabla 'usuarios' en la base de datos
    sin tocar el resto del sistema (Inversion de Dependencias)."""

    def __init__(self, usuario_valido: str, password_valido: str):
        self.usuario_valido = usuario_valido
        self.password_valido = password_valido

    def validar_credenciales(self, usuario: str, password: str) -> bool:
        return usuario.strip() == self.usuario_valido and password.strip() == self.password_valido
