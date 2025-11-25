from fastapi import APIRouter,Depends
from database import get_db
from sqlalchemy.orm import Session
from services.roles_service import get_roles,delete_rol,create_roles,get_roles_permisos,save_roles_permisos
from schemas.roles_schema import RolSchema
from schemas.roles_permisos_schema import RolesPermisoSchema

router=APIRouter(prefix="/api/v1/roles",tags=["Roles"])

@router.get("/")
def llamar(db:Session=Depends(get_db)):
    return get_roles(db)
@router.post("/")
def create(data:RolSchema,db:Session=Depends(get_db)):
    return create_roles(db,data)
@router.delete("/{id}")
def destroy(id:int,db:Session=Depends(get_db)):
    return delete_rol(db,id)
@router.get("/roles-permisos")
def roles_permisos(db:Session=Depends(get_db)):
    return get_roles_permisos(db)
@router.post("/roles-permisos")
def create_roles_permisos(valores:RolesPermisoSchema,db:Session=Depends(get_db)):
    return save_roles_permisos(db,valores)