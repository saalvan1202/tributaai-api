from pydantic import BaseModel

class PrediccionRequest(BaseModel):
    MQ1: float
    MQ2: float
    MQ3: float
    NORM1: float
    NORM2: float
    NORM3: float
