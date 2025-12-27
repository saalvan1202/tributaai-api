from database import Base,engine
from sqlalchemy import String,Integer,Column

class Usuarios(Base):
    __tablename__='usuarios'
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    nombre=Column(String(100),nullable=True)
    correo=Column(String(150),nullable=True)
    empresa_id=Column(Integer,nullable=True)
    rol_id=Column(Integer,nullable=True)
    estado=Column(String(1),nullable=True)
    usuario=Column(String(100),nullable=False)
    password=Column(String,nullable=False)
    activo=Column(String(1),nullable=False)
    apellidos=Column(String(100),nullable=False)
    telefono=Column(String(20),nullable=False)
    #Para crear al tabla al ejecutar 
Base.metadata.create_all(engine)