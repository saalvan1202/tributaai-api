from pydantic import BaseModel
from uuid import UUID

class UsuarioSchema(BaseModel):
    id:int
    nombre:str
    correo:str
    empresa_id:int
    rol_id:int
    usuario:str
    password:str
    apellidos:str
    telefono:str
    class Config:
        from_attributes=True