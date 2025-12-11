from pydantic import BaseModel
from sqlalchemy import JSON

class MensajesSchema(BaseModel):
    wa_id:str
    nombre:str
    id_usuario:int
    direction:str
    waba_message_id:str
    message_type:str
    text_content:str
    raw_json:dict | list
    timestamp:int