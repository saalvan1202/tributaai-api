from pydantic import BaseModel
class AgenteSchema(BaseModel):
    id:int
    nombre:str
    descripcion:str
    logo:str
    path:str
    class Config:
        from_attributes=True