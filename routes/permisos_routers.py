from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from services.permisos_service import get_permisos,create_permisos,delete_permiso
from schemas.permisos_schema import PermisoSchema

router=APIRouter(prefix="/api/v1/permisos",tags=["Permisos"])

@router.get("/")
def llamar(db:Session=Depends(get_db)):
    return get_permisos(db)
@router.post("/")
def create(data:PermisoSchema,db:Session=Depends(get_db)):
    return create_permisos(db,data)
@router.delete("/{id}")
def destroy(id:int,db:Session=Depends(get_db)):
    return delete_permiso(db,id)