from fastapi import APIRouter,Depends
from database import get_db
from sqlalchemy.orm import Session
from services.contactos_service import get_contactos

router=APIRouter(prefix="/api/v1/contactos",tags=['Contactos'])

@router.get("/")
def llamar(db:Session=Depends(get_db)):
    return get_contactos(db)
