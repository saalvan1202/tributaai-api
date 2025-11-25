from pydantic import BaseModel
class EmpresaSchema(BaseModel):
    nombre:str
    ruc:str
    direccion:str
    class Config:
        from_attributes = True