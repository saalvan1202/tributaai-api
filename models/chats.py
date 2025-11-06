# from sqlalchemy.orm import I
from database import Base,engine
from sqlalchemy import Integer,String,Date,Boolean,Column

class Chat(Base):
    __tablename__="n8n_chat_histories"
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    session_id=Column(String,nullable=False)
    message=Column(String,nullable=False)  
#Para crear al tabla al ejecutar 
Base.metadata.create_all(engine)