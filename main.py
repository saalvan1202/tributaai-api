from fastapi import FastAPI
from routes import administrado_routers,consulta_routers
#Instancias api
app = FastAPI()
#Incluyes las rutas de las API
app.include_router(administrado_routers.router)
app.include_router(consulta_routers.router)
