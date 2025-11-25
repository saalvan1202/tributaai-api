from pydantic import BaseModel
class RolesPermisoSchema(BaseModel):
    id_rol:int
    valores:list[int]