from fastapi import FastAPI
from routes import administrado_routers,consulta_routers,chats_routers
from fastapi.middleware.cors import CORSMiddleware
#Instancias api
app = FastAPI()
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5173", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],              # métodos permitidos (GET, POST, etc.)
    allow_headers=["*"],              # encabezados permitidos
)
#Incluyes las rutas de las API
app.include_router(administrado_routers.router)
app.include_router(consulta_routers.router)
app.include_router(chats_routers.router)