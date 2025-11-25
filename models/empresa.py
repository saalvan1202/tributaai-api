from database import Base,engine
from sqlalchemy import Integer,String,Boolean,Column

class Empresa(Base):
    __tablename__="empresa"
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    nombre=Column(String(150),nullable=False)
    ruc=Column(String(11),nullable=False)
    direccion=Column(String(150),nullable=False)
    estado=Column(String(1),nullable=False)
Base.metadata.create_all(engine)