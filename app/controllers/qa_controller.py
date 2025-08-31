from sentence_transformers import SentenceTransformer # Importamos SentenceTransformer (para usar embeddings y vectorizar texto)
from sklearn.metrics.pairwise import cosine_similarity # Importamos cosine_similarity de sklearn para medir similitud entre vectores
import numpy as np # Importamos numpy para manejo de arrays y operaciones numericas
from app.db.mongo import db # Importamos la conexion a la base de datos MongoDB
from app.config import settings

#Creamos una instancia de SentenceTransformer, pasando el nombre del modelo
embeddings_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

collection = db[settings.COLLECTION_NAME]

# Función para encontrar el chunk de texto mas cercano a la pregunta
# Usa embeddings y similitud coseno, con un umbral minimo por defecto de 0.4
def get_most_similar_chunk(question: str, min_similarity: float = 0.4):

    # Transformamos la pregunta en un vector (embedding) para poder compararlo
    question_embedding = embeddings_model.encode(question)

    # Traemos los documentos de la base de datos, solo con los campos 'text' y 'embedding'
    docs = list(collection.find({}, {"text": 1, "embedding": 1, "_id": 0}))

    # Si no hay documentos, retornamos un mensaje indicando que la DB está vacia
    if not docs:
        return {"message": "No hay datos en la base"}

    # Creamos un array con los embeddings de todos los documentos
    embeddings = np.array([doc["embedding"] for doc in docs])
    
    # Calculamos la similitud coseno entre la pregunta y todos los documentos
    similarities = cosine_similarity([question_embedding], embeddings)[0]

    # Obtenemos el indice del documento con mayor similitud
    max_idx = np.argmax(similarities)
    max_sim = similarities[max_idx]

    # Si la mayor similitud es menor al umbral mínimo, retornamos un mensaje
    if max_sim < min_similarity:
        return {"message": "No se encontró un chunk suficientemente cercano"}

    # Si pasa el umbral, retornamos la similitud y el texto del chunk más cercano
    return {
        "similarity": float(max_sim),
        "chunk": docs[max_idx]["text"]
    }
