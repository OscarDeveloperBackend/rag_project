import io
import re
import traceback
from datetime import datetime
from typing import List

import numpy as np
import pdfplumber
from sentence_transformers import SentenceTransformer

from app.db.mongo import db
from app.config import settings

embeddings_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def extract_people_from_pdf_bytes(pdf_bytes: bytes) -> List[str]:
    """
    Extrae el texto del PDF (bytes) y lo divide por entradas que empiezan con
    un número seguido de punto (ej: "14. Priya Patel ...").
    Devuelve una lista de strings limpios (cada persona).
    """
    try:
        all_text = ""
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"

        if not all_text.strip():
            return []

        personas = re.findall(
            r"\d+\.\s+.*?(?=\n?\d+\.\s+|\Z)", all_text, flags=re.DOTALL
        )

        personas_limpias = []
        for persona in personas:
            persona = persona.strip()
            persona = persona.replace("\r", " ").replace("\n", " ")
            persona = re.sub(r"\s+", " ", persona).strip()
            if persona:
                personas_limpias.append(persona)

        return personas_limpias

    except Exception:
        traceback.print_exc()
        return []


def build_docs_with_embeddings(text_blocks: List[str], source_filename: str):

    if not text_blocks:
        return []

    vectors = embeddings_model.encode(
        text_blocks, batch_size=32, show_progress_bar=False
    )
    now_iso = datetime.utcnow().isoformat() + "Z"

    docs = []
    for i, (persona, vec) in enumerate(zip(text_blocks, vectors), start=1):
        docs.append(
            {
                "text": persona,
                "embedding": np.asarray(vec).tolist(),
                "person_id": i,
                "source": source_filename,
                "ingested_at": now_iso,
            }
        )
    return docs


def handle_upload(file, clear: bool = True):

    if not file.filename.endswith(".pdf"):
        return {"error": "El archivo no es un PDF válido."}
    tmp_bytes = None
    try:
        if hasattr(file, "file"):
            tmp_bytes = file.file.read()
            filename = getattr(file, "filename", "uploaded.pdf")
        elif isinstance(file, (bytes, bytearray)):
            tmp_bytes = bytes(file)
            filename = "uploaded.pdf"
        else:
            return {"error": "Archivo inválido."}

        personas = extract_people_from_pdf_bytes(tmp_bytes)
        if not personas:
            return {
                "message": "No se detectaron entradas con el patrón esperado (ej: '1. Nombre ...').",
                "filename": filename,
                "detected_people": 0,
                "inserted": 0,
            }

        docs = build_docs_with_embeddings(personas, filename)

        collection = db[settings.COLLECTION_NAME]

        if clear:
            collection.delete_many({})

        if docs:
            res = collection.insert_many(docs)
            inserted = len(res.inserted_ids)
        else:
            inserted = 0

        return {
            "message": "PDF procesado y guardado correctamente.",
            "filename": filename,
            "detected_people": len(personas),
            "inserted": inserted,
            "collection": collection.name,
            "cleared_before_insert": bool(clear),
        }

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
