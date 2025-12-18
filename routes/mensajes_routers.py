from database import get_db
from schemas.mensajes_schema import MensajesSchema
from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter
from fastapi.responses import JSONResponse
from services.contactos_service import save_mensaje,get_messages_chat,send_mensaje
from web.web_socket import manager
import os
from cryptography.fernet import Fernet
import json

router=APIRouter(prefix="/api/v1/mensajes",tags=['Mensajes'])

fernet=Fernet(os.getenv("HI_KEY"))
@router.post("/")
async def save(data:MensajesSchema,db:Session=Depends(get_db)):
    mensaje=save_mensaje(db,data)
    json_data=json.dumps(data.model_dump()).encode()
    encriptar=fernet.encrypt(json_data).decode()
    await manager.broadcast({
        "payload":encriptar
    })
    return JSONResponse(content={
        "message":"El mensaje fue enviado correctamente",
        "status":200
    }) 

@router.get("/")
def llamar(wa_id:str,db:Session=Depends(get_db)):
    return get_messages_chat(db,wa_id)

@router.post("/send")
def send(data:MensajesSchema,db:Session=Depends(get_db)):
    return send_mensaje(db,data)