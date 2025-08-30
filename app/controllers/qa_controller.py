from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.db.mongo import db

embeddings_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

collection = db["colegio_data"]

def get_most_similar_chunk(question: str, min_similarity: float = 0.4):

    question_embedding = embeddings_model.encode(question)

    docs = list(collection.find({}, {"text": 1, "embedding": 1, "_id": 0}))

    if not docs:
        return {"message": "No hay datos en la base"}

    embeddings = np.array([doc["embedding"] for doc in docs])
    similarities = cosine_similarity([question_embedding], embeddings)[0]

    max_idx = np.argmax(similarities)
    max_sim = similarities[max_idx]

    if max_sim < min_similarity:
        return {"message": "No se encontró un chunk suficientemente cercano"}

    return {
        "similarity": float(max_sim),
        "chunk": docs[max_idx]["text"]
    }
