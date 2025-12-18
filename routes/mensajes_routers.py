from database import get_db
from schemas.mensajes_schema import MensajesSchema
from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter
from fastapi.responses import JSONResponse
from services.contactos_service import save_mensaje,get_messages_chat,send_mensaje
from web.web_socket import manager
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
import base64

router=APIRouter(prefix="/api/v1/mensajes",tags=['Mensajes'])

SECRET_KEY = os.getenv("HI_KEY").encode()[:32]
IV = b'1234567890123456' 
@router.post("/")
async def save(data:MensajesSchema,db:Session=Depends(get_db)):
    mensaje=save_mensaje(db,data)
    raw = json.dumps(data.model_dump()).encode()
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    encrypted = cipher.encrypt(pad(raw, AES.block_size))
    await manager.broadcast({
        "payload":base64.b64encode(encrypted).decode()
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