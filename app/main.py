from fastapi import FastAPI
from app.routes import pdf_routes, qa_routes

app = FastAPI()

@app.get("/")
def welcome_message_json():
    return {
        "message": "¡Bienvenido al Sistema RAG!",
        "documentation_url": "/docs"
    }

app.include_router(pdf_routes.router, prefix="/pdf", tags=["PDF"])
app.include_router(qa_routes.router, prefix="/qa", tags=["Q&A"])