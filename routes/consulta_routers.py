from fastapi import Depends,HTTPException,APIRouter
from services.consulta_service import validar_consulta,registrar_consulta
from sqlalchemy.orm import Session
from schemas.consulta_schema import ConsultasItem
from database import get_db

router=APIRouter(prefix="/consulta",tags=["Consulta"])
# response_model=list[ConsultasItem]
@router.get("/validar-agente")
def validate_agent(dni:int,telefono:int,db:Session=Depends(get_db)):
    return validar_consulta(db,dni,telefono)

@router.post("/registrar-consulta")
def create_consulta(dni:int,descripcion:str,telefono:int,db:Session=Depends(get_db)):
    return registrar_consulta(db,dni,descripcion,telefono)