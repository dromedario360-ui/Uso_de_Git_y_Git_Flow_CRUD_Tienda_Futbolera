from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from models.pedido import Pedido


class IPedidoRepository(ABC):
    @abstractmethod
    def crear_pedido(self, total: float, detalles: List[Dict], cliente_nombre: Optional[str] = None) -> Pedido:
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Pedido]:
        pass
