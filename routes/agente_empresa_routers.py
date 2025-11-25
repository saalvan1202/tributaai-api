from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from services.agente_empresa_service import (get_agente_empresa,
                                             create_agente_empresa,
                                             get_agentes_asignados_empresa,
                                             get_agentes_asignados_empresa_path,
                                             edit_agentes_asignados_empresa,
                                             estado_agentes_asignados_empresa)
from schemas.agente_empresa_schema import AgenteEmpresaCreate,AgenteEmpresaComunicate,AgenteEmpresaEstado

router=APIRouter(prefix="/api/v1/agente-empresa",tags=["Agente Empresa"])

@router.get("/")
def llamar(db:Session=Depends(get_db)):
    return get_agente_empresa(db)
@router.post("/")
def create(data:AgenteEmpresaCreate,db:Session=Depends(get_db)):
    return create_agente_empresa(db,data)
@router.get("/{id_empresa}")
def llamar_agente_asignados_empresas(id_empresa:int,db:Session=Depends(get_db)):
    return get_agentes_asignados_empresa(db,id_empresa)
@router.get("/{id_empresa}/{path}")
def llamar_agente_asignados_empresas_path(path:str,id_empresa:int,db:Session=Depends(get_db)):
    return get_agentes_asignados_empresa_path(db,id_empresa,path)
@router.post("/edit-comunicate")
def cambiar_comunicate_agente(data:AgenteEmpresaComunicate,db:Session=Depends(get_db)):
    return edit_agentes_asignados_empresa(db,data)
@router.post("/cambiar-estado")
def cambiar_estado_agente(data:AgenteEmpresaEstado,db:Session=Depends(get_db)):
    return estado_agentes_asignados_empresa(db,data)