from abc import ABC, abstractmethod


class IAutenticacionRepository(ABC):
    """Contrato del componente Gestion de Usuarios  Cualquier fuente de
    autenticacion archivo base de datos y la api externa debe implementar esto."""

    @abstractmethod
    def validar_credenciales(self, usuario: str, password: str) -> bool:
        pass
