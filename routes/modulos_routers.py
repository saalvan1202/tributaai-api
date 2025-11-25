from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from services.modulos_service import get_modulos,create_modulos,delete_modulo,get_roles_modulos
from schemas.modulos_schema import ModuloSchema

router=APIRouter(prefix="/api/v1/modulos",tags=["Modulos"])

@router.get("/")
def llamar(db:Session=Depends(get_db)):
    return get_modulos(db)
@router.post("/")
def create(data:ModuloSchema,db:Session=Depends(get_db)):
    return create_modulos(db,data)
@router.delete("/{id}")
def destro(id:int,db:Session=Depends(get_db)):
    return delete_modulo(db,id)
@router.get("/modulos-rol/{id_rol}")
def llamar_modulos_rol(id_rol:int,db:Session=Depends(get_db)):
    return get_roles_modulos(db,id_rol)