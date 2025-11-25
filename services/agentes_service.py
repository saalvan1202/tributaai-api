from sqlalchemy.orm import Session
from models.agentes import Agente
from models.agente_empresa import AgenteEmpresa
from fastapi.responses import JSONResponse
from schemas.agente_schema import AgenteSchema

def get_agentes(db:Session):
    agentes=db.query(Agente).filter(Agente.estado=="A").all()
    if not agentes:
        return JSONResponse(content={"message":"No se encontraron agentes registrados"})
    return agentes

def create_agente(db:Session,data:AgenteSchema):
    agente=db.query(Agente).filter(Agente.id==data.id,Agente.estado=='A').first()
    if agente:
        agente.descripcion=data.descripcion
        agente.nombre=data.nombre
        agente.path=data.path
        agente.logo=data.logo
        db.commit()
        db.refresh(agente)
        return JSONResponse(content={"message":"Se modificó correctamente el agente","data":AgenteSchema.model_validate(agente).model_dump()})
    agente=Agente(
        nombre=data.nombre,
        descripcion=data.descripcion,
        path=data.path,
        logo=data.logo,
        estado='A'
    )
    db.add(agente)
    db.commit()
    db.refresh(agente)
    return JSONResponse(content={"message":"Se agregó correctamente el agente","data":AgenteSchema.model_validate(agente).model_dump()})

def delete_agente(db:Session,id:int):
    agente=db.query(Agente).filter(Agente.id==id).first()
    if not agente:
        return JSONResponse(content={"message":"No se encontró el agente a eliminar"})
    agente.estado='I'
    db.commit()
    return JSONResponse(content={"message":"El agente fue eliminado correctamente"})