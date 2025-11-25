from sqlalchemy.orm import Session
from models.permisos import  Permisos
from models.modulos import Modulos
from fastapi.responses import JSONResponse
from schemas.permisos_schema import PermisoSchema

def get_permisos(db:Session):
    permisos=db.query(Permisos,Modulos.nombre.label("modulo")).join(Modulos,Permisos.id_modulo==Modulos.id).filter(Permisos.estado=='A').all()
    if not permisos:
        return JSONResponse(content={"message":"No se encontraron permisos"})
    result = []
    for permiso, modulo in permisos:
        result.append({
            "id": permiso.id,
            "nombre": permiso.nombre,
            "accion": permiso.accion,
            "id_modulo": permiso.id_modulo,
            "modulo": modulo
        })

    return result

def create_permisos(db:Session,data:PermisoSchema):
    permiso=db.query(Permisos).filter(Permisos.id==data.id).first()
    if permiso:
        permiso.nombre=data.nombre
        permiso.acccion=data.accion
        permiso.id_modulo=data.id_modulo
        db.commit()
        db.refresh(permiso)
        return JSONResponse(content={"message":"Permiso actualizado correctamente","data":PermisoSchema.model_validate(permiso).model_dump()})
    permiso=Permisos(
        nombre=data.nombre,
        accion=data.accion,
        id_modulo=data.id_modulo,
        estado='A'
    )
    db.add(permiso)
    db.commit()
    db.refresh(permiso)
    return JSONResponse(content={"message":"El permiso fue creado correctamente","data":PermisoSchema.model_validate(permiso).model_dump()})

def delete_permiso(db:Session,id:int):
    permiso=db.query(Permisos).filter(Permisos.id==id).first()
    if not permiso:
        return JSONResponse(content={"message":"No se encontró el permiso"})
    permiso.estado="I"
    db.commit()
    db.refresh(permiso)
    return JSONResponse(content={"message":"Permiso eliminado correctamente"})