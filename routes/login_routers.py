from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from security.security import verify_token,create_access_token,verify_password
from schemas.login_schema import LoginSchema,LoginResponse
from database import get_db
from models.usuarios import Usuarios 

router=APIRouter(prefix="/api/v1/login",tags=["Login"])

@router.post("/")
def login_user(login:LoginSchema,db:Session = Depends(get_db)):
    usuario=db.query(Usuarios).filter(Usuarios.usuario==login.usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Usuario no encontrado")
    if not verify_password(login.password,usuario.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Contraseña incorrectas")
    usuario.activo='S'
    db.commit()
    db.refresh(usuario)
    return LoginResponse(access_token=create_access_token(data={"username":usuario.usuario,"id_usuario":usuario.id,"nombre":usuario.nombre}),token_type="bearer")