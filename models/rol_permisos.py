from database import Base,engine
from sqlalchemy import Column,Integer,String

class RolPermisos(Base):
    __tablename__="rol_permisos"
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    rol_id=Column(Integer,nullable=False)
    permiso_id=Column(Integer,nullable=False)
    estado=Column(String(1),nullable=False)
Base.metadata.create_all(engine)