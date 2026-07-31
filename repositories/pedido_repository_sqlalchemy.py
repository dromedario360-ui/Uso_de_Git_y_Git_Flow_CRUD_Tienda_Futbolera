from typing import List, Dict, Optional
from database.conexion import SessionLocal
from models.pedido import Pedido, DetallePedido
from repositories.pedido_repository import IPedidoRepository


class PedidoRepositorySQLAlchemy(IPedidoRepository):
    def crear_pedido(self, total: float, detalles: List[Dict], cliente_nombre: Optional[str] = None) -> Pedido:
        sesion = SessionLocal()
        try:
            pedido = Pedido(total=total, cliente_nombre=cliente_nombre)
            sesion.add(pedido)
            sesion.flush()

            for d in detalles:
                sesion.add(DetallePedido(
                    pedido_id=pedido.id,
                    producto_id=d["producto_id"],
                    nombre_producto=d["nombre_producto"],
                    cantidad=d["cantidad"],
                    precio_unitario=d["precio_unitario"],
                ))

            sesion.commit()
            sesion.refresh(pedido)
            return pedido
        finally:
            sesion.close()

    def obtener_todos(self) -> List[Pedido]:
        sesion = SessionLocal()
        try:
            return sesion.query(Pedido).all()
        finally:
            sesion.close()
