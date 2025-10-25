from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv
import os
#Cargamos el archivo .env
load_dotenv()
##CREAMOS LA CONEXIÓN A LA BASE DE DATOS
engine=create_engine(os.getenv("DATABASE_URL"))
SESSION=sessionmaker(bind=engine)
Base=declarative_base()
#Llamada a la base de datos
def get_db():
    db=SESSION()
    try:
        yield db
    finally:
        db.close()