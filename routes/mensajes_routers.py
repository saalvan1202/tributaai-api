from database import get_db
from schemas.mensajes_schema import MensajesSchema
from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter
from fastapi.responses import JSONResponse
from services.contactos_service import save_mensaje,get_messages_chat
from web.web_socket import manager


router=APIRouter(prefix="/api/v1/mensajes",tags=['Mensajes'])

@router.post("/")
async def save(data:MensajesSchema,db:Session=Depends(get_db)):
    mensaje=save_mensaje(db,data)
    await manager.broadcast(data.model_dump())
    JSONResponse(content={
        "message":"El mensaje fue enviado correctamente",
        "status":200
    }) 

@router.get("/")
def llamar(id_contact:str,db:Session=Depends(get_db)):
    return get_messages_chat(db,id_contact)