from fastapi import FastAPI
from routes import (administrado_routers,
                    consulta_routers,chats_routers,
                    empresa_routers,modulos_routers,
                    roles_routers,permisos_routers,
                    agente_routers,
                    agente_empresa_routers,
                    usuarios_routers,
                    derivaciones_routers,
                    login_routers,
                    mensajes_routers)
from fastapi.middleware.cors import CORSMiddleware
from middleware.auth_middleware import AuthMiddleware
from middleware.error_middleware import ErrorMiddleware
#Instancias api
app = FastAPI()
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5173", 
]
# app.add_middleware(AuthMiddleware)
app.add_middleware(ErrorMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],              # métodos permitidos (GET, POST, etc.)
    allow_headers=["*"],             # encabezados permitidos
)

#Incluyes las rutas de las API
app.include_router(administrado_routers.router)
app.include_router(consulta_routers.router)
app.include_router(chats_routers.router)
app.include_router(empresa_routers.router)
app.include_router(modulos_routers.router)
app.include_router(roles_routers.router)
app.include_router(permisos_routers.router)
app.include_router(agente_routers.router)
app.include_router(agente_empresa_routers.router)
app.include_router(usuarios_routers.router)
app.include_router(derivaciones_routers.router)
app.include_router(login_routers.router)
app.include_router(mensajes_routers.router)