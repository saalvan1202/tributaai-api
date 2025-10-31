from fastapi import Depends,HTTPException,APIRouter
from services.consulta_service import validar_consulta,registrar_consulta, validar_codigo_whatsapp
from sqlalchemy.orm import Session
from schemas.consulta_schema import ConsultasItem
from database import get_db
import joblib
import numpy as np
from pydantic import BaseModel
import os
router=APIRouter(prefix="/consulta",tags=["Consulta"])
# response_model=list[ConsultasItem]
@router.get("/validar-agente")
def validate_agent(dni:int,telefono:int,db:Session=Depends(get_db)):
    return validar_consulta(db,dni,telefono)

@router.post("/registrar-consulta")
def create_consulta(dni:int,descripcion:str,telefono:int,db:Session=Depends(get_db)):
    return registrar_consulta(db,dni,descripcion,telefono)

@router.post("/valirdar-codigo")
def validate_code(dni:int,telefono:int,codigo:int,db:Session=Depends(get_db)):
    return validar_codigo_whatsapp(db,codigo,dni,telefono)
    