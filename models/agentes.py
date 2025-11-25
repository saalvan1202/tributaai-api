from database import Base,engine
from sqlalchemy import Integer,String,Column

class Agente(Base):
    __tablename__="agente"
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    nombre=Column(String(100),nullable=False)
    descripcion=Column(String,nullable=False)
    logo=Column(String(200),nullable=False)
    path=Column(String(50),nullable=False)
    estado=Column(String(1),nullable=False)
Base.metadata.create_all(engine)