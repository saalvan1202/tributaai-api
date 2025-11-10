from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.administrado_service import get_administrado,create_administrado,get_first_administrado,update_administrado,delete_administrado
from schemas.administrado_schema import AdministradoItem,AdministradoCreate

router=APIRouter(prefix="/api/v1/administrado",tags=["Administrado"])

@router.get("/",response_model=list[AdministradoItem])
def get(db:Session=Depends(get_db)):
    return get_administrado(db)

@router.post("/",response_model=AdministradoCreate)
def create(data:AdministradoCreate,db:Session=Depends(get_db)):
    return create_administrado(data,db)


@router.get("/{id}")
def get_first(id:int,db:Session=Depends(get_db)):
    result=get_first_administrado(db,id)
    if(not result):
        return HTTPException(status_code=200,detail="No se encontró")
    return result

@router.put("/",response_model=AdministradoItem)
def update(data:AdministradoItem,db:Session=Depends(get_db)):
    return update_administrado(db,data)

@router.delete("/{id}",response_model=AdministradoItem)
def delete(id:int,db:Session=Depends(get_db)):
    administrado=delete_administrado(id,db)
    if not administrado:
        return HTTPException(detail="No se encontró el administrado",status_code=200)
    return administrado

#TEST
# {
#   "id": 1,
#   "nombres": "Shandes Andres"
#   "apellido_paterno": "Alvans",
#   "apellido_materno": "Rios",
#   "telefono": 901981127,
#   "dni": 71456922,
#   "gmail": "ashande75@gmail.com"
# }
#Instropección => Capacidad de lenguaje para analizarce a uno mismo, osea metodo o funciones espcificas que me permite
#analizar mis funciones internas.
# Los tipos => osea las variables se manjean, es el fuerte de FastAPI con pydantic   
#El tipo list lo que hace es que la salida sea un array y si le quitas que sea un obj