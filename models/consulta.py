# from sqlalchemy.orm import I
from database import Base,engine
from sqlalchemy import Integer,String,Boolean,Column,TIMESTAMP

class Consulta(Base):
    __tablename__="consultas"
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    id_administrado=Column(Integer,nullable=False)
    descripcion=Column(String(200),nullable=False)
    codigo=Column(Integer,nullable=False)
    dni=Column(Integer,nullable=False)
    telefono=Column(Integer,nullable=False)
    verificado=Column(String(1),nullable=False)
    fecha=Column(TIMESTAMP,nullable=False)
#Para crear al tabla al ejecutar 
Base.metadata.create_all(engine)
     
     