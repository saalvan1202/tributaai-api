from pydantic import BaseModel
from uuid import UUID

class DerivacionSchema(BaseModel):
    id:int
    telefono:str
    motivo_derivacion:str
    id_empresa:int
    class Config:
        from_attributes = True

class AceptarDerivacionSchema(BaseModel):
    uuid:UUID
    token:str