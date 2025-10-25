# Crear entorno virutral
```sh
#Crear el entorno virtual
py -m venv venv
#Activar el entorno virtual
./venv/Scripts/activate
desactivate
#Instalacion de FASTAPI
pip install "fastapi[standard]"
#Inicializador uvicorn
uvicorn main:app
uvicorn main:app --reload --port 8000 --host 0.0.0.0

#Para enlistar las librerias 
pip list
py -m pip list
pip freeze 
#Guardar todas la librerias en un archivo txt
pip freeze > requeriments.txt
#Instalar las librerias del requerimients
pip install -r requeriments.txt
#Desinstalar las librerias del requerimients
pip uninstall -y -r requeriments.txt7
#Leer variables de entorno
pip install python-dotenv
#Instalar el ORM y Manejador de base de datos SQLalchemy
pip install sqlalchemy
