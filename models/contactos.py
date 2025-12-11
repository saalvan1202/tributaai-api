from sqlalchemy import Column,String,Integer
from database import Base

class Contactos(Base):
    __tablename__='contacts'
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    wa_id=Column(String(30),nullable=False)
    nombre=Column(String(200))
    estado=Column(String(1),nullable=False)