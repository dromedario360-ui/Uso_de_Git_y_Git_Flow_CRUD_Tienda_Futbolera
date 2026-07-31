from typing import List, Optional
from database.conexion import SessionLocal
from models.producto import Producto
from repositories.producto_repository import IProductoRepository


class ProductoRepositorySQLAlchemy(IProductoRepository):
    def obtener_todos(self) -> List[Producto]:
        sesion = SessionLocal()
        try:
            return sesion.query(Producto).all()
        finally:
            sesion.close()

    def obtener_por_categoria(self, categoria: str) -> List[Producto]:
        sesion = SessionLocal()
        try:
            return sesion.query(Producto).filter(Producto.categoria == categoria).all()
        finally:
            sesion.close()

    def obtener_por_id(self, id_producto: int) -> Optional[Producto]:
        sesion = SessionLocal()
        try:
            return sesion.query(Producto).filter(Producto.id == id_producto).first()
        finally:
            sesion.close()

    def agregar(self, producto: Producto) -> Producto:
        sesion = SessionLocal()
        try:
            sesion.add(producto)
            sesion.commit()
            sesion.refresh(producto)
            return producto
        finally:
            sesion.close()

    def actualizar(self, producto: Producto) -> Producto:
        sesion = SessionLocal()
        try:
            sesion.merge(producto)
            sesion.commit()
            return producto
        finally:
            sesion.close()

    def eliminar(self, id_producto: int) -> bool:
        sesion = SessionLocal()
        try:
            producto = sesion.query(Producto).filter(Producto.id == id_producto).first()
            if producto:
                sesion.delete(producto)
                sesion.commit()
                return True
            return False
        finally:
            sesion.close()