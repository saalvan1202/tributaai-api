from fastapi import HTTPException
from database import Base,engine
from schemas.consulta_schema import ConsultasItem
from models.consulta import Consulta
from models.administrado import Administrado
from sqlalchemy.orm import Session
from datetime import datetime as dt
import pytz


def validar_consulta(db:Session,dni:int,telefono:int):
    zona_peru = pytz.timezone("America/Lima")
    fecha_actual = dt.now(zona_peru)
    fecha = fecha_actual.strftime("%Y/%m/%d")
    #------------------------Validamos la identidad del usuario--------------------->
    administrado=db.query(Administrado).filter(Administrado.dni==dni).first()
    if not administrado:
        return "El contribuyente no existe"
    ##Se pueda tener varias consultas con el mismo dni y telefono
    consulta=db.query(Consulta).filter(Consulta.dni==dni,Consulta.telefono==telefono,Consulta.fecha==fecha).first()
    if not consulta:
        return HTTPException(status_code=404,detail="No se encontró la consulta")
    if consulta.verificado=='S':
        return "Este usuario ya tiene un consulta hoy verficada"
    return consulta