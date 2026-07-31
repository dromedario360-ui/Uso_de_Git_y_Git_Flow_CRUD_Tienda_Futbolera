from sqlalchemy import Column, Integer, String, Float
from database.conexion import Base

class Producto(Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    talla = Column(String, nullable=True)
    stock = Column(Integer, nullable=False,default=0)
    imagen = Column(String, nullable=True)
    categoria = Column(String, nullable=False)
    precio = Column(Float, nullable=False)


    def __repr__(self):
        return f"<Producto: {self.nombre} ({self.categoria})>"



