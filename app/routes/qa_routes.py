from fastapi import APIRouter
from app.controllers.qa_controller import get_most_similar_chunk
from app.llm.llm_controller import generate_answer

router = APIRouter()

@router.post("/ask")
def ask_question_endpoint(question: str):
    chunk_result = get_most_similar_chunk(question)
    if "chunk" not in chunk_result:
        return {"answer": "No se encontró información relevante", "context": None}

    answer = generate_answer(question, chunk_result["chunk"])

    return {
        "answer": answer,
        "context_used": chunk_result["chunk"],
        "similarity": chunk_result.get("similarity", 0)
    }
