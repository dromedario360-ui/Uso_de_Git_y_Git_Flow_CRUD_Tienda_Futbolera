from typing import List
from models.producto import Producto
from repositories.producto_repository import IProductoRepository

class ProductoService:
    def __init__(self, repositorio: IProductoRepository):
        self.repositorio = repositorio

    def listar_productos(self) -> List[Producto]:
        return self.repositorio.obtener_todos()

    def listar_por_categoria(self, categoria: str) -> List[Producto]:
        return self.repositorio.obtener_por_categoria(categoria)

    def buscar_por_nombre(self, texto: str) -> List[Producto]:
        texto = (texto or "").strip().lower()
        return [p for p in self.repositorio.obtener_todos() if texto in p.nombre.lower()]

    def crear_producto(self, nombre, categoria, descripcion, talla, precio, stock, imagen) -> Producto:
        if not nombre or not categoria:
            raise ValueError("El nombre y la categoria son obligatorios")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")

        nuevo = Producto(
            nombre=nombre, categoria=categoria, descripcion=descripcion,
            talla=talla, precio=precio, stock=stock, imagen=imagen
        )
        return self.repositorio.agregar(nuevo)

    def actualizar_producto(self, id_producto, nombre, categoria, descripcion, talla, precio, stock) -> Producto:
        if not nombre or not categoria:
            raise ValueError("El nombre y la categoria son obligatorios")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")

        producto = self.repositorio.obtener_por_id(id_producto)
        if producto is None:
            raise ValueError("El producto no existe")

        producto.nombre = nombre
        producto.categoria = categoria
        producto.descripcion = descripcion
        producto.talla = talla
        producto.precio = precio
        producto.stock = stock

        return self.repositorio.actualizar(producto)

    def vender_producto(self, id_producto: int, cantidad: int = 1) -> Producto:
        producto = self.repositorio.obtener_por_id(id_producto)
        if producto is None:
            raise ValueError("El producto no existe")
        if producto.stock < cantidad:
            raise ValueError("No hay suficiente stock")
        producto.stock -= cantidad
        return self.repositorio.actualizar(producto)

    def eliminar_producto(self, id_producto: int) -> bool:
        return self.repositorio.eliminar(id_producto)
