from sqlalchemy import Boolean,Integer,String,Column
from database import Base,engine

#Tabla(Si la tabla ya está creada tienen que ser los mismo tipos de datos)
class Administrado(Base):
    __tablename__="administrado"
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    nombres=Column(String(100),nullable=False)
    apellido_paterno=Column(String(100),nullable=False)
    apellido_materno=Column(String(100),nullable=False)
    telefono=Column(Integer,nullable=False)
    dni=Column(Integer,nullable=False,unique=True)
    gmail=Column(String,nullable=False,unique=True)
    cod_administrado=Column(String,nullable=False)
    # estado=Column(String,nullable=False,default='A')
Base.metadata.create_all(engine)
#Puedo usar herramienta externas para hacer migraciones a la base de datos, cómo agregar campos nuevos, modificar los campos ya existentes
#Usar Alembic (herramienta de migraciones) → actualiza la BD de forma controlada.
#Base.metada.create_all(engine), sirve para solo crear lo declarado, no para modificar