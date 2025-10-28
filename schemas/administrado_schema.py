from pydantic import BaseModel
from typing import Optional

class AdministradoItem(BaseModel):
    id:int
    nombres:str
    apellido_paterno:str
    apellido_materno:str
    telefono:int
    dni:int
    gmail:str
    cod_administrado:Optional[str] = None
    class Config:
        from_attributes = True 

class AdministradoCreate(BaseModel):
    nombres:str
    apellido_paterno:str
    apellido_materno:str
    telefono:int
    dni:int
    gmail:str
    class Config:
        from_attributes = True 
    