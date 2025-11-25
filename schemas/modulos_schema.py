from pydantic import BaseModel

class ModuloSchema(BaseModel):
    id:int
    nombre:str
    link:str
    is_padre:str
    icono:str
    class Config:
        from_attributes = True