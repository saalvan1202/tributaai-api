from fastapi import APIRouter,Depends
from database import get_db
from schemas.agente_schema import AgenteSchema
from sqlalchemy.orm import Session
from services.agentes_service import get_agentes,create_agente,delete_agente


router=APIRouter(prefix="/api/v1/agente",tags=["Agentes"])

@router.get("/")
def llamar(db:Session=Depends(get_db)):
    return get_agentes(db)

@router.post("/")
def create(data:AgenteSchema,db:Session=Depends(get_db)):
    return create_agente(db,data)

@router.delete("/{id}")
def destroy(id:int,db:Session=Depends(get_db)):
    return delete_agente(db,id)