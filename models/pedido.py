from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.conexion import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, default=datetime.now)
    total = Column(Float, nullable=False)
    cliente_nombre = Column(String, nullable=True)

    detalles = relationship("DetallePedido", back_populates="pedido", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Pedido #{self.id} - ${self.total:.2f}>"


class DetallePedido(Base):
    __tablename__ = "detalle_pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("producto.id"), nullable=False)
    nombre_producto = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)

    pedido = relationship("Pedido", back_populates="detalles")
