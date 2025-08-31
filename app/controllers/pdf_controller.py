import io # - io: para trabajar con flujos de bytes leer PDF en memoria.
import re # - re: para usar expresiones regulares en la limpieza y extraccpin de texto.
import traceback # - traceback: para mostrar el detalle de errores cuando ocurra una excepcion.
from datetime import datetime # - datetime: para registrar fechas y horas (ej: cuando se ingresa un documento).
from typing import List # - typing.List: para indicar que una función devuelve una lista de strings u otros tipos.

import numpy as np # - numpy: para manejar manejar los vectores numericos de los embeddings.
import pdfplumber # - pdfplumber: para extraer texto de archivos PDF.
# - sentence_transformers: para cargar un modelo para generar embeddings de texto.
from sentence_transformers import SentenceTransformer 

from app.db.mongo import db # - db: conexion a la base de datos MongoDB.
from app.config import settings # - cargar las variables de entorno.

#Creamos una instancia de SentenceTransformer, pasando el nombre del modelo
embeddings_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Función usada en la ruta para subir el archivo PDF.
def handle_upload(file, clear: bool = True):

    # Si el archivo no tiene extensión .pdf, devolvemos un error.
    if not file.filename.endswith(".pdf"):
        return {"error": "El archivo no es un PDF valido."}

    # Si es vlido, leemos su contenido en bytes y obtenemos el nombre del archivo.
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

        # Extraemos el texto del PDF y lo convertimos en una lista de personas
        personas = extract_people_from_pdf_bytes(tmp_bytes)

        # si la lista de personas esta vacaa, devolvemos un mensaje indicando.
        if not personas:
            return {
                "message": "No se detectaron entradas con el patron esperado o hubo un error.",
                "filename": filename,
                "detected_people": 0,
                "inserted": 0,
            }

        # procesamos la lista de personas y generamos sus embeddings con el modelo
        docs = build_docs_with_embeddings(personas, filename)

        # Obtenemos la coleccion de MongoDB
        collection = db[settings.COLLECTION_NAME]

        # Si el parámetro clear esta en True (por defecto), borramos la colección antes de insertar
        if clear:
            collection.delete_many({})

        # Insertamos los documentos si existen, y contamos cuantos fueron guardados.
        if docs:
            res = collection.insert_many(docs)
            inserted = len(res.inserted_ids)
        else:
            inserted = 0

        # Retornamos un resumen con la información del proceso:
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

# Función que recibe el PDF en bytes, extrae el texto y devuelve una lista de personas en forma de strings
def extract_people_from_pdf_bytes(pdf_bytes: bytes) -> List[str]:

    try:
        all_text = ""
        # Usamos pdfplumber para leer el PDF desde los bytes y extraer todo el texto.
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"

        # Si no se encuentra texto devolvemos una lista vacia.
        if not all_text.strip():
            return []

        # usamos una expresion regular para extraer bloques de texto que empiezan con un numero y un punto (ej: "1. Nombre ....")
        personas = re.findall(
            r"\d+\.\s+.*?(?=\n?\d+\.\s+|\Z)", all_text, flags=re.DOTALL
        )

        personas_limpias = []
        # recorremos la lista de personas y por cada persona:
        for persona in personas:
            persona = persona.strip()   # quitamos espacios al inicio y final
            # reemplazamos saltos de linea por espacios
            persona = persona.replace("\r", " ").replace("\n", " ") 
            persona = re.sub(r"\s+", " ", persona).strip() 
            #al final si hay contenido en persobn lo agregamso ala lsita
            if persona:
                personas_limpias.append(persona)

        return personas_limpias

    except Exception:
        traceback.print_exc()
        return []

# funcion que procesa la lista de personas extraidas del PDF 
def build_docs_with_embeddings(text_blocks: List[str], source_filename: str):

    # Verificamos si hay datos, en caso contrario retornamos lista vacaa
    if not text_blocks:
        return []

    #Usamos el modelo cargado para vectorizar la data y generar los embeddings
    vectors = embeddings_model.encode(
        text_blocks, batch_size=32, show_progress_bar=False
    )
    
    # Obtenemos la fecha y hora actual en formato ISO para registra
    now_iso = datetime.utcnow().isoformat() + "Z"

    docs = []
    # Recorremos las personas junto con sus vectores usando zip.
    for i, (persona, vec) in enumerate(zip(text_blocks, vectors), start=1):
        docs.append(
            {
                "text": persona,
                # convertimos el vector de NumPy a lista para poder guardarlo en MongoDB
                "embedding": np.asarray(vec).tolist(),
                "person_id": i,
                "source": source_filename,
                "ingested_at": now_iso,
            }
        )
    return docs


