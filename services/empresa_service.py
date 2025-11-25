from models.empresa import Empresa
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from schemas.empresas_schema import EmpresaSchema
from fastapi.responses import JSONResponse


def get_empresas(db:Session):
    empresas=db.query(Empresa).filter(Empresa.estado=="A").all()
    if not empresas:
        return JSONResponse(content={"message":"No se encontraron emrpesas"})
    return empresas

def create_empresa(db:Session,data:EmpresaSchema):
    obj=db.query(Empresa).filter(Empresa.ruc==data.ruc,Empresa.estado=="A").first()
    if obj:
        obj.nombre=data.nombre,
        obj.ruc=data.ruc,
        obj.direccion=data.direccion,
        obj.estado='A'
        db.commit()
        db.refresh(obj)
        return JSONResponse(content={"message":"Registro editado correctamente correctamente","empresa":EmpresaSchema.model_validate(obj).model_dump(),"status":"200"})
    empresa=Empresa(
        nombre=data.nombre,
        ruc=data.ruc,
        direccion=data.direccion,
        estado='A'              
    )
    db.add(empresa)
    db.commit()
    db.refresh(empresa)
    return JSONResponse(content={"message":"Registrado Correctamente","empresa":EmpresaSchema.model_validate(empresa).model_dump(),"status":"200"})

def delete_empresa(db:Session,id:int):
    empresa=db.query(Empresa).filter(Empresa.id==id,Empresa.estado=="A").first()
    if not empresa:
        return JSONResponse(content={"message":"No se encontró la empresa"})
    empresa.estado='I'
    db.commit()
    db.refresh(empresa)
    return JSONResponse(content={"message":"Se eliminó la empresa correctamente"})

def search_empresa(q:str,db:Session):
    results=db.query(Empresa).filter(Empresa.nombre.ilike(f"%{q}%") | Empresa.ruc.like(f"%{q}%")).all()
    return results
    
