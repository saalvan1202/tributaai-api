from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from services.empresa_service import get_empresas,create_empresa,delete_empresa,search_empresa
from schemas.empresas_schema import EmpresaSchema
router=APIRouter(prefix="/api/v1/empresas",tags=["Empresas"])

@router.get("/")
def get(db:Session=Depends(get_db)):
    return get_empresas(db)

@router.post("/",response_model=EmpresaSchema)
def create(data:EmpresaSchema,db:Session=Depends(get_db)):
    return create_empresa(db,data)
@router.delete("/{id}")
def destroy(id:int,db:Session=Depends(get_db)):
    return  delete_empresa(db,id)

@router.get("/search-empresa/{q}")
def search(q:str,db:Session=Depends(get_db)):
    return search_empresa(q,db)
