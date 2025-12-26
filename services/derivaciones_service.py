from models.derivaciones import Derivaciones
from models.usuarios import Usuarios
from sqlalchemy.orm import Session
from schemas.derivaciones_schemas import DerivacionSchema
from fastapi.responses import JSONResponse
from utils.methods import time
from schemas.usuario_schema import UsuarioSchema

def get_derivaciones(db:Session):
    derivaciones=db.query(Derivaciones).filter(Derivaciones.estado=="A").all()
    if not derivaciones:
        return JSONResponse(content={"message":"No se encontraron derivaciones"})
    return derivaciones
def create_derivaciones(db:Session,data:DerivacionSchema):
    time_actural=time.timeActual()
    # 1) Primer identificamos los usuario activos
    usuarios_activos=db.query(Usuarios).filter(Usuarios.activo=='S',Usuarios.empresa_id==data.id_empresa).all()
    if not usuarios_activos:
        return JSONResponse(content={"message":"No se encontrarón usuario activos en este momento."})
    return usuarios_activos
    derivacion=db.query(Derivaciones).filter(Derivaciones.id==data.id,Derivaciones.estado=="A").first()
    if derivacion:
        derivacion.motivo_derivacion=data.motivo_derivacion
        derivacion.id_usuario=data.id_usuario
        derivacion.id_session=data.id_session
        derivacion.observaciones=data.observaciones
        return JSONResponse(content={"message":"El registro fue editado correctamente","data":DerivacionSchema.model_validate(derivacion).model_dump()})
    derivacion=Derivaciones(
        fecha_derivacion=time_actural['fecha_registro'],
        motivo_derivacion=data.motivo_derivacion,
        id_usuario=data.id_usuario,
        id_session=data.id_session,
        observaciones=data.observaciones,
        estado='A',
        resuelto='N',
        estado_derivacion='PENDIENTE'
    )
    db.add(derivacion)
    db.commit()
    db.refresh(derivacion)
    return JSONResponse(content={"message":"La derivación se realizó correctamente","data":DerivacionSchema.model_validate(derivacion).model_dump()})

def delete_derivacion(db:Session,id:int):
    derivacion=db.query(Derivaciones).filter(Derivaciones.id==id,Derivaciones.estado=="A").first()
    if not derivacion:
        return JSONResponse(content={"message":"No se encontró derivación activa"})
    derivacion.estado='I'
    db.commit()
    return JSONResponse(content={"message":"Derivación eliminada correctamente"})