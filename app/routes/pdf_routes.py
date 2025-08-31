# De FastAPI importamos:
# - APIRouter: para crear y organizar las rutas de este modulo.
# - UploadFile: para recibir el archivo PDF que se suba.
# - File: para indicar que el parametro 'file' se recibirá como archivo.
# - Query: para manejar y validar parametros en la URL.
from fastapi import APIRouter, UploadFile, File,Query

# Importamos el controlador que se encargara de procesar el PDF, subirlo, vectorisarlo y guardarlo.
from app.controllers import pdf_controller

# Creamos una instancia de APIRouter.
router = APIRouter()

# Definimos un endpoint (POST /upload), que luego sera conectado en el main
@router.post("/upload")
def upload_pdf(file: UploadFile = File(...), clear: bool = Query(True)):
    return pdf_controller.handle_upload(file, clear=clear)
