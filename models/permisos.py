from sqlalchemy import Column,String,Integer
from database import Base,engine

class Permisos(Base):
    __tablename__="permisos"
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    id_modulo=Column(Integer,nullable=False)
    nombre=Column(String(100),nullable=False)
    accion=Column(String(50),nullable=False)
    estado=Column(String(1),nullable=False)
Base.metadata.create_all(engine)