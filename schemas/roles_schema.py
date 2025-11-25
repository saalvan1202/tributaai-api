from pydantic import BaseModel
class RolSchema(BaseModel):
    id:int
    nombre:str
    descripcion:str
    class Config:
        from_attributes=True