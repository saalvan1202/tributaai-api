from fastapi import Depends,HTTPException,APIRouter
router=APIRouter(prefix="/chat",tags=["Chat"])
from sqlalchemy.orm import Session
from database import get_db
from services.chats_service import get_session_chat,get_messages_chat

router=APIRouter(prefix="/api/v1/chat",tags=["Chat"])

@router.get("/session-chat")
def session_chat(db:Session=Depends(get_db)):
    return get_session_chat(db)
@router.get("/messages-chat")
def messages_chat(id_session:str,db:Session=Depends(get_db)):
    return get_messages_chat(db,id_session)