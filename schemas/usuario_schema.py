from pydantic import BaseModel

class UsuarioSchema(BaseModel):
    id:int
    nombre:str
    correo:str
    empresa_id:int
    rol_id:int
    usuario:str
    password:str
    apellidos:str
    class Config:
        from_attributes=True