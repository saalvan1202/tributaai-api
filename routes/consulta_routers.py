from fastapi import Depends,APIRouter
from services.consulta_service import validar_consulta,registrar_consulta, validar_codigo_whatsapp,deudas_tributarias
from sqlalchemy.orm import Session
from database import get_db
from schemas.prediccion_schema import PrediccionRequest
from fastapi.responses import JSONResponse
router=APIRouter(prefix="/api/v1/consulta",tags=["Consulta"])
# response_model=list[ConsultasItem]
@router.get("/validar-agente")
def validate_agent(dni:int,telefono:int,db:Session=Depends(get_db)):
    return validar_consulta(db,dni,telefono)

@router.post("/registrar-consulta")
def create_consulta(dni:int,descripcion:str,telefono:int,db:Session=Depends(get_db)):
    return registrar_consulta(db,dni,descripcion,telefono)

@router.post("/validar-codigo")
def validate_code(dni:int,telefono:int,codigo:int,db:Session=Depends(get_db)):
    return validar_codigo_whatsapp(db,codigo,dni,telefono)

@router.post("/deudas-contribuyente")
def consulta_deuda_tributaria(dni:int,telefono:int,tipos_deudas:int,db:Session=Depends(get_db)):
    return deudas_tributarias(db,telefono,dni,tipos_deudas)

@router.post("/predecir")
async def predecir(data: PrediccionRequest):
    """
    Recibe los datos enviados desde el fetch y ejecuta la predicción
    """

    # 👉 Ejemplo: convertir a array para el modelo
    features = [
        data.MQ1,
        data.MQ2,
        data.MQ3,
        data.NORM1,
        data.NORM2,
        data.NORM3
    ]

    # 🔮 AQUÍ VA TU MODELO REAL
    # resultado_modelo = modelo.predict([features])
    # confianza = modelo.predict_proba([features]).max()

    # ⚠️ Simulación (para pruebas)
    resultado_modelo = "0"
    confianza = 0.98

    return JSONResponse(
        status_code=200,
        content={
            "resultado": resultado_modelo,
            "confianza": confianza
        }
)