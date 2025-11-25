from pydantic import BaseModel

class PermisoSchema(BaseModel):
    id:int
    id_modulo:int
    nombre:str
    accion:str
    class Config:
        from_attributes=True