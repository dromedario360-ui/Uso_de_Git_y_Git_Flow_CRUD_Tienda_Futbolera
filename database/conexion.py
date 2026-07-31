from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# plantilla de la que heredan todas las tablas

Base = declarative_base()


engine = create_engine("sqlite:///tienda2.db", echo=True)
SessionLocal = sessionmaker(bind=engine)

def crear_base_datos():
    from models.producto import Producto
    Base.metadata.create_all(engine)





