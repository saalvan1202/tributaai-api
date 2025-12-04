from fastapi import APIRouter,Depends
from services.derivaciones_service import (get_derivaciones,
                                           create_derivaciones,
                                           delete_derivacion)
from sqlalchemy.orm import Session
from database import get_db
from schemas.derivaciones_schemas import DerivacionSchema

router=APIRouter(prefix="/api/v1/derivaciones",tags=["Derivaciones"])

@router.get("/")
def llamar(db:Session=Depends(get_db)):
    return get_derivaciones(db)

@router.post("/")
def create(data:DerivacionSchema,db:Session=Depends(get_db)):
    return create_derivaciones(db,data)

@router.delete("/{id}")
def destroy(id:int,db:Session=Depends(get_db)):
    return delete_derivacion(db,id)