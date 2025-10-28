from fastapi import HTTPException
from fastapi.responses import JSONResponse
from database import Base,engine
from schemas.consulta_schema import ConsultasItem
from models.consulta import Consulta
from models.administrado import Administrado
from sqlalchemy.orm import Session
from datetime import datetime as dt
import pytz
from services.whats_app_api import Whatsapp
import random

#------------------------ Puntos importantes a considerar ------------------------>
#1) Las consultas se pueden hacer desde cualquier dispositivo, el registro de ella es por dispositivo
#2) Pero el código de valición se envía la telefono registrado en la base de datos

def registrar_consulta(db:Session,dni:int,descripcion:str,telefono:int):
    whatsapp=Whatsapp()
    zona_peru = pytz.timezone("America/Lima")
    fecha_actual = dt.now(zona_peru)
    fecha = fecha_actual.strftime("%Y/%m/%d")
    administrado=db.query(Administrado).filter(Administrado.dni==dni).first()
    if not administrado:
        return JSONResponse(content={"message":"El contribuyente no existe"})
    whatsapp.whats_text(administrado.telefono,f"*Espere un momento*, estamos registrando su consulta...")
    consulta_registrada=db.query(Consulta).filter(Consulta.dni==administrado.dni,Consulta.telefono==telefono,Consulta.fecha==fecha).first()
    if consulta_registrada:
        if consulta_registrada.verificado=='S':
            return JSONResponse(content={"message":"El contribuyente tiene un consulta registrada el día de hoy con este dispositivo","client":str(administrado.nombres)})
        elif consulta_registrada.verificado=='N':
            return JSONResponse(content={"consulta":str(consulta_registrada.dni),"message":"El contribuyente tiene un consulta registrada el día de hoy con este dispositivo, pero no está verificada","client":str(administrado.nombres)})
    codigo=random.randint(100000, 999999)
    consulta=Consulta(
        id_administrado=administrado.id,
        descripcion=descripcion,
        codigo=codigo,
        dni=administrado.dni,
        telefono=administrado.telefono,
        verificado='N',
        fecha=fecha
    )
    db.add(consulta)
    db.commit()
    whatsapp.whats_text(administrado.telefono,f"Este es su código de verificación: {codigo}")
    db.refresh(consulta)
    return JSONResponse(content={"message":"La consulta fue registrada exitosamente, ingrese el código que se envio a su número registrado.","client":str(administrado.nombres)})
    
def validar_consulta(db:Session,dni:int,telefono:int):
    whatsapp=Whatsapp()
    zona_peru = pytz.timezone("America/Lima")
    fecha_actual = dt.now(zona_peru)
    fecha = fecha_actual.strftime("%Y/%m/%d")
    whatsapp.whats_text(telefono,"*Estoy validando tu documento*. Dame un momento, por favor  🙂")
    #------------------------Validamos la identidad del usuario--------------------->
    administrado=db.query(Administrado).filter(Administrado.dni==dni).first()
    whatsapp.whats_text(telefono,"Listo 👍")
    if not administrado:
        return JSONResponse(content={"message": "El contribuyente no existe"})
    ##Se pueda tener varias consultas con el mismo dni y telefono
    consulta=db.query(Consulta).filter(Consulta.dni==dni,Consulta.telefono==telefono,Consulta.fecha==fecha).first()
    if not consulta:
        return JSONResponse(content={"message": "Hemos validado tu DNI, pero no se encontró una consulta tuya registrada con este dispositivo el día de hoy",
                                     "client":str(administrado.nombres)})
    if consulta.verificado=='S':
        return JSONResponse(content={"message": "Hemos validado tu DNI, se encontró una consulta tuya registrada y validada con este dispositivo","client":str(administrado.nombres)})
    elif consulta.verificado=='N':
        return JSONResponse(content={"message": "Hemos validado tu DNI, se encontró una consulta tuya registrada y no está validada con este dispositivo","client":str(administrado.nombres)})
    return consulta