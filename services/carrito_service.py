from typing import List, Dict
from models.producto import Producto
from services.producto_service import ProductoService
from repositories.pedido_repository import IPedidoRepository
from repositories.pago_gateway import IPagoGateway


class ItemCarrito:
    def __init__(self, producto: Producto, cantidad: int):
        self.producto = producto
        self.cantidad = cantidad

    @property
    def subtotal(self) -> float:
        return self.producto.precio * self.cantidad


class CarritoService:
    def __init__(self, producto_service: ProductoService, pedido_repositorio: IPedidoRepository, pago_gateway: IPagoGateway):
        self.producto_service = producto_service
        self.pedido_repositorio = pedido_repositorio
        self.pago_gateway = pago_gateway
        self.items: Dict[int, ItemCarrito] = {}

    def agregar_item(self, producto: Producto, cantidad: int = 1):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        actual = self.items[producto.id].cantidad if producto.id in self.items else 0
        if actual + cantidad > producto.stock:
            raise ValueError(f"Solo hay {producto.stock} unidades disponibles de {producto.nombre}")

        if producto.id in self.items:
            self.items[producto.id].cantidad += cantidad
        else:
            self.items[producto.id] = ItemCarrito(producto, cantidad)

    def quitar_item(self, producto_id: int):
        self.items.pop(producto_id, None)

    def vaciar(self):
        self.items = {}

    def obtener_items(self) -> List[ItemCarrito]:
        return list(self.items.values())

    def calcular_total(self) -> float:
        return sum(item.subtotal for item in self.items.values())

    def confirmar_compra(self, cliente_nombre: str = None):
        if not self.items:
            raise ValueError("El carrito esta vacio")

        total = self.calcular_total()

        if not self.pago_gateway.procesar_pago(total):
            raise ValueError("El pago fue rechazado")

        detalles = [{
            "producto_id": item.producto.id,
            "nombre_producto": item.producto.nombre,
            "cantidad": item.cantidad,
            "precio_unitario": item.producto.precio,
        } for item in self.items.values()]

        for item in self.items.values():
            self.producto_service.vender_producto(item.producto.id, item.cantidad)

        pedido = self.pedido_repositorio.crear_pedido(total=total, detalles=detalles, cliente_nombre=cliente_nombre)
        self.vaciar()
        return pedido
