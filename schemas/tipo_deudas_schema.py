from pydantic import BaseModel
from typing import List

class TipoDeudas(BaseModel):
    tipos_deudas:List[int]