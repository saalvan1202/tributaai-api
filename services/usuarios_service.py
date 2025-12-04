from models.usuarios import Usuarios
from models.empresa import Empresa
from models.roles import Roles
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from schemas.usuario_schema import UsuarioSchema
from security.security import hash_password

def get_usuarios(db:Session):
    usuarios=db.query(Usuarios.correo.label("correo"),
                      Usuarios.nombre.label("nombre"),
                      Usuarios.rol_id,
                      Usuarios.empresa_id,
                      Usuarios.id.label("id_usuario"),
                      Empresa.nombre.label("empresa"),
                      Roles.nombre.label("rol")
                      ).join(Roles,Roles.id==Usuarios.rol_id
                             ).join(Empresa,Empresa.id==Usuarios.empresa_id).filter(Usuarios.estado=='A',Empresa.estado=='A',Roles.estado=='A').all()
    if not usuarios:
        return JSONResponse(content={"message":"No se encontraron usuarios disponibles"})
    usuarios_list = []
    for u in usuarios:
        usuarios_list.append({
            "id": u.id_usuario,
            "nombre": u.nombre,
            "correo": u.correo,
            "empresa": u.empresa,
            "rol_id":u.rol_id,
            "empresa_id":u.empresa_id,
            "rol": u.rol
        })
    return usuarios_list

def create_usuarios(db:Session,data:UsuarioSchema):
    usuario=db.query(Usuarios).filter(Usuarios.id==data.id,Usuarios.estado=='A').first()
    if usuario:
        usuario.nombre=data.nombre
        usuario.correo=data.correo
        usuario.empresa_id=data.empresa_id
        usuario.rol_id=data.rol_id
        usuario.usuario=data.usuario
        usuario.apellidos=data.apellidos,
        db.commit()
        db.refresh(usuario)
        return JSONResponse(content={"message":"El usuario fue actualizado correctamente","data":UsuarioSchema.model_validate(usuario).model_dump()})
    usuario=Usuarios(
        nombre=data.nombre,
        apellidos=data.apellidos,
        correo=data.correo,
        empresa_id=data.empresa_id,
        rol_id=data.rol_id,
        activo='N',
        usuario=data.usuario,
        password=hash_password(data.password),
        estado='A'
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return JSONResponse(content={"message":"Se creó el usuario correctamente","data":UsuarioSchema.model_validate(usuario).model_dump()})

def delete_usuarios(db:Session,id:int):
    usuario=db.query(Usuarios).filter(Usuarios.estado=='A',Usuarios.id==id).first()
    if not usuario:
        return JSONResponse(content={"message":"El usuario no se encontró"})
    usuario.estado='I'
    db.commit()
    db.refresh(usuario)
    return JSONResponse(content={"message":"El usuario se eliminó correctamente"})