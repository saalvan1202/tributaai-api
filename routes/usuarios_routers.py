from fastapi import APIRouter,Depends
from services.usuarios_service import get_usuarios,create_usuarios,delete_usuarios
from sqlalchemy.orm import Session
from database import get_db
from schemas.usuario_schema import UsuarioSchema

router=APIRouter(prefix="/api/v1/usuarios",tags=['Usuarios'])

@router.get("/")
def llamar(db:Session=Depends(get_db)):
    return get_usuarios(db)

@router.post("/")
def create(data:UsuarioSchema,db:Session=Depends(get_db)):
    return create_usuarios(db,data)

@router.delete("/{id}")
def destroy(id:int,db:Session=Depends(get_db)):
    return delete_usuarios(db,id)