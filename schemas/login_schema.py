from pydantic import BaseModel

class LoginSchema(BaseModel):
    usuario: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
