from database import Base,engine
from sqlalchemy import Integer,String,Column

class Roles(Base):
    __tablename__="roles"
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    nombre=Column(String(100),nullable=False)
    descripcion=Column(String,nullable=False)
    estado=Column(String(1),nullable=False)
Base.metadata.create_all(engine)