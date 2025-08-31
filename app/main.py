# Importamos FastAPI, el framework que utilizaremos para crear nuestra API REST.
from fastapi import FastAPI 

# Importamos las rutas desde la carpeta "routes", lo que permite mantener el proyecto modular y organizado.
from app.routes import pdf_routes, qa_routes

# Creamos una instancia de la aplicación FastAPI.
app = FastAPI()

# Definimos la ruta raiz que devuelve un mensaje de bienvenida en formato JSON
@app.get("/")
def welcome_message_json():
    return {
        "message": "¡Bienvenido al Sistema RAG!",
        "documentation_url": "/docs"
    }

# Incluimos el router encargado de manejar todo lo relacionado con los archivos PDF,
# asignándole el prefijo "/pdf" y la etiqueta "PDF" para su agrupación en la documentación.
app.include_router(pdf_routes.router, prefix="/pdf", tags=["PDF"])

# Incluimos el router encargado de manejar la funcionalidad de Preguntas y Respuestas (Q&A),
# asignándole el prefijo "/qa" y la etiqueta "Q&A" en la documentación.
app.include_router(qa_routes.router, prefix="/qa", tags=["Q&A"])