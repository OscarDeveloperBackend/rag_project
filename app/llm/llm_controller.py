import traceback
from openai import OpenAI
from app.config import settings

client = OpenAI(
    api_key=settings.OPEN_ROUTER,
    base_url="https://openrouter.ai/api/v1"
)

OPENROUTER_MODEL = "deepseek/deepseek-chat-v3.1:free"

def generate_answer(question: str, context: str) -> str:
    try:
        prompt = f"""Eres un asistente útil y servicial.
Responde a la siguiente pregunta de forma clara y completa, usando únicamente la información del contexto.
Si no hay suficiente información en el contexto, responde exactamente: "No se encontró información para responder".

Contexto:
{context}

Pregunta:
{question}

Respuesta:"""

        response = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("ERROR en generate_answer:", e)
        traceback.print_exc()
        return "Lo siento, no pude generar una respuesta en este momento."
