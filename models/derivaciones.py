from database import Base,engine
from sqlalchemy import String, Integer,DateTime,Column
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Derivaciones(Base):
    __tablename__='derivaciones'
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    id_usuario=Column(Integer,nullable=False)
    id_contacto=Column(Integer,nullable=False)
    motivo_derivacion=Column(String,nullable=False)
    fecha_derivacion=Column(DateTime,nullable=False)
    fecha_atencion=Column(DateTime,nullable=False)
    observaciones=Column(String,nullable=True)
    estado_derivacion=Column(String(50),nullable=False)
    resuelto=Column(String(1),nullable=False)
    estado=Column(String(1),nullable=False)
    uuid=Column(UUID(as_uuid=True),default=uuid.uuid4)
Base.metadata.create_all(engine)
