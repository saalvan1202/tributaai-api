from sqlalchemy.orm import Session
from models.roles import Roles
from models.rol_permisos import RolPermisos
from fastapi.responses import JSONResponse
from schemas.roles_schema import RolSchema
from schemas.roles_permisos_schema import RolesPermisoSchema

def get_roles(db:Session):
    roles=db.query(Roles).filter(Roles.estado=='A').all()
    if not roles:
        return JSONResponse(content={"message":"No se encontraron roles"})
    return roles
def get_roles_permisos(db:Session):
    result={}
    roles=db.query(Roles.nombre,Roles.id.label("id_rol"),RolPermisos.permiso_id.label("id_permiso")
                   ).outerjoin(RolPermisos,RolPermisos.rol_id==Roles.id
                               ).filter(Roles.estado=='A',RolPermisos.estado=="A"
                                        ).all()
    if not roles:
        return JSONResponse(content={"message":"No se encontraron roles"})
    for rol in roles:
        if not rol.id_rol in result:
            result[rol.id_rol]={
                "id":rol.id_rol,
                "nombres":rol.nombre,
                "permisos":[]
            }
        if not rol.id_permiso:
            continue
        result[rol.id_rol]["permisos"].append(rol.id_permiso)
    return list(result.values())

def save_roles_permisos(db:Session,valores:RolesPermisoSchema):
    permisos=db.query(Roles
                      ,RolPermisos.permiso_id.label("id_permiso")
                      ,RolPermisos.id.label("id_permisos_roles")
                      ).join(RolPermisos
                             ,Roles.id==RolPermisos.rol_id
                             ).filter(Roles.estado=="A"
                                      ,Roles.id==valores.id_rol
                                      ,RolPermisos.estado=="A"
                                      ).all()
    if not permisos:
        for valor in valores.valores:
            permisos_roles=RolPermisos(
                rol_id=valores.id_rol,
                permiso_id=valor,
                estado='A'
            )
            db.add(permisos_roles)
            db.commit() 
            db.refresh(permisos_roles)
        return JSONResponse(content={"message":"Permisos guardados correctamente"})
    permisos_existentes = {p.id_permiso for p in permisos}
    permisos_enviados=set(valores.valores)
    permisos_eliminar = permisos_existentes - permisos_enviados
        
    for valor in valores.valores:
        if valor in permisos_existentes:
            continue
        obj=db.query(RolPermisos
                     ).filter(RolPermisos.rol_id==valores.id_rol,
                                         RolPermisos.permiso_id==valor,
                                         RolPermisos.estado=="I"
                                         ).first()
        if obj:
            obj.estado='A'
            db.commit()
            db.refresh(obj)
            continue
        permisos_roles=RolPermisos(
            rol_id=valores.id_rol,
            permiso_id=valor,
            estado='A'
        )
        db.add(permisos_roles)
        db.commit()
        db.refresh(permisos_roles)
    if permisos_eliminar:
        db.query(RolPermisos
                 ).filter(RolPermisos.rol_id==valores.id_rol
                          ,RolPermisos.permiso_id.in_(permisos_eliminar)).update({RolPermisos.estado:'I'},synchronize_session=False)
        db.commit()
    return JSONResponse(content={"message":"Permisos guardados correctamente"})
            
    
def create_roles(db:Session,data:RolSchema):
    rol=db.query(Roles).filter(Roles.id==data.id).first()
    if rol:
        rol.nombre=data.nombre
        rol.descripcion=data.descripcion
        db.commit()
        db.refresh(rol)
    rol=Roles(
        nombre=data.nombre,
        descripcion=data.descripcion,
        estado='A'
    )
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return JSONResponse(content={"message":"El rol fue resgistrado con exito","data":RolSchema.model_validate(rol).model_dump()})
def delete_rol(db:Session,id:int):
    rol=db.query(Roles).filter(Roles.id==id).first()
    if not rol:
        return JSONResponse(content={"message":"No se encontró el rol"})
    rol.estado="I"
    db.commit()
    db.refresh(rol)
    return JSONResponse(content={"message":"El rol fue eliminado correctamentes"})
    
        