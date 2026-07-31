from abc import ABC, abstractmethod
from typing import List, Optional
from models.producto import Producto

class IProductoRepository(ABC):
    @abstractmethod
    def obtener_todos(self) -> List[Producto]:
        pass

    @abstractmethod
    def obtener_por_categoria(self, categoria: str) -> List[Producto]:
        pass

    @abstractmethod
    def obtener_por_id(self, id_producto: int) -> Optional[Producto]:
        pass

    @abstractmethod
    def agregar(self, producto: Producto) -> Producto:
        pass

    @abstractmethod
    def actualizar(self, producto: Producto) -> Producto:
        pass

    @abstractmethod
    def eliminar(self, id_producto: int) -> bool:
        pass

    