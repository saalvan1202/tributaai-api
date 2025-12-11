from database import get_db
from schemas.mensajes_schema import MensajesSchema
from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter
from services.contactos_service import save_mensaje


router=APIRouter(prefix="/api/v1/mensajes",tags=['Mensajes'])

@router.post("/")
def save(data:MensajesSchema,db:Session=Depends(get_db)):
    return save_mensaje(db,data)