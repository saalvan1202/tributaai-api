from sqlalchemy.orm import Session
from models.modulos import Modulos
from fastapi.responses import JSONResponse
from schemas.modulos_schema import ModuloSchema
from models.roles import Roles
from models.rol_permisos import RolPermisos
from models.permisos import Permisos

def get_roles_modulos(db:Session,id_rol:int):
    result={}
    modulos=db.query(Modulos.id.label("id_modulo"),
                     Modulos.nombre,
                     Modulos.link,
                     Modulos.icono
                     ).select_from(Roles).outerjoin(RolPermisos,
                                 RolPermisos.rol_id==Roles.id
                                 ).join(Permisos,
                                        Permisos.id==RolPermisos.permiso_id
                                        ).join(Modulos,
                                               Modulos.id==Permisos.id_modulo
                                               ).filter(Roles.estado=='A',
                                                        RolPermisos.estado=="A",
                                                        Roles.id==id_rol
                                                        ).all()
    if not modulos:
        return JSONResponse(content={"message":"No se encontraron roles"})
    for modulo in modulos:
            result[modulo.id_modulo]={
                "id":modulo.id_modulo,
                "nombre":modulo.nombre,
                "icono":modulo.icono,
                "link":modulo.link,
            }
    return list(result.values())

def get_modulos(db:Session):
    modulos=db.query(Modulos).filter(Modulos.estado=="A").all()
    if not modulos:
        return JSONResponse(content={"message":"No se encontraron modulos"})
    return modulos

def create_modulos(db:Session,data:ModuloSchema):
    modulo=db.query(Modulos).filter(Modulos.id==data.id).first()
    if modulo:
        modulo.nombre=data.nombre
        modulo.is_padre=data.is_padre
        modulo.link=data.link
        modulo.icono=data.icono
        db.commit()
        db.refresh(modulo)
        return JSONResponse(content={"message":f"El modulo fue actualizado correctamente.","data":ModuloSchema.model_validate(modulo).model_dump()})
    modulo=Modulos(
        nombre=data.nombre,
        link=data.link,
        is_padre=data.is_padre,
        icono=data.icono,
        estado='A'
    )
    db.add(modulo)
    db.commit()
    db.refresh(modulo)
    return JSONResponse(content={"message":"El registro se guardó correctamente","data":ModuloSchema.model_validate(modulo).model_dump()})
    
def delete_modulo(db:Session,id:int):
    modulo=db.query(Modulos).filter(Modulos.id==id).first()
    if not modulo:
        return JSONResponse(content={"message":"El modulo a eliminar no fue encontrado"})
    modulo.estado='I'
    db.commit()
    db.refresh(modulo)
    return JSONResponse(content={"message":"El registro fue eliminado"})
        