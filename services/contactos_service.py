from sqlalchemy.orm import Session
from models.contactos import Contactos
from models.mensajes import Mensajes
from schemas.mensajes_schema import MensajesSchema

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
    return "elegante"    
    