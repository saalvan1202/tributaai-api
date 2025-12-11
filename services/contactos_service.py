from sqlalchemy.orm import Session
from models.contactos import Contactos
from models.mensajes import Mensajes
from schemas.mensajes_schema import MensajesSchema
from fastapi.responses import JSONResponse

def save_mensaje(db:Session,data:MensajesSchema):
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
    
    return JSONResponse(content={
        "message":"El mensaje fue enviado correctamente",
        "status":200
    })    
    