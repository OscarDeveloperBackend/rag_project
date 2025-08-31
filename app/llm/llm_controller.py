import traceback # Para imprimir el detalle de errores si algo falla
from openai import OpenAI  # Cliente para conectarse a OpenAI/OpenRouter
from app.config import settings # Para cargar la API key y otras configuraciones

# Creamos la instancia del cliente de OpenRouter usando la API key del .env
client = OpenAI(
    api_key=settings.OPEN_ROUTER,
    base_url="https://openrouter.ai/api/v1"
)

# Modelo que se usara para generar las respuestas
OPENROUTER_MODEL = "deepseek/deepseek-chat-v3.1:free"

# Funcion que genera una respuesta usando el llm para procesar la pregunta y la respuesta.
def generate_answer(question: str, context: str) -> str:
    try:
        prompt = f"""Eres un asistente útil y servicial. 
        Responde a la siguiente pregunta de forma clara y completa usando únicamente la información del contexto. 
        Ignora cualquier '\\n' o salto de línea que aparezca en los datos, y no agregues saltos de línea en tu respuesta. 
        Si no hay suficiente información en el contexto, responde exactamente: "No se encontró información para responder". 
        Contexto: {context} Pregunta: {question} Respuesta:"""


        # Llamamos al endpoint de chat completions para generar la respuesta
        response = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )

        # Devolvemos la respuesta generada, eliminando espacios al inicio y final
        return response.choices[0].message.content.strip()

    except Exception as e:
        # En caso de error, imprimimos el detalle y retornamos mensaje por defecto
        print("ERROR en generate_answer:", e)
        traceback.print_exc()
        return "Lo siento, no pude generar una respuesta en este momento."
