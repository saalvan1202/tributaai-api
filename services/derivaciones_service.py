from models.derivaciones import Derivaciones
from models.usuarios import Usuarios
from sqlalchemy.orm import Session
from schemas.derivaciones_schemas import DerivacionSchema
from fastapi.responses import JSONResponse
from utils.methods import time
from schemas.usuario_schema import UsuarioSchema
from services.whats_app_api import Whatsapp
from models.contactos import Contactos
from uuid import UUID

def get_derivaciones(db:Session):
    derivaciones=db.query(Derivaciones).filter(Derivaciones.estado=="A").all()
    if not derivaciones:
        return JSONResponse(content={"message":"No se encontraron derivaciones"})
    return derivaciones
def create_derivaciones(db:Session,data:DerivacionSchema):
    whatsapp=Whatsapp()
    time_actural=time.timeActual()
    time_wpp=time_actural["timestamp"]
    #Buscamos el contacto
    contacto=db.query(Contactos).filter(Contactos.wa_id==data.telefono).first()
    if not contacto:
        return JSONResponse(content={"message":"No se encontró el contacto"})
    # 1) Primer identificamos los usuario activos
    usuarios_activos=db.query(Usuarios).filter(Usuarios.activo=='S',Usuarios.empresa_id==data.id_empresa).all()
    if not usuarios_activos:
        return JSONResponse(content={"message":"No se encontrarón usuario activos en este momento."})
    derivacion=db.query(Derivaciones).filter(Derivaciones.id==data.id,Derivaciones.estado=="A").first()
    if derivacion:
        derivacion.motivo_derivacion=data.motivo_derivacion
        derivacion.id_usuario=data.id_usuario
        derivacion.id_contacto=contacto.id
        derivacion.observaciones=data.observaciones
        return JSONResponse(content={"message":"El registro fue editado correctamente","data":DerivacionSchema.model_validate(derivacion).model_dump()})
    derivacion=Derivaciones(
        fecha_derivacion=time_actural['fecha_registro'],
        motivo_derivacion=data.motivo_derivacion,
        id_usuario=data.id_usuario,
        id_contacto=contacto.id,
        observaciones=data.observaciones,
        estado='A',
        resuelto='N',
        estado_derivacion='PENDIENTE'
    )
    db.add(derivacion)
    db.commit()
    db.refresh(derivacion)
    for usuario in usuarios_activos:
         whatsapp.waba_text(db,usuario.telefono,time_wpp,"Necesitamos de tu ayuda, para resolver un problema. Ingresa a este link para aceptar.")
    return "Estamos buscando.."
    return JSONResponse(content={"message":"La derivación se realizó correctamente","data":DerivacionSchema.model_validate(derivacion).model_dump()})

def get_derivacion(db:Session,uuid:UUID):
    derivacion=(db.query(Derivaciones,Contactos.wa_id
                        ).join(Contactos,Contactos.id==Derivaciones.id_contacto
                               ).filter(Derivaciones.uuid==uuid,Derivaciones.estado=='A'
                                        ).first())
    derivar, wa_id = derivacion

    return {
        "id": derivar.id,
        "uuid": derivar.uuid,
        "estado": derivar.estado,
        "id_contacto": derivar.id_contacto,
        "wa_id": wa_id,
        "motivo":derivar.motivo_derivacion,
        "estado_derivacion":derivar.estado_derivacion
    }

def delete_derivacion(db:Session,id:int):
    derivacion=db.query(Derivaciones).filter(Derivaciones.id==id,Derivaciones.estado=="A").first()
    if not derivacion:
        return JSONResponse(content={"message":"No se encontró derivación activa"})
    derivacion.estado='I'
    db.commit()
    return JSONResponse(content={"message":"Derivación eliminada correctamente"})