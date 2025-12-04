from models.chats import Chat
from sqlalchemy.orm import Session,aliased
from sqlalchemy import distinct
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import random
from sqlalchemy import func, and_

def get_session_chat(db:Session):
    #result=db.query(distinct(Chat.session_id)).all()
    # ult_message = db.query(Chat).order_by(Chat.id.desc()).first()
    # if ult_message:
    #     ult_message=ult_message.message
    subq = db.query(
    Chat.session_id,
    func.max(Chat.id).label("max_id")
    ).group_by(Chat.session_id).subquery()
    ChatAlias = aliased(Chat)
    ult_messages = db.query(ChatAlias).join(
    subq,
    and_(
        ChatAlias.session_id == subq.c.session_id,
        ChatAlias.id == subq.c.max_id
    )
    ).all()
    for msg in ult_messages:
        msg.avatar = random.randint(0, 4)
    #sessions = [{"id":row[0],"avatar": random.randint(0, 4),"ult_message":ult_messages}for row in result]
    return ult_messages
def get_messages_chat(db:Session,id_session:str):
    session=db.query(Chat).filter(Chat.session_id==id_session).order_by(Chat.id.asc()).all()
    if not session:
        return "No se encontró menajes en este chat"
    return session

# def create_message_chat()