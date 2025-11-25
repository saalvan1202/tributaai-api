from database import Base,engine
from sqlalchemy import String,Column,Integer

class Modulos(Base):
    __tablename__="modulos"
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    nombre=Column(String(100),nullable=False)
    is_padre=Column(String(1),nullable=False)
    link=Column(String,nullable=False)
    icono=Column(String(50),nullable=False)
    estado=Column(String(1),nullable=False)
Base.metadata.create_all(engine)