from sqlalchemy.orm import Session,aliased
from models.contactos import Contactos
from models.mensajes import Mensajes
from schemas.mensajes_schema import MensajesSchema
from fastapi.responses import JSONResponse
from sqlalchemy import func, and_
from web.web_socket import manager

async def save_mensaje(db:Session,data:MensajesSchema):
    contactos=db.query(Contactos).filter(Contactos.wa_id==data.wa_id).first()
    if not contactos:
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
    await manager.broadcast(data.model_dump())
    return JSONResponse(content={
        "message":"El mensaje fue enviado correctamente",
        "status":200
    })    

def get_contactos(db:Session):
    subq = db.query(
    Mensajes.id_contact,
    func.max(Mensajes.id).label("max_id")
    ).filter(Mensajes.direction=='incoming').group_by(Mensajes.id_contact).subquery()
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
            # "fecha": chat.timestamp.isoformat() if chat.timestamp else None,
            "id_contact": chat.id_contact,
            "wa_id": wa_id,
            "nombre": nombre
        })

    return JSONResponse(content=contactos)

def get_messages_chat(db:Session,id_contact:str):
    mensajes=db.query(Mensajes).filter(Mensajes.id_contact==id_contact).order_by(Mensajes.id.asc()).all()
    if not mensajes:
        return "No se encontró menajes en este chat"
    return mensajes