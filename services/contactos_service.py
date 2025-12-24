from sqlalchemy.orm import Session,aliased
from models.contactos import Contactos
from models.mensajes import Mensajes
from schemas.mensajes_schema import MensajesSchema
from fastapi.responses import JSONResponse
from sqlalchemy import func, and_
import requests
from dotenv import load_dotenv
import os
load_dotenv()

def save_mensaje(db:Session,data:MensajesSchema):
    contactos=db.query(Contactos).filter(Contactos.wa_id==data.wa_id).first()
    if not contactos:
        print("no hay contacto")
        contactos=Contactos(
            wa_id=data.wa_id,
            nombre=data.nombre,
            estado='A'
        )
        db.add(contactos)
        db.commit()
        db.refresh(contactos)
        
    mensaje=Mensajes(
        id_contact=contactos.id,
        id_usuario=data.id_usuario,
        direction=data.direction,
        waba_message_id=data.waba_message_id,
        message_type=data.message_type,
        text_content=data.text_content,
        raw_json=data.raw_json,
        timestamp=data.timestamp,
        estado='A'
    )
    db.add(mensaje)
    db.commit()
    db.refresh(mensaje)
    return mensaje   

def get_contactos(db:Session):
    subq = db.query(
    Mensajes.id_contact,
    func.max(Mensajes.id).label("max_id")
    ).group_by(Mensajes.id_contact).subquery()
    ChatAlias = aliased(Mensajes)
    ult_messages = db.query(ChatAlias,Contactos.wa_id,Contactos.nombre).join(
    subq,
    and_(
        ChatAlias.id_contact == subq.c.id_contact,
        ChatAlias.id == subq.c.max_id
    )
    ).join(
        Contactos,Contactos.id==ChatAlias.id_contact).filter(Contactos.estado=='A').all()
    #sessions = [{"id":row[0],"avatar": random.randint(0, 4),"ult_message":ult_messages}for row in result]
    if not ult_messages:
        return JSONResponse(content={
            "message":"No se encontraron contactos.",
            "status":200
        })
    contactos = []
    for chat, wa_id, nombre in ult_messages:
        contactos.append({
            "id": chat.id,
            "mensaje": chat.text_content,
            "direction":chat.direction,
            # "fecha": chat.timestamp.isoformat() if chat.timestamp else None,
            "id_contact": chat.id_contact,
            "wa_id": wa_id,
            "nombre": nombre
        })

    return JSONResponse(content=contactos)

def get_messages_chat(db:Session,wa_id:str):
    mensajes=db.query(Mensajes,Contactos.wa_id
                      ).join(Contactos,Contactos.id==Mensajes.id_contact
                             ).filter(Contactos.wa_id==wa_id
                                      ).order_by(Mensajes.id.asc()
                                                 ).all()
    if not mensajes:
        return "No se encontró menajes en este chat"
    lista = []
    for m,wa in mensajes:
        lista.append({
            "id_contact": m.id_contact,
            "direction": m.direction,
            "message_type": m.message_type,
            "text_content": m.text_content,
            "timestamp": m.timestamp,
            "raw_json": m.raw_json,
            "waba_message_id": m.waba_message_id,
        })

    return lista

def send_mensaje(db,data:MensajesSchema):
    version=os.getenv("VERSION_WPP_API")
    phone_number_id=os.getenv("ID_PHONE_NUMER_WPP")
    token=os.getenv("TOKEN_WPP")
    url = f"https://graph.facebook.com/{version}/{phone_number_id}/messages"

    body = {
        "messaging_product": "whatsapp",    
        "recipient_type": "individual",
        "to": f"{data.wa_id}",
        "type": "text",
        "text": {
            "preview_url": False,
            "body": f"{data.text_content}"
        }
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response=requests.post(url, json=body, headers=headers)

    if not response.ok:
        return JSONResponse(content={"error":response.text},status_code=500)
    obj = response.json()
    message_id = obj["messages"][0]["id"]
    data.waba_message_id=message_id
    data.raw_json=obj
    mensaje=save_mensaje(db,data)
    return {
        "status": "sent",
        "id": mensaje.id,
        "waba_message_id": data.waba_message_id
    }

    