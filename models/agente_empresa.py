from database import Base,engine
from sqlalchemy import Column,String,Integer

class AgenteEmpresa(Base):
    __tablename__="agente_empresa"
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    agente_id=Column(Integer,nullable=True)
    empresa_id=Column(Integer,nullable=True)
    estado_agente=Column(String(1),nullable=True)
    instancia=Column(String(100),nullable=True)
    telefono=Column(String(100),nullable=True)
    estado=Column(String(1),nullable=True)
Base.metadata.create_all(engine)