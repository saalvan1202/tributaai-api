from pydantic import BaseModel
class AgenteEmpresaSchema(BaseModel):
    id:int
    agente_id:int
    empresa_id:int
    class Config:
        from_attributes=True
        
class AgenteEmpresaCreate(BaseModel):
    id_empresa:int
    agentes:list[int]
    class Config:
        from_attributes=True

class AgenteEmpresaComunicate(BaseModel):
    id_agente_empresa:int
    instancia:str
    telefono:str
    
class AgenteEmpresaEstado(BaseModel):
    id_agente_empresa:int
    estado:str
    
class AgenteValidate(BaseModel):
    id_empresa:int
    path:str
    telefono:str