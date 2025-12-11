from pydantic import BaseModel

class ContactoSchema(BaseModel):
    id:int
    wa_id:str
    nombre:str