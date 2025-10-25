from fastapi import HTTPException
from models.administrado import Administrado
from schemas.administrado_schema import AdministradoCreate,AdministradoItem
from sqlalchemy.orm import Session
#:Session es un tipo de variable
def get_administrado(db:Session):
    result=db.query(Administrado).all()
    return result

def get_first_administrado(db:Session,id:int):
    result=db.query(Administrado).filter(Administrado.id==id,Administrado.estado=='A').first()
    return result
    
def create_administrado(administrado:AdministradoCreate,db:Session):
    administrado=Administrado(
        nombres=administrado.nombres,
        apellido_paterno=administrado.apellido_paterno,
        apellido_materno=administrado.apellido_materno,
        telefono=administrado.telefono,
        dni=administrado.dni,
        gmail=administrado.gmail,
        estado="A"
        )
    db.add(administrado)
    db.commit()
    db.refresh(administrado)
    return administrado

def update_administrado(db:Session,data:AdministradoItem):
    if not data:
        return HTTPException(status_code=400,detail="Id no encontrado")
    administrado=db.query(Administrado).filter(Administrado.id==data.id).first()
    if administrado is None:
        return HTTPException(status_code=400,detail="No se encontró")
    administrado.nombres=data.nombres
    administrado.apellido_materno=data.apellido_materno
    administrado.apellido_paterno=data.apellido_paterno
    administrado.dni=data.dni
    administrado.gmail=data.gmail
    administrado.telefono=data.telefono
    administrado.estado=data.estado
    db.add(administrado)
    db.commit()
    db.refresh(administrado)
    return administrado

def delete_administrado(id:int,db:Session):
    administrado=db.query(Administrado).filter(Administrado.id==id).first()
    if not administrado:
        return administrado
    administrado.estado='I'
    db.add(administrado)
    db.commit()
    db.refresh(administrado)
    return administrado