from pydantic import BaseModel
from datetime import date

class ConsultasItem(BaseModel):
    id:int
    id_administrado:int
    descripcion:str
    codigo:int
    dni:int
    telefono:int
    verificado:str
    fecha:date
    class Config:
        from_attributes = True 