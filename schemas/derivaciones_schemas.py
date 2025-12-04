from pydantic import BaseModel

class DerivacionSchema(BaseModel):
    id:int
    id_usuario:int
    id_session:str
    motivo_derivacion:str
    observaciones:str
    class Config:
        from_attributes = True 