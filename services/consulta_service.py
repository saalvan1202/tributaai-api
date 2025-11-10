from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from database import Base,engine
from schemas.consulta_schema import ConsultasItem
from schemas.tipo_deudas_schema import TipoDeudas
from models.consulta import Consulta
from models.administrado import Administrado
from sqlalchemy.orm import Session
from sqlalchemy import text,func
from services.whats_app_api import Whatsapp
import random
from repositories.consultas_repositoty import ConsultasRepo
from utils.methods import time
def deudas_tributarias(db:Session,telefono:int,dni:int,tipo_deudas:int):
    whatsapp=Whatsapp()
    time_now=time.timeActual()
    fecha=time_now["fecha_validacion"]
    administrado=db.query(Administrado).filter(Administrado.dni==dni).first()
    if not administrado:
        return JSONResponse(content={"message":"El contribuyente no existe"})
    consulta_registrada=db.query(Consulta).filter(Consulta.dni==dni,Consulta.telefono==telefono,func.date(Consulta.fecha)==fecha).first()
    if not consulta_registrada:
        #<-------------------Con la idea que el tiempo de sesión de cada consulta es 24 horas ----->
        return JSONResponse(content={"message":"La sesion de la consulta del contribuyente vencio"})
    whatsapp.whats_text(telefono,"📄 Espere un momento, estamos revisando sus deudas...")
    result=ConsultasRepo.consulta_deudas(db,tipo_deudas,administrado.cod_administrado)
    if not result:
        return JSONResponse(content={"message":"El contribuyente no cuenta con deudas en ese momento."})
    result = [dict(row._mapping) for row in result]
    result_serialized = jsonable_encoder(result)
    data = {"deudas": result_serialized}
    mensaje=ConsultasRepo.generar_mensaje_whatsapp(data)
    whatsapp.whats_text(telefono, mensaje)
    return JSONResponse(content={'message':"El resumen de deudas fue enviado con exito"})
    
    
def validar_codigo_whatsapp(db:Session,codigo:int,dni:int,telefono:int):
    whatsapp=Whatsapp()
    time_now=time.timeActual()
    fecha = time_now["fecha_validacion"]
    administrado=db.query(Administrado).filter(Administrado.dni==dni).first()
    if not administrado:
        return JSONResponse(content={"message":"El contribuyente no existe"})
    whatsapp.whats_text(telefono,f"*Validando Código...*")
    consulta_registrada=db.query(Consulta).filter(Consulta.dni==administrado.dni,Consulta.telefono==telefono,func.date(Consulta.fecha)==fecha).first()
    if consulta_registrada:
        result=ConsultasRepo.tipo_deudas(db,administrado.cod_administrado)
        if consulta_registrada.verificado=='S':
            if not result:     
                return JSONResponse(content={"message":f"El contribuyente tiene un consulta registrada y validada el día de hoy con este dispositivo. También se comprobó que el contribuyente {administrado.cod_administrado} no tiene deudas pendientes","client":str(administrado.nombres)})
            return JSONResponse(content={"message":"El contribuyente tiene un consulta registrada y validada el día de hoy con este dispositivo","client":str(administrado.nombres)})
        if consulta_registrada.codigo==codigo:
            consulta_registrada.verificado='S'
            db.add(consulta_registrada)
            db.commit()
            db.refresh(consulta_registrada)
            if not result:     
                return JSONResponse(content={"message":f"El código fue validado correctamente. También se comprobó que el contribuyente {administrado.cod_administrado} no tiene deudas pendientes","client":str(administrado.nombres)})
            return JSONResponse(content={"message":f"El código fue validado correctamente. El contribuyente {administrado.cod_administrado} tiene las siguientes deudas: {result}","client":str(administrado.nombres)})    
        return JSONResponse(content={"message":"El código que adjuntaste no es correcto, verifique el código que se mandó a su número.","client":str(administrado.nombres)})
    return JSONResponse(content={"message":"El contribuyente no tiene una deuda registrada el día de hoy, deseas registrar una consulta?"})
#<------------------------ Puntos importantes a considerar ------------------------>
#1) Las consultas se pueden hacer desde cualquier dispositivo, el registro de ella es por dispositivo
#2) Pero el código de valición se envía la telefono registrado en la base de datos
def registrar_consulta(db:Session,dni:int,descripcion:str,telefono:int):
    whatsapp=Whatsapp()
    time_now=time.timeActual()
    fecha_registro = time_now["fecha_registro"]
    fecha_validacion=time_now["fecha_validacion"]
    administrado=db.query(Administrado).filter(Administrado.dni==dni).first()
    if not administrado:
        return JSONResponse(content={"message":"El contribuyente no existe"})
    whatsapp.whats_text(administrado.telefono,f"*Espere un momento*, estamos registrando su consulta...")
    consulta_registrada=db.query(Consulta).filter(Consulta.dni==administrado.dni,Consulta.telefono==telefono,func.date(Consulta.fecha)==fecha_validacion).first()
    if consulta_registrada:
        if consulta_registrada.verificado=='S':
            result=ConsultasRepo.tipo_deudas(db,administrado.cod_administrado)
            if not result:
                return JSONResponse(content={"message": "Hemos validado tu DNI, se encontró una consulta tuya registrada y validada con este dispositivo. Recordando también que el no tiene ninguan deuda pendiente.","client":str(administrado.nombres)}) 
            return JSONResponse(content={"message": f"Hemos validado tu DNI, se encontró una consulta tuya registrada y validada con este dispositivo. Tus tipos de deudas son {result}","client":str(administrado.nombres)})
        elif consulta_registrada.verificado=='N':
                return JSONResponse(content={"consulta":str(consulta_registrada.dni),"message":"El contribuyente tiene un consulta registrada el día de hoy con este dispositivo, pero no está verificada","client":str(administrado.nombres)})
    codigo=random.randint(100000, 999999)
    consulta=Consulta(
        id_administrado=administrado.id,
        descripcion=descripcion,
        codigo=codigo,
        dni=administrado.dni,
        telefono=telefono,
        verificado='N',
        fecha=fecha_registro
    )

    if consulta.telefono==telefono:
        consulta.verificado='S'
        db.add(consulta)
        db.commit()
        db.refresh(consulta)
        result=ConsultasRepo.tipo_deudas(db,administrado.cod_administrado)
        return JSONResponse(content={"message":"Se verifico el que el numero registrado es el mismo en el que se está comunicando. Tus tipos de deudas son {result}","client":str(administrado.nombres)})
    whatsapp.whats_text(administrado.telefono,f"Este es su código de verificación: {codigo}")
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    return JSONResponse(content={"message":"La consulta fue registrada exitosamente, ingrese el código que se envio a su número registrado.","client":str(administrado.nombres)})
    
def validar_consulta(db:Session,dni:int,telefono:int):
    whatsapp=Whatsapp()
    time_now=time.timeActual()
    fecha = time_now["fecha_validacion"]
    whatsapp.whats_text(telefono,"*Estoy validando tu documento*. Dame un momento, por favor  🙂")
    #------------------------Validamos la identidad del usuario--------------------->
    administrado=db.query(Administrado).filter(Administrado.dni==dni).first()
    whatsapp.whats_text(telefono,"Listo 👍")
    if not administrado:
        return JSONResponse(content={"message": "El contribuyente no existe"})
    ##Se pueda tener varias consultas con el mismo dni y telefono, pero no en la misma fecha
    #Tenemos un detalle con el tipo TiemStamp -> Cuando se intenta comparar solo con la fecha tiene que suar el func.date 
    consulta=db.query(Consulta).filter(Consulta.dni==dni,Consulta.telefono==telefono,func.date(Consulta.fecha)==fecha).first()
    if not consulta:
        if administrado.telefono==telefono:
            return JSONResponse(content={"message": "Hemos validado tu DNI y verificado tu identidad, pero no se encontró una consulta tuya registrada con este dispositivo el día de hoy",
                    "client":str(administrado.nombres)})
        return JSONResponse(content={"message": "Hemos validado tu DNI, pero no se encontró una consulta tuya registrada con este dispositivo el día de hoy",
                                     "client":str(administrado.nombres)})
    if consulta.verificado=='S':
        result=ConsultasRepo.tipo_deudas(db,administrado.cod_administrado)
        if not result:
           return JSONResponse(content={"message": "Hemos validado tu DNI, se encontró una consulta tuya registrada y validada con este dispositivo. Recordando también que el no tiene ninguan deuda pendiente.","client":str(administrado.nombres)}) 
        return JSONResponse(content={"message": f"Hemos validado tu DNI, se encontró una consulta tuya registrada y validada con este dispositivo. Tus tipos de deudas son {result}","client":str(administrado.nombres)})
    elif consulta.verificado=='N':
        return JSONResponse(content={"message": "Hemos validado tu DNI, se encontró una consulta tuya registrada y no está validada con este dispositivo","client":str(administrado.nombres)})
    return consulta