# De FastAPI importamos:
# - APIRouter: para crear y organizar las rutas de este modulo.
from fastapi import APIRouter

# Importamos el controlador que busca el vector mas cercano en la DB
from app.controllers.qa_controller import get_most_similar_chunk

# Importamos el controlador que genera una respuesta formal usando un LLM
from app.llm.llm_controller import generate_answer

# Creamos una instancia de APIRouter.
router = APIRouter()

# Definimos un endpoint POST, que luego sera conectado en el main
@router.post("/ask")
def ask_question_endpoint(question: str):

    # Recibimos la pregunta y buscamos el chunk más cercano
    chunk_result = get_most_similar_chunk(question)

    # Si no hay chunk relevante (similaridad < 0.4), devolvemos mensaje por defecto
    if "chunk" not in chunk_result:
        return {
            "answer": "No se encontró información relevante",
            "context": None,
            "info": chunk_result.get("message", "")
        }

    # Si sí hay chunk, generamos la respuesta usando la pregunta y el chunk
    answer = generate_answer(question, chunk_result["chunk"])

    # Retornamos la respuesta final, el chunk usado y su similitud
    return {
        "answer": answer,
        "context_used": chunk_result["chunk"],
        "similarity": chunk_result.get("similarity", 0)
    }
