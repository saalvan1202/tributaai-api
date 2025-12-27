from pydantic import BaseModel

class DerivacionSchema(BaseModel):
    id:int
    id_usuario:int
    telefono:str
    motivo_derivacion:str
    observaciones:str
    id_empresa:int
    class Config:
        from_attributes = True 