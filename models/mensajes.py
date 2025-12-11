from database import Base
from sqlalchemy import Integer,String,Column,JSON

class Mensajes(Base):
    __tablename__="messages"
    id=Column(Integer,primary_key=True,autoincrement=True,index=True,nullable=False)
    id_contact=Column(Integer,nullable=False)
    id_usuario=Column(Integer,nullable=False)
    direction=Column(String(10),nullable=False)
    waba_message_id=Column(String(200),nullable=False)
    message_type=Column(String(20),nullable=False)
    text_content=Column(String,nullable=False)
    raw_json=Column(JSON,nullable=False)
    timestamp=Column(Integer,nullable=False)
    estado=Column(String(1),nullable=False)